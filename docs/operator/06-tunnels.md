# 隧道与覆盖网络

- [GRE 隧道](06-tunnels/gre.md)。GRE 用于在可达的三层网络上承载另一条三层逻辑链路。隧道本身不提供加密。
- [IP-in-IP 隧道](06-tunnels/ip-in-ip.md)。IP-in-IP 用 IP 包封装另一个 IP 包，连接跨底层网络的三层网段。按需搭配 IPv4 或 IPv6 内外层。
- [静态 VXLAN 与 NVE](06-tunnels/vxlan-static.md)。VXLAN 在 IP 网络上延伸二层业务。静态模式从 NVE 手动指定远端 VTEP，适用于远端固定的部署。
- [BGP EVPN 与动态 VXLAN](06-tunnels/vxlan-evpn.md)。EVPN 通过 BGP 发布二层业务的远端信息，适用于无需逐个填写 VTEP 地址的 VXLAN 网络。
- [WireGuard 隧道](06-tunnels/wireguard.md)。WireGuard 用于在站点或终端之间建立加密三层连接。可按对端指定公钥、网络前缀和远端地址。
- [AmneziaWG 隧道](06-tunnels/amneziawg.md)。AmneziaWG 为站点间提供加密隧道及可配置的握手与报文格式。可以与 WireGuard 并行配置。

```{toctree}
:maxdepth: 1
:hidden:

06-tunnels/gre
06-tunnels/ip-in-ip
06-tunnels/vxlan-static
06-tunnels/vxlan-evpn
06-tunnels/wireguard
06-tunnels/amneziawg
```
