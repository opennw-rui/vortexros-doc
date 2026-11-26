# 物理接口、聚合、VLAN、BD 与邻居

## 接口所有权

设备只允许一个转发平面管理物理接口。VPP未启用时，可在CLI中配置Linux能够识别的物理口；VPP接管完成后，只允许配置设备已经识别的业务接口。接管过程中接口配置暂时只读，避免同一接口同时由两套转发平面管理。

```vortexros-cli
display vpp interface-ownership verbose
display interface brief
display ip interface brief
display ipv6 interface brief
```

状态含义：`^down`表示配置对象已创建但尚不满足底层数据面创建条件；普通`down`表示底层对象存在但链路或协议条件未满足。接口无IP不应因此down。

`display interface brief`中的`CRC`只显示网卡驱动提供的硬件CRC/FCS坏帧计数；驱动或虚拟接口不支持该计数时显示`--`。它不会把接口down期间的发送尝试、转发丢弃或其他软件错误混入CRC。使用`display interface <接口>`查看CRC/FCS、丢弃、punt以及收发方向的软件错误明细。

`InUti/OutUti`由daemon复用一条VPP统计连接，每秒读取标准字节计数，并使用最近300秒的成熟窗口按接口链路速率换算为一位小数的利用率。daemon启动、VPP重连、同名接口重建、计数器清零或尚未形成完整300秒窗口时显示`0.0%`；执行display命令本身不会临时采样或等待。统计读取连续超过3秒未成功时旧速率立即失效，不会把故障前的数值继续显示成当前状态。NVE和尚未创建数据面对象的隧道没有独立计数器，显示`--`而不是虚构零流量。CRC/FCS属于低频诊断计数，不进入每秒采样。

`display interface <接口>`同时显示当前1秒速率和最近300秒平均速率。daemon启动或VPP重连后的前两个有效样本之间，当前速率显示`--`；连续采样尚未达到300秒时，300秒平均值显示`--`。计数器清零、接口运行索引变化或VPP会话变化会废弃该接口的旧窗口，不会把两个对象的累计计数相减。

IP简表合并VPP与LCP地址。LCP接口正在删除或重建而无法完成地址观察时，该行地址与协议状态显示`unavailable`/`unknown`，且不计入协议UP或DOWN数量；这表示当前证据不足，不表示接口已经确认协议Down。其他接口仍正常显示。

## 物理接口与offload

```text
interface Ethernet 1
 description uplink
 mtu 9000
 ip address 192.0.2.2 255.255.255.0
 undo hardware offload tso tx-checksum rx-checksum
```

先用 `display interface hardware offload Ethernet1` 查看设备支持的能力。示例同时关闭 TSO 与其依赖的收发校验和卸载。用 `hardware offload` 撤销禁用项，具体项以设备实际能力为准。

IPv4继续使用主地址与`sub`从地址语义；IPv6地址为累加列表，不使用`sub`：

```text
interface LoopBack 0
 ipv6 address 2001:db8:100::1 64
 ipv6 address 2001:db8:200::1 64
```

同一接口最多配置16个IPv6全局单播地址。同一VPN实例内，同一IPv6前缀只允许归属一个接口；
未指定、多播、链路本地、IPv4映射地址以及物理接口上的回环地址在进入Candidate时拒绝。前缀长度
小于127时，前缀本身的全零接口标识保留为子网路由器任播地址，不能作为普通接口地址。

| 步骤 | Candidate变化 | commit后效果 | 验证 |
|---|---|---|---|
| 创建/进入接口 | 无或创建配置对象 | 不一定创建数据面 | `display this` |
| 配置MTU/IP | 保存本会话修改 | 提交后更新接口MTU和地址 | `display interface Ethernet 1` |
| 关闭offload | 保存关闭项 | 提交后关闭硬件支持的指定能力 | `display interface hardware offload Ethernet 1` |
| 精确undo | 删除对应叶 | 恢复默认/撤销地址 | display及转发验证 |

## Eth-Trunk

聚合接口默认L3，支持static和LACP；成员必须是物理接口并满足兼容属性。加入后，成员不再允许独立配置L2/L3参数，聚合无关的ACL/QoS绑定按能力保留。

