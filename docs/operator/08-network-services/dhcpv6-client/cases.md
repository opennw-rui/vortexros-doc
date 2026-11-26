---
nav_title: 配置案例
nav_overview: 案例索引
---


# DHCPv6 客户端与前缀委派 配置案例

(case-conditions-08-network-services-dhcpv6-client)=
## 配置条件

确认上游支持有状态地址分配或前缀委派。如果还需要默认路由，请准备 RA。

```{toctree}
:maxdepth: 1

cases/example-1
cases/example-2
```

(case-verification-08-network-services-dhcpv6-client)=
## 通用验证

```vortexros-cli
display dhcpv6 client interface Ethernet 1
display dhcpv6 client prefix name CPE-PREFIX
display ipv6 interface brief
```

分别确认接口地址与委派前缀。需要对外通信时再检查 IPv6 默认路由。

[IPv6 路由通告与 SLAAC](../../04-ip-routing/ipv6-router-advertisement.md)
