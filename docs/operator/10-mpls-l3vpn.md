# MPLS、LDP 与 L3VPN

## MPLS 与 LDP

在核心链路开通 IPv4 底层连通，使用稳定且全网唯一的 LSR ID，并在 IGP 中通告其主机地址。两端在核心三层接口启用 MPLS 和 LDP。以下示例使用一条核心链路。

```vortexros-config
#
sysname PE1
#
mpls lsr-id 192.0.2.1
mpls
#
mpls ldp
#
interface LoopBack0
 ip address 192.0.2.1 255.255.255.255
#
interface Ethernet0
 ip address 198.51.100.1 255.255.255.252
 mpls
 mpls ldp
 ospf network-type p2p
#
ospf 1 router-id 192.0.2.1
 area 0.0.0.0
  network 192.0.2.1 0.0.0.0
  network 198.51.100.1 0.0.0.0
#
return
```

对端使用同一链路的另一有效地址及独立的 LSR ID。提交后核对两端 IGP 路由，再核对 LDP 会话、标签绑定和实际转发表。

```vortexros-cli
display mpls interface
display mpls ldp interface
display mpls ldp peer
display mpls ldp binding
display mpls lsp
display mpls forwarding-table
```

## 接入 L3VPN

在 PE 建立 VPN 实例和地址族，配置区分符 RD 与导入、导出 Route Target。把客户三层接口绑定到相应 VPN，随后配置地址和 PE–CE 路由。在 PE 之间启用 MP-BGP 的 VPNv4 或 VPNv6 地址族，核对邻居、远端 VPN 路由和实际标签路径。

IPv6 客户业务与核心传输地址族分别核对。采用 IPv4 MPLS 核心时，也要对 VPNv6 实测双向转发。确认客户路由落入正确 VPN，避免只用控制面可见的路由判断业务。

撤销时先移除 VPN 路由发布并确认远端撤销，再解除客户接口绑定。只有核心标签传输无业务引用时，才撤销该链路的 LDP 与 MPLS。

[VPN 和静态路由](04-ip-routing.md) · [BGP 地址族](05-dynamic-routing.md) · [完整命令参考](reference/commands.md)
