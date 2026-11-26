# IPv6 路由通告与 SLAAC

## 功能介绍

主机可从 RA 学习 IPv6 前缀和默认路由。VortexROS 可在上联接收 RA，也可在下游三层接口发布 RA。

## 配置准备

确认上游在指定链路提供路由通告。独立使用 DHCPv6 时，仍需为默认路由准备 RA 或静态路由。

## 配置案例

```vortexros-config
interface Ethernet 1
 ipv6 address auto global default
#
return
```

提交后，等待地址生成和重复地址检测完成。若只需其中一项，分别使用 `ipv6 address auto slaac` 或 `ipv6 nd ra default-route enable`。用 `undo ipv6 address auto global default` 撤销组合配置。

### 向下游发布 IPv6 前缀

下例由 Ethernet2 向直连终端发布 2001:db8:20::/64。替换为实际下游接口和前缀后录入，再提交。

```vortexros-config
interface Ethernet 2
 ipv6 enable
 ipv6 address 2001:db8:20::1 64
 undo ipv6 nd ra halt
 ipv6 nd ra lifetime 1800
 ipv6 nd ra prefix 2001:db8:20:: 64 3600 1800
#
return
```

## 验证配置

```vortexros-cli
display ipv6 interface brief
display ipv6 neighbors
display ipv6 routing-table
```

确认地址与通告前缀匹配，默认路由指向上游路由器的链路本地地址。撤销后检查对应自动学习的地址和路由已消失。

如果设备在发出 RA，从下游主机检查自动生成的 IPv6 地址和默认路由，并测试网关连通。
