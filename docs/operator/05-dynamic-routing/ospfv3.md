# OSPFv3（IPv6）

## 功能介绍

OSPFv3 为 IPv6 域内业务学习路由，在指定链路的三层接口建立邻居。

## 配置准备

准备 IPv6 上联、非重复的 Router ID 和两端相同的区域。

## 配置案例

OSPFv3用于IPv6动态路由。先创建进程和区域，再在三层接口下绑定进程：

```text
ospfv3 1 router-id 10.0.0.1
 maximum load-balancing 6
 bandwidth-reference 100000
 import-route static
 area 0.0.0.0
interface Vlanif 12
 ospfv3 1 area 0.0.0.0
```

接口必须属于与进程相同的 VPN 实例。进程 1 使用默认路由表，其他进程必须在创建时指定非默认 VPN，例如 `ospfv3 2 router-id 10.0.0.2 vpn-instance BLUE`。每个 VPN 只能配置一个 OSPFv3 进程。

Stub、NSSA和IPv6区域汇总在area视图配置：

```text
ospfv3 1
 area 0.0.0.1
  nssa no-summary
  abr-summary 2001:db8:: 32 not-advertise
```

`stub`与`nssa`互斥。`default-route-advertise`仅在本机已有IPv6默认路由时发布，`default-route-advertise always`则不依赖本机默认路由。`silent-interface INTERFACE`保留该接口的网络发布但停止建立邻居。

```vortexros-cli
display ospfv3 1 brief
display ospfv3 1 peer brief
display ospfv3 1 interface
display ospfv3 1 lsdb
display ospfv3 1 routing
```

`peer brief` 显示当前邻接，`routing` 显示 OSPFv3 学到的路由。正常时应同时确认邻居为 Full、目标 IPv6 路由存在并可达。

撤销示例：

```text
interface Vlanif 12
 undo ospfv3 1 area 0.0.0.0
ospfv3 1
 area 0.0.0.1
  undo abr-summary 2001:db8:: 32
  undo nssa
undo ospfv3 1
commit
```

### 双节点 OSPFv3 发布 IPv6 环回

R1 和 R2 以 Ethernet0 直连，分别使用 2001:db8:12::1/64 和 ::2/64。两端在同一区域发布不同的 IPv6 环回。

两台设备分别在系统视图录入各自的配置片段，退出功能视图后提交。

**R1**

```vortexros-config
ospfv3 1 router-id 198.51.100.1
 area 0.0.0.0
#
interface Ethernet 0
 ipv6 enable
 ipv6 address 2001:db8:12::1 64
 ospfv3 1 area 0.0.0.0
#
interface LoopBack 0
 ipv6 enable
 ipv6 address 2001:db8:1::1 128
 ospfv3 1 area 0.0.0.0
#
return
```

**R2**

```vortexros-config
ospfv3 1 router-id 198.51.100.2
 area 0.0.0.0
#
interface Ethernet 0
 ipv6 enable
 ipv6 address 2001:db8:12::2 64
 ospfv3 1 area 0.0.0.0
#
interface LoopBack 0
 ipv6 enable
 ipv6 address 2001:db8:2::1 128
 ospfv3 1 area 0.0.0.0
#
return
```

分别查看状态。

```vortexros-cli
display ospfv3 1 peer brief
display ospfv3 1 routing
display ipv6 routing-table
```

两端均看到对方 Router ID，邻接为 Full。R1 应学到 2001:db8:2::1/128，下一跳通常为对端链路本地地址。用 IPv6 ping 验证远端环回。

## 验证配置

```vortexros-cli
display ospfv3 peer
display ospfv3 routing
display ipv6 routing-table
```

确认邻接建立、远端 IPv6 前缀可见并在相应实例中从端点完成测试。
