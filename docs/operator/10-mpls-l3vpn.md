# MPLS 与 L3VPN

- [MPLS 核心转发](10-mpls-l3vpn/mpls.md)。MPLS 通过标签转发报文，为 L3VPN 等业务提供核心传输。核心设备需能到达对端的稳定标识地址。
- [LDP 标签分发](10-mpls-l3vpn/ldp.md)。LDP 在 MPLS 核心的邻居之间交换标签绑定，供目的前缀建立标签转发路径。
- [MPLS L3VPN、VPNv4 与 VPNv6](10-mpls-l3vpn/l3vpn.md)。L3VPN 在 MPLS 核心中承载相互隔离的客户路由。IPv6 客户流量可以通过 IPv4 的 MPLS 核心传输。

```{toctree}
:maxdepth: 1
:hidden:

10-mpls-l3vpn/mpls
10-mpls-l3vpn/ldp
10-mpls-l3vpn/l3vpn
```
