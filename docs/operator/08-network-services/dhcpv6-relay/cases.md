---
nav_title: 配置案例
nav_overview: 案例索引
---


# DHCPv6 中继 配置案例

(case-conditions-08-network-services-dhcpv6-relay)=
## 配置条件

在客户端所在的三层接口配置中继，确认目标服务器可达并为接入链路准备 IPv6 地址池。

```{toctree}
:maxdepth: 1

cases/example-1
cases/example-2
```

(case-verification-08-network-services-dhcpv6-relay)=
## 通用验证

```vortexros-cli
display dhcpv6 relay
display ipv6 routing-table
```

核对中继接口与目标地址，用接入客户端实际请求租约并检查服务器返回的地址或前缀。