```text
interface Eth-Trunk 10
 mode lacp-static
 trunkport Ethernet 1 to Ethernet 2
 mtu 9000
 ip address 198.51.100.1 255.255.255.0
```

```vortexros-cli
display eth-trunk 10
display interface Eth-Trunk 10
```

反复增删成员时只变更相关成员，不重建无变化的聚合接口。

删除单个成员或整个聚合接口：

```text
interface Eth-Trunk 10
 undo trunkport Ethernet 2
undo interface Eth-Trunk 10
commit
```

成员口退出聚合后，才可重新配置其独立的二层/三层属性。

## 三层子接口

```text
interface Ethernet 1.100
 encapsulation dot1q vid 100
 ip address 10.100.0.1 255.255.255.0
```

QinQ示例：

```text
interface Ethernet 1.200
 encapsulation qinq vid 200 ce-vid 20
 ip address 10.200.20.1 255.255.255.0
```

提交后，只有标签匹配的报文进入对应子接口。父接口down时子接口随之down；父接口恢复后自动恢复。使用以下命令验证：

```vortexros-cli
display interface Ethernet 1.100
display ip interface brief
display ip routing-table protocol direct
```

## VLAN、子接口与Vlanif

```text
vlan batch 100 200
interface Ethernet 1
 portswitch
 port link-type trunk
 port trunk allow-pass vlan 100 200
interface Vlanif 100
 ip address 10.100.0.1 255.255.255.0
```

配置在二层物理接口或VLAN上的策略会作用于对应的trunk业务流量。Vlanif只有在VLAN中至少存在一个可用成员端口时才能正常up；没有可用成员时显示普通down，并撤销相关直连路由。

`display vlan`使用一张表同时显示状态、MAC学习、描述和端口成员，端口状态中的`U/D`表示up/down，`TG/UT`表示tagged/untagged。表格宽度根据实际内容调整；端口之间间隔两个字符，每行最多显示四个端口，更多端口在下一行按首个接口位置继续显示：

```text
-----------------------------------------------------------------
U: Up;         D: Down;         TG: Tagged;         UT: Untagged;
-----------------------------------------------------------------

VID  Type    Status  MAC-LRN  Description    Ports
-----------------------------------------------------------------
1    common  enable  enable   VLAN 1         UT:eth2(D)  eth3(D)
10   common  enable  enable   To_CTC_ISP     UT:eth0(U)
20   common  enable  enable   To_LAN_Client  UT:eth1(U)
-----------------------------------------------------------------
```

`display ip interface brief`和`display ipv6 interface brief`保持相同的状态列布局，便于同时核对Physical、Protocol和VPN-Instance。

隐式默认MAC不进入 `display current-configuration` 或 `display this`。

启用交换功能后，每个VLAN对应的转发域默认采用以下行为：

- 动态MAC学习：开启；
- 广播和组播泛洪：开启；
- 未知单播泛洪：开启；
- 二层转发：开启；
- 动态MAC老化时间：300秒。

动态MAC老化时间是全局参数。需要修改时，在系统视图执行：

```text
mac-address aging-time 600
commit
```

提交后，所有VLAN对应转发域的动态MAC老化时间变为600秒。恢复默认值：

```text
undo mac-address aging-time
commit
```

默认值不显示在配置中；只有非默认值才进入 `display current-configuration`。VPP以整分钟保存该参数，因此配置值必须是60秒的整数倍。

## BD与Vbdif

```text
bridge-domain 11
 l2 binding vlan 100
 vxlan vni 1011
interface Vbdif 11
 ip address 10.11.0.1 255.255.255.0
```

验证BD、VNI、MAC学习和L3网关：

```vortexros-cli
display bridge-domain 11
display mac-address
display interface Vbdif 11
```

删除前先解除Vbdif、VNI和VLAN绑定，避免业务仍在引用BD。

### 高位 Bridge Domain

普通 VLAN 业务 VID 为 1–4094，4095 保留。需要扩展域编号的服务可显式使用 4096–4294967294 的高位 BD。高位编号独立于普通 VLAN 和 VXLAN VNI。常规 STP、RSTP 和 MSTP 沿用普通端口或 VLAN 范围。

