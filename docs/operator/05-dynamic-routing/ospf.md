# OSPF（IPv4）

## 功能介绍

OSPF 为 IPv4 域内路由交换链路状态，可用多区域组织网络。

## 配置准备

为每台路由器选独立的 Router ID。检查链路地址、区域、网络类型和计时两端一致。

## 配置案例

### 使用area下的network激活

```text
ospf 1 router-id 10.0.0.1
 opaque-capability enable
 area 0.0.0.0
  network 10.0.12.1 0.0.0.0 description P1-P2
```

`network`只能在area视图中输入。提交后，地址匹配的接口开始发送Hello报文；只有两端area、网络类型、认证和计时等条件兼容时才会建立邻居。

### 使用接口命令激活

```text
ospf 1 router-id 10.0.0.1
interface Vlanif 12
 ospf enable 1 area 0.0.0.0
 ospf network-type p2p
 ospf cost 10
 ospf dr-priority 100
```

同一进程只能选择 `network` 或接口 `ospf enable` 一种激活方式；混用会在命令进入待提交配置前报错。广播网络上的DR优先级范围为0至255，0表示不参与DR/BDR选举。

### Stub、NSSA与区域汇总

区域类型和汇总在area视图配置：

```text
ospf 1
 area 0.0.0.1
  nssa no-summary
  abr-summary 10.0.0.0 255.0.0.0 not-advertise
```

`stub`与`nssa`互斥；已经配置一种类型时，必须先执行对应的`undo`，不能用另一条命令隐式覆盖。`no-summary`阻止向该区域发布三类汇总路由，`not-advertise`阻止发布指定区域汇总。撤销命令为`undo stub`、`undo nssa`和`undo abr-summary ADDRESS MASK`。

### 验证与撤销

```vortexros-cli
display ospf 1 brief
display ospf 1 peer brief
display ospf 1 peer 10.0.0.2
display ospf 1 interface
display ospf 1 lsdb
display ospf 1 routing
```

`display ospf peer brief`按以下顺序显示，Interface位于Neighbor id左侧：

```text
Area Id    Pri  Up Time   Dead Time  Interface   Neighbor id  State
0.0.0.0      1  00:12:31  00:00:38   Vlanif12    10.0.0.2     Full
```

修改与删除示例：

```text
interface Vlanif 12
 undo ospf dr-priority
 undo ospf network-type
 undo ospf enable 1
undo ospf 1
commit
```

撤销接口激活只影响该接口；删除进程会撤销该进程的全部邻居和路由。

### 两台设备建立 Area 0 邻接

R1 Ethernet0 192.0.2.1/24 直连 R2 Ethernet0 192.0.2.2/24。两端通告各自 LoopBack0 的 198.51.100.1/32 和 198.51.100.2/32。

两台设备分别在系统视图录入各自的配置片段，退出功能视图后提交。

**R1**

```vortexros-config
ospf 1 router-id 198.51.100.1
 area 0.0.0.0
#
interface Ethernet 0
 ip address 192.0.2.1 255.255.255.0
 ospf enable 1 area 0.0.0.0
 ospf network-type p2p
#
interface LoopBack 0
 ip address 198.51.100.1 255.255.255.255
 ospf enable 1 area 0.0.0.0
#
return
```

**R2**

```vortexros-config
ospf 1 router-id 198.51.100.2
 area 0.0.0.0
#
interface Ethernet 0
 ip address 192.0.2.2 255.255.255.0
 ospf enable 1 area 0.0.0.0
 ospf network-type p2p
#
interface LoopBack 0
 ip address 198.51.100.2 255.255.255.255
 ospf enable 1 area 0.0.0.0
#
return
```

分别查看状态。

```vortexros-cli
display ospf 1 peer brief
display ospf 1 interface
display ip routing-table protocol ospf
```

两端 Area 均为 0.0.0.0，邻居为 Full。R1 应看到 198.51.100.2/32 的 OSPF 路由，下一跳为 192.0.2.2。R2 应看到相反方向的路由。从 R1 ping 198.51.100.2 核对转发。

### 在管理 VPN 内建立独立 OSPF 邻居

沿用上面的物理连线。在另一套配置中把两个接口都放入 BLUE，进程改为 2，区域改为 0.0.0.200。

两台设备分别在系统视图录入各自的配置片段，退出功能视图后提交。

**R1**

```vortexros-config
ip vpn-instance BLUE
 ipv4-family
#
ospf 2 router-id 198.51.100.1 vpn-instance BLUE
 area 0.0.0.200
#
interface Ethernet 0
 ip binding vpn-instance BLUE
 ip address 192.0.2.1 255.255.255.0
 ospf enable 2 area 0.0.0.200
 ospf network-type p2p
#
interface LoopBack 0
 ip binding vpn-instance BLUE
 ip address 198.51.100.1 255.255.255.255
 ospf enable 2 area 0.0.0.200
#
return
```

**R2**

```vortexros-config
ip vpn-instance BLUE
 ipv4-family
#
ospf 2 router-id 198.51.100.2 vpn-instance BLUE
 area 0.0.0.200
#
interface Ethernet 0
 ip binding vpn-instance BLUE
 ip address 192.0.2.2 255.255.255.0
 ospf enable 2 area 0.0.0.200
 ospf network-type p2p
#
interface LoopBack 0
 ip binding vpn-instance BLUE
 ip address 198.51.100.2 255.255.255.255
 ospf enable 2 area 0.0.0.200
#
return
```

分别查看状态。

```vortexros-cli
display ospf 2 peer brief
display ip routing-table vpn-instance BLUE protocol ospf
```

进程 2 中邻居达到 Full。远端环回应出现在 BLUE 路由表。从 R1 执行 `ping -vpn-instance BLUE 198.51.100.2` 检查。

## 验证配置

```vortexros-cli
display ospf peer brief
display ip routing-table protocol ospf
```

核对邻接状态、学习的前缀及下一跳，并从下游测试连通性。
