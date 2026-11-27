# 组网与验证案例索引

按要部署的业务选取案例。每个案例给出配置条件、可执行命令和检查项。部分功能页另附不同组网的实测节选，执行时应按所选拓扑核对设备、接口和地址。

## 常用组网

| 要验证的业务 | 拓扑与案例 | 实测检查项 |
| --- | --- | --- |
| 安装后启动 | [单机首次启动](../../installation/06-first-start.md) · [健康状态](service-health.md) | 读取启动版本和所选配置，健康状态为 `ready`，活动告警为 0。 |
| 动态路由和保存配置恢复 | [三节点 OSPF](../05-dynamic-routing/ospf.md) · [运行配置重置与恢复](operational-reset.md) | 复查两侧路由邻接和 VPN 路由，确认同一启动配置仍可加载并恢复业务。 |
| BFD 与双栈 VRRP | [路由邻接故障检测](../05-dynamic-routing/bfd.md) · [Vlanif 双栈网关](../05-dynamic-routing/vrrp.md) | 分别核对 BFD `Up`、VRRP `Master/Backup` 和虚拟地址可达。 |
| 双栈单播 VRRP | [双机同广播域单播选举](../05-dynamic-routing/vrrp/cases/dual-stack-vrrp-unicast.md) | 两端交换双栈单播通告，切换和恢复后从客户端探测虚拟网关。 |
| DHCPv4/v6 直连与中继 | [IPv4 直连](../08-network-services/dhcpv4-server/cases/example-2.md) · [IPv4 中继](../08-network-services/dhcpv4-relay.md) · [IPv6 三节点中继](../08-network-services/dhcpv6-relay/cases/example-2.md) | 客户端取得对应链路的租约，检查服务端、中继和客户端的状态。 |
| VPN 内 DHCPv4 | [实例内分配固定租约](../08-network-services/dhcpv4-server/cases/vpn-static-lease.md) | 在 VPN 实例 `ALL` 下取得 `10.253.10.105/24`，确认回显的实例列。 |
| QoS 限速与恢复 | [二层成员口和 Vlanif 限速](../07-policy/interface-qos.md) · [VPP 恢复后的接口复查](operational-reset/cases/example-2.md) | 限速生效，撤销后释放，恢复配置后重新生效。 |
| EVPN All-Active 多归属 | [两台本地 PE 与一台远端 PE](../06-tunnels/evpn-multihoming.md) | 检查 Ethernet Segment、DF 角色、成员故障和业务恢复。 |
| EVPN 两个二层 VNI | [双站点 EVPN 二层与网关](../06-tunnels/vxlan-evpn/cases/two-bridge-domains.md) | 独立学习 MAC/IP，撤销一个 VNI 时另一业务域保持可达。 |
| IPv4 MPLS 骨干 | [四节点 6PE 与 6VPE 环网](../10-mpls-l3vpn/l3vpn/cases/ipv4-core-ring.md) | 骨干口保持关闭 IPv6，在主路、备路和主路恢复后三个阶段验证双向 IPv6。 |
| 出站 NAT | [单边界路由器出站 PAT](../07-policy/nat/cases/outbound-pat.md) · [静态发布及回流](../07-policy/nat/cases/example-1.md) | 分别核对命中规则、转换会话和远端收到的源地址。 |
| 高位 Bridge Domain | [高位 BD 动态 EVPN](../03-interfaces-l2/bridge-domain/cases/example-2.md) | 不同 BD 内同地址设备各自通信，验证迁移、撤销以及两域隔离。 |

## 同一网络中的其他组合

| 组合 | 案例 | 实测检查项 |
| --- | --- | --- |
| 二层接入和聚合 | [VLAN access、trunk 与 hybrid](../03-interfaces-l2/vlan.md) | 混合端口验证标记帧与未标记帧。故障排查按 VLAN 和端口核对实际学习。 |
| 外部静态路由组 | [文件或 HTTPS 发布路由组](../04-ip-routing/static-route-groups.md) | 源文件更新后查询两族安装结果，撤销后检查原路由的移除。 |
| IPv6 IGP 与 BFD | [OSPFv3](../05-dynamic-routing/ospfv3.md) · [BFD](../05-dynamic-routing/bfd.md) | BFD 会话关闭时保持物理链路在线，核对备路和故障恢复。 |
| 隧道转发 | [GRE](../06-tunnels/gre.md) · [IP-in-IP 的四种地址族组合](../06-tunnels/ip-in-ip.md) · [WireGuard](../06-tunnels/wireguard.md) · [AmneziaWG](../06-tunnels/amneziawg.md) | 通过两端接口和业务探测核对内外层地址族、实际出接口及 MTU。 |
| 流量分类与导向 | [ACL](../07-policy/acl.md) · [MQC](../07-policy/mqc.md) | 对比匹配和不匹配流量，核对命中计数、转发方向及撤销后的行为。 |