先为 NVE 准备可达的 VTEP 源和 EVPN 邻居。同一 VNI 的两端使用匹配的 RT，每台设备使用自己的 RD。以下示例将 Ethernet0 接入高位域 65536，把它关联到 VNI 65010。

```text
system-view
evpn-overlay enable
bridge-domain 65536
vxlan vni 65010
evpn
route-distinguisher 65000:1101
vpn-target 65000:65010 import-extcommunity
vpn-target 65000:65010 export-extcommunity
quit
quit
interface Ethernet0
bridge-domain 65536
quit
interface Nve1
vni 65010 head-end peer-list protocol bgp
quit
commit
```

部署高位 EVPN 时，用 `display bridge-domain` 和 `display mac-address` 核对域归属和 MAC 学习，再检查 VNI、远端 VTEP 和 EVPN 路由。迁移网关或成员后，确认旧位置的远端 MAC/IP 已撤销并在新位置重新学习。可以在不同域使用同一客户 VID 或 MAC，验证时应检查域间隔离和域内连通。

撤销该 VNI 的动态通告时，在对应 NVE 视图执行 `undo vni 65010 head-end peer-list protocol bgp` 并提交。随后核对受影响域的远端状态和其余域的转发。

## ARP与代理ARP

IPv4 ARP和IPv6 ND邻居老化是VPP进程级参数，不依赖VLAN或bridge-domain。纯三层接口同样使用这些参数。默认值均为1200秒，并在VPP每次启动或重新连接后优先恢复，再下发接口、地址和业务配置。

```text
arp timeout 900
ipv6 nd stale-timeout 1800
ipv6 nd max-number 65536
ipv6 nd recycle enable
commit
```

恢复默认值：

```text
undo arp timeout
undo ipv6 nd stale-timeout
undo ipv6 nd max-number
undo ipv6 nd recycle
commit
```

`max-number`限制VPP IPv6邻居表容量；`recycle enable`在容量已满时回收最老的动态条目，静态邻居不参与动态回收。回收策略必须显式配置，`undo`恢复VPP启动时的默认策略。上述命令只管理VPP邻居表，不修改Linux内核的ARP/ND参数。默认值不显示在配置中，非默认值通过 `display current-configuration` 和 `display ipv6 nd` 回读验证。

静态IPv6邻居绑定在三层数据面接口上，地址与MAC均以规范格式保存：

```text
ipv6 neighbor 2001:db8:10::2 02:11:22:33:44:55 interface Vlanif10
commit
display ipv6 neighbors static
undo ipv6 neighbor 2001:db8:10::2 02:11:22:33:44:55 interface Vlanif10
commit
```

多播、未指定IPv6地址，多播或全零MAC，以及二层或控制型接口都会在提交前被拒绝。动态邻居只属于运行态，不会写入配置。

静态ARP和单IP/范围代理ARP必须绑定一个真实、具备MAC且能发送ARP的L3接口；LoopBack和NVE不出现在补全中。

静态ARP只接受可用IPv4单播地址和六字节单播MAC；全零、组播或广播映射会在提交前拒绝。静态MAC
表项的出口必须实际属于该表项的桥域；trunk与业务桥域先转换为最终数据面子接口和桥域后再校验，
不能把其他桥域的端口写入当前桥域。

```text
arp proxy 10.10.10.12 10.10.10.14 interface Vlanif 100
display arp proxy
undo arp proxy 10.10.10.12 10.10.10.14 interface Vlanif 100
```

提交后，指定地址范围的ARP请求从所选三层接口代理响应。接口down/up或重新创建后，设备会自动恢复已经提交的代理配置。

## 接口状态时间

`display interface`中的最近up/down时间来自接口实际状态变化，不会因为执行display而重置。控制服务重启后无法确认的历史时间显示 `-`；修改时区只会改变时间的显示方式。

## 删除顺序

先解除路由、隧道、VRRP/BFD、策略和VPN引用，再删除IP、成员、Vlanif/BD/VLAN/聚合对象。校验器会在进入Candidate前拒绝明显的悬空引用。
