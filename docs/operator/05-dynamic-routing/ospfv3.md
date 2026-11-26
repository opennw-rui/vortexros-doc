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

`peer brief`中的邻居状态来自FRR OSPFv3运行态，`routing`中的路由数量只统计协议为`ospf6`的IPv6路由。配置已提交但尚未形成邻接时不会伪造Full状态；验收时应同时确认邻居Full、IPv6路由存在和业务地址可达。

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

## 验证配置

```vortexros-cli
display ospfv3 peer
display ospfv3 routing
display ipv6 routing-table
```

确认邻接建立、远端 IPv6 前缀可见并在相应实例中从端点完成测试。
