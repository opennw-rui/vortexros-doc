# DHCP 与 LLDP

本章说明VortexROS提供的DHCPv4/DHCPv6客户端、服务器、中继以及LLDP功能。系统自身的DNS解析由Linux负责；DHCP客户端不会把租约中的DNS服务器写入系统解析器。

## DHCPv4服务器

先在系统视图启用DHCP服务：

```text
enable dhcp
commit
```

使用全局地址池时，创建地址池并在三层接口启用：

```text
ip pool LAN4
 network 192.0.2.0 mask 255.255.255.0
 gateway-list 192.0.2.1
 section 0 192.0.2.100 192.0.2.200
 dns-list 1.1.1.1 8.8.8.8
 lease day 1
#
interface Vlanif 100
 ip address 192.0.2.1 255.255.255.0
 dhcp select global
```

池中的`dns-list`只作为DHCP Option通告给外部客户端，不改变VortexROS主机的`/etc/resolv.conf`。
全局地址池使用`section <编号> <起始地址> [结束地址]`限制可动态分配的地址段；可配置多个互不重叠的
section，编号范围为0至255。未配置section时使用network中的全部可用主机地址。网关、排除地址、
接口本机地址和静态绑定仍会从section中扣除。`gateway-list`与`dns-list`保持录入顺序，第一项是
客户端收到的首选地址，保存和重载不会按数值重新排序。
全局池应用到接口时，该接口在此子网内的全部本地IPv4地址都会自动从动态分配范围排除。
同一VPN实例内，一个IPv4或IPv6地址池只能绑定一个接口；当前版本不提供跨接口共享子网模型，
重复绑定会在进入Candidate时给出明确错误。

也可以直接使用接口主地址所在网段生成接口地址池。未配置`gateway-list`时，接口主IPv4地址自动作为客户端网关：

```text
interface Vlanif 20
 ip address 192.168.10.254 255.255.255.0
 dhcp select interface
 dhcp server ip-range 192.168.10.100 192.168.10.200
 dhcp server dns-list 1.1.1.1 8.8.8.8
 dhcp server lease day 1
#
commit
```

如需通告同网段内的其他网关，可用`dhcp server gateway-list X.X.X.X [X.X.X.X]`显式替换默认值。`undo dhcp server gateway-list`恢复“接口主地址作为网关”的默认行为。确实不希望发送Router Option时，使用`dhcp server gateway-list disable`。接口本机使用的所有IPv4地址始终从动态地址池排除，与通告哪个网关无关。

接口地址池使用`dhcp server ip-range <起始地址> <结束地址>`限制可分配范围；起止地址必须属于接口
主IPv4网段且均为可用主机地址。该范围存在时优先使用它，`undo dhcp server ip-range`恢复从接口
主网段的全部可用主机地址分配。接口地址池只保存一个显式范围；需要多个不连续地址段时使用全局
地址池的多个`section`。

验证：

```vortexros-cli
display dhcp service verbose
display ip pool
display current-configuration
```

`Ready`只有在Kea控制接口正常、主进程拥有正确的UDP监听、每个已配置LCP接口保持admin UP且目标地址仍可用时才显示为`true`；监听数量相同但绑定到无关地址，或服务启动后接口关闭、地址消失，都会判定为未就绪。一个服务器接口配置多个本地地址时，Kea会监听该接口的全部可用地址，因此中继可以把请求发往其中任一明确配置的服务地址。IPv6允许Kea使用能够覆盖已配置接口的UDP/547通配监听，但接口与地址可服务条件仍须满足。后台审计会持续执行这组检查，并在接口恢复后重新收敛。可用Linux的`ss -lunp`作辅助诊断，但产品状态以`display dhcp service verbose`的权威回读为准。

关闭接口上的服务器角色：

```text
interface Vlanif 100
 undo dhcp select
commit
```

确认已撤销需要停止的服务后，可在系统视图关闭 DHCP 服务器全局开关。

```vortexros-cli
undo enable dhcp server
commit
```

## DHCPv4客户端

```text
interface Ethernet 1
 ip address dhcp-alloc
commit
display dhcp client
```

客户端只接收和维护IPv4地址、默认路由、classless route及租约生命周期。撤销：

```text
interface Ethernet 1
 undo ip address dhcp-alloc
commit
```

VPP启用时，DHCP客户端运行在VPP为业务接口建立的LCP host接口上。报文仍通过对应VPP物理接口收发，客户端不会重新绑定、独占或接管物理网卡。这样IPv4与IPv6租约采用同一套生命周期、VRF、撤销和重启恢复逻辑，并且可以完整处理默认路由和classless route。租约中的DNS选项不写入Linux系统解析配置。

默认会安装DHCP学习到的默认路由，默认优先级为60。可以调整优先级，或显式禁止默认路由：

```text
interface Ethernet 1
 dhcp client default-route preference 80
 # 如不需要上游默认路由：
 undo dhcp client default-route enable
```

## DHCP服务器租约查看

`display ip pool`同时列出全局IPv4地址池和接口地址池。需要查看Kea已经实际分配的地址时，使用与设备命令树一致的`used`参数：

```vortexros-cli
display ip pool used
display ip pool name OFFICE used
display ip pool interface Vlanif20 used
```

