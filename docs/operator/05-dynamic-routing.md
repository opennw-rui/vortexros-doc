# 动态路由与高可用

- [前缀列表与路由策略](05-dynamic-routing/route-policy.md)。用前缀列表筛选路由，用路由策略决定接收、发布或调整属性。策略可复用于多个邻居。
- [OSPF（IPv4）](05-dynamic-routing/ospf.md)。OSPF 为 IPv4 域内路由交换链路状态，可用多区域组织网络。
- [OSPFv3（IPv6）](05-dynamic-routing/ospfv3.md)。OSPFv3 为 IPv6 域内业务学习路由，在指定链路的三层接口建立邻居。
- [BGP 与 MP-BGP](05-dynamic-routing/bgp.md)。BGP 用于 AS 间和 AS 内的路由交换。按地址族激活邻居，可处理 IPv4、IPv6 和 VPN 路由。
- [IS-IS](05-dynamic-routing/isis.md)。IS-IS 通过交换链路状态建立 IPv4 或 IPv6 域内路由，可按 Level-1、Level-2 划分邻接范围。
- [BFD 快速故障检测](05-dynamic-routing/bfd.md)。BFD 快速检测两个转发端点之间的可达性。可独立建立会话，也可配合动态路由协议加速故障收敛。
- [VRRP 与 VRRP6 网关冗余](05-dynamic-routing/vrrp.md)。VRRP 让多台设备共用虚拟网关，适用于接入网段的网关冗余。IPv4 默认 VRRPv2，IPv6 使用 VRRPv3。
- [RIP（IPv4）](05-dynamic-routing/rip.md)。RIP 根据跳数交换 IPv4 路由，适用于已有 RIP 设备的小型网络。
- [RIPng（IPv6）](05-dynamic-routing/ripng.md)。RIPng 根据跳数交换 IPv6 路由。可在指定三层接口接收和发送路由更新。

```{toctree}
:maxdepth: 1
:hidden:

05-dynamic-routing/route-policy
05-dynamic-routing/ospf
05-dynamic-routing/ospfv3
05-dynamic-routing/bgp
05-dynamic-routing/isis
05-dynamic-routing/bfd
05-dynamic-routing/vrrp
05-dynamic-routing/rip
05-dynamic-routing/ripng
```
