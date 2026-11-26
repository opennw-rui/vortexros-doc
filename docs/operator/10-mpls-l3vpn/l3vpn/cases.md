---
nav_title: 配置案例
nav_overview: 案例索引
---


# MPLS L3VPN、VPNv4 与 VPNv6 配置案例

(case-conditions-10-mpls-l3vpn-l3vpn)=
## 配置条件

预先建立 PE 之间的 MPLS/LDP 与 MP-BGP 会话，准备客户接口、独立 RD 及两端匹配的 RT。

```{toctree}
:maxdepth: 1

cases/example-1
cases/example-2
cases/example-3
```

(case-verification-10-mpls-l3vpn-l3vpn)=
## 通用验证

```vortexros-cli
display bgp vpnv4 vpn-instance BLUE routing-table
display bgp vpnv6 vpn-instance BLUE routing-table
display ip routing-table vpn-instance BLUE
display ipv6 routing-table vpn-instance BLUE
display mpls forwarding-table
```

在 PE 核对远端 VPN 前缀及标签路径。从两端客户设备分别测试 IPv4 与 IPv6 的双向转发。