`used`只显示仍有效的已分配地址；`all`显示Kea仍保留的全部租约状态，包括已过期或被拒绝的记录。输出包含地址池或接口、客户端IP、MAC、Client-ID、剩余租期、状态、主机名和VPN实例。租约来自Kea控制Socket的权威运行态，不读取可能正在写入的CSV文件；读取失败会明确报错，不会把观察失败显示为零租约。

DHCPv6服务器使用相同的运行态语义：

```vortexros-cli
display dhcpv6 pool name V6-POOL used
display ipv6 pool name V6-POOL all
```

IPv6输出区分IA_NA、IA_TA和IA_PD，并显示DUID/IAID、地址或委派前缀、剩余租期和状态。租约属于运行数据，不进入Candidate、CFG或SQLite配置投影。

Classless Static Route Option存在并启用解析时，按标准优先使用该选项，不再同时采用Router Option。无论默认路由来自哪个DHCP选项，`undo dhcp client default-route enable`都会阻止其中的`/0`，普通明细路由仍可安装。

## DHCPv6

```text
dhcpv6 pool LAN6
 address prefix 2001:db8:100::/64
 dns-server 2001:4860:4860::8888
#
interface Vlanif 100
 dhcpv6 server LAN6
```

验证和撤销：

```text
display dhcp service verbose
display ipv6 pool
interface Vlanif 100
 undo dhcpv6 server
commit
```

DHCPv6客户端和中继在对应接口视图配置；可使用`?`查看地址请求、前缀委派和中继目标的完整参数。DHCPv6客户端同样绑定LCP host接口，因此不会与VPP争用物理接口。

同一DHCPv6地址池内的地址前缀和委派前缀必须使用同一组有效/首选生命周期；显式生命周期最小为
60秒，首选生命周期不得大于有效生命周期。重叠的委派前缀在进入Candidate时即被拒绝，不会留到
Kea启动阶段才失败。

有状态地址、前缀委派以及立即续租的示例：

```text
interface Ethernet 1
 ipv6 address auto dhcp
 dhcpv6 client pd CPE-PREFIX
commit
display dhcpv6 client interface Ethernet 1
display dhcpv6 client prefix name CPE-PREFIX
# 在接口视图立即请求续租：
interface Ethernet 1
 dhcpv6 client renew
```

`display dhcpv6 client`分别显示IA_NA地址和IA_PD委派前缀，不会用其中一个字段遮盖另一个字段。`dhcpv6 client renew`是立即执行的运行命令，不进入Candidate或保存配置。

DHCPv6地址和IPv6路由器发现是两项独立功能。DHCPv6不会提供IPv6默认网关；默认路由来自Router Advertisement。需要同时从RA生成全局地址并接受RA默认路由时，可使用组合命令：

```text
interface Ethernet 1
 ipv6 address auto global default
commit
display ipv6 interface brief
display ipv6 neighbors
display ipv6 routing-table
```

若只需要其中一项，也可分别使用`ipv6 address auto slaac`或`ipv6 nd ra default-route enable`。使用有状态DHCPv6获取地址、同时从RA获取默认路由时，可以组合`ipv6 address auto dhcp`与`ipv6 nd ra default-route enable`，无需同时启用SLAAC地址生成。

VortexROS只在已配置的接口上开启RA接收。VPP模式下由该接口的LCP host接收RA，Linux内核执行DAD并维护前缀、首选时间、有效时间和Router Lifetime，linux-cp再把有效地址和路由同步到VPP。即使系统开启IPv6转发，该接口仍会使用明确的RA接收策略；其他接口不会被全局放开。接口属于VPN实例时，LCP接口先加入对应Linux VRF，学习结果留在该VPN的路由域内。

组合意图可一次撤销：

```text
interface Ethernet 1
 undo ipv6 address auto global default
commit
```

分别配置的地址自动生成与默认路由也可以用各自的精确`undo`撤销。

撤销全部RA功能后，控制面关闭该接口的RA、自动前缀和默认路由接收，并清理内核中由RA协议安装的路由及可识别的SLAAC地址。DHCPv6地址不属于这套清理范围。

## LLDP

```text
enable lldp
commit
display lldp neighbor brief
display lldp neighbor interface Ethernet0
```

关闭LLDP：

```text
undo lldp enable
commit
```

LLDP未收敛或后端不可用时会在`display health`和告警中显示，但不会触发VPP物理接口所有权回滚。

## DHCP 的接口限制

DHCPv4 和 DHCPv6 的发放、中继及客户端命令使用三层接口。交换接入端口保留二层转发，在该网段的 Vlanif 或适用的三层接口配置服务。帮助与 Tab 根据当前候选接口模式给出命令。

## SNMP

只读轮询支持 SNMPv2c，SNMPv3 使用 `authPriv`、SHA2-256 和 AES128。使用 `snmp-agent protocol source-interface vpn-instance NAME IFNAME` 时，先确认接口与管理实例一致且具有 IPv4 地址。授权凭据应使用设备专用值。

```vortexros-cli
display snmp-agent sys-info
display process udp listen
```

来自管理站的轮询应经实际配置的接口和路由表验证。设备查询监听使用 UDP 161，通知发送到配置的 IPv4 目标。用 `undo snmp-agent` 删除整套 SNMP 配置，并在提交后检查监听已撤销。
