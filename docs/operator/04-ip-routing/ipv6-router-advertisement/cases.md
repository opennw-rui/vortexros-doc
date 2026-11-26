---
nav_title: 配置案例
nav_overview: 案例索引
---


# IPv6 路由通告与 SLAAC 配置案例

(case-conditions-04-ip-routing-ipv6-router-advertisement)=
## 配置条件

确认上游在指定链路提供路由通告。独立使用 DHCPv6 时，仍需为默认路由准备 RA 或静态路由。

```{toctree}
:maxdepth: 1

cases/example-1
cases/example-2
```

(case-verification-04-ip-routing-ipv6-router-advertisement)=
## 通用验证

```vortexros-cli
display ipv6 interface brief
display ipv6 neighbors
display ipv6 routing-table
```

确认地址与通告前缀匹配，默认路由指向上游路由器的链路本地地址。撤销后检查对应自动学习的地址和路由已消失。

如果设备在发出 RA，从下游主机检查自动生成的 IPv6 地址和默认路由，并测试网关连通。
