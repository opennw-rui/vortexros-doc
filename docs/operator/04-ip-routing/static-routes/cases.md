---
nav_title: 配置案例
nav_overview: 案例索引
---


# IPv4 与 IPv6 静态路由 配置案例

(case-conditions-04-ip-routing-static-routes)=
## 配置条件

确认下一跳在正确的路由表内可达。使用跨 VPN 下一跳时先创建相应 VPN。

```{toctree}
:maxdepth: 1

cases/example-1
cases/example-2
```

(case-verification-04-ip-routing-static-routes)=
## 通用验证

```vortexros-cli
display ip routing-table protocol static
display ip routing-table vpn-instance BLUE
display ipv6 routing-table protocol static
display ip fib
display ipv6 fib
```

检查优选路由的目的前缀、下一跳和出接口。DPDK 数据面还可查看 FIB。存在多条等价路径时，核对每条有效路径并验证实际转发。
