# IP 接入与静态路由

- [IPv6 路径 MTU](04-ip-routing/ipv6-path-mtu.md)。找出到远端目的地址的报文大小限制。
- [IPv4 与 IPv6 接口地址](04-ip-routing/ip-addresses.md)。在三层接口配置 IPv4 或 IPv6 地址后，设备可以连接对应网段。同一 IPv4 接口可以有主地址和从地址，IPv6 地址逐条添加。
- [VPN 实例与路由隔离](04-ip-routing/vpn-instance.md)。VPN 实例提供独立的路由表。在一台设备上可隔离不同租户的三层接口与路由，共用的设备可以承载重叠的地址规划。
- [IPv4 与 IPv6 静态路由](04-ip-routing/static-routes.md)。静态路由把指定目的前缀交给固定的下一跳或出接口，适用于默认出口、固定对端或备用路径。
- [静态路由组](04-ip-routing/static-route-groups.md)。用一个可维护的前缀清单管理具有相同下一跳和属性的多条静态路由。可录入手工成员，也可从文件或 URL 读取。
- [uRPF 反向路径检查](04-ip-routing/urpf.md)。uRPF 用源地址的路由检查入站流量，适用于限制来源与网络拓扑不符的报文。
- [IPv6 路由通告与 SLAAC](04-ip-routing/ipv6-router-advertisement.md)。主机可从 RA 学习 IPv6 前缀和默认路由。VortexROS 可在指定的三层接口使用 SLAAC 生成地址并接收 RA 默认路由。

```{toctree}
:maxdepth: 1
:hidden:

04-ip-routing/ipv6-path-mtu
04-ip-routing/ip-addresses
04-ip-routing/vpn-instance
04-ip-routing/static-routes
04-ip-routing/static-route-groups
04-ip-routing/urpf
04-ip-routing/ipv6-router-advertisement
```
