# 802.1Q 与 QinQ 三层子接口

## 功能介绍

三层子接口按 802.1Q 标签区分共用物理链路的多个网段。QinQ 用外层和内层标签共同区分业务。

## 配置准备

确保父接口按三层模式工作。对端须发送与相应子接口匹配的单标签或双标签。

## 配置案例

```text
interface Ethernet 1.100
 vlan-type dot1q 100
 ip address 10.100.0.1 255.255.255.0
```

QinQ示例：

```text
interface Ethernet 1.200
 vlan-type dot1q 200 inner 20
 ip address 10.200.20.1 255.255.255.0
```

提交后，只有标签匹配的报文进入对应子接口。父接口down时子接口随之down；父接口恢复后自动恢复。使用以下命令验证：

```vortexros-cli
display interface Ethernet 1.100
display ip interface brief
display ip routing-table protocol direct
```

### 两端的 802.1Q 三层子接口

将 R1 和 R2 的 Ethernet1 直连。VLAN 100 和 200 分别使用不同的 IPv4 子网。父接口保持三层模式。

两台设备分别在系统视图录入各自的配置片段，退出功能视图后提交。

**R1**

```vortexros-config
interface Ethernet 1.100
 vlan-type dot1q 100
 ip address 198.51.100.1 255.255.255.0
#
interface Ethernet 1.200
 vlan-type dot1q 200
 ip address 203.0.113.1 255.255.255.0
#
return
```

**R2**

```vortexros-config
interface Ethernet 1.100
 vlan-type dot1q 100
 ip address 198.51.100.2 255.255.255.0
#
interface Ethernet 1.200
 vlan-type dot1q 200
 ip address 203.0.113.2 255.255.255.0
#
return
```

分别查看状态。

```vortexros-cli
display interface Ethernet 1.100
display interface Ethernet 1.200
display ip interface brief
```

两端的 1.100 与 1.200 均应为 up，各自 IP 正确。分别 ping 对端 198.51.100.x 与 203.0.113.x。两端标签不一致时，对应网络的流量无法由正确的子接口接收。

### 灵活 QinQ 二层接入

每端 Ethernet1 连客户上联，外层 VID 为 200，客户内层允许 20–29。每端 Ethernet2 接业务侧，显式加入 BD 20。先分别在两端提交以下相同配置。该拓扑可与静态 VXLAN 组合，按其案例在两个 BD 20 间建立相同 VNI，把本地业务延伸到对端。

```vortexros-config
bridge-domain 20
#
interface Ethernet 1.200 mode l2
 encapsulation qinq vid 200 ce-vid 20 to 29
 rewrite pop none
 bridge-domain 20
#
interface Ethernet 2
 bridge-domain 20
#
return
```

```vortexros-cli
display interface Ethernet 1.200
display bridge-domain 20
display ip interface brief
```

1.200 应归属 BD 20，普通接口状态中能看到它，IP 简表中没有该二层口。用可生成双标签的客户设备分别测试 200/20、200/29 和 200/30，前两组应进入 BD 20，最后一组不应匹配。对端采用相同的标签约定。

## 验证配置

```vortexros-cli
display interface Ethernet 1.100
display interface Ethernet 1.200
display ip routing-table protocol direct
```

核对两个子接口的状态和直连路由。分别从两种标签的对端发包，确认流量经对应子接口进入。
