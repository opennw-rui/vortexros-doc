# MPLS L3VPN、VPNv4 与 VPNv6

## 功能介绍

L3VPN 在 MPLS 核心中承载相互隔离的客户路由。IPv6 客户流量可以通过 IPv4 的 MPLS 核心传输。

## 配置准备

预先建立 PE 之间的 MPLS/LDP 与 MP-BGP 会话，准备客户接口、独立 RD 及两端匹配的 RT。

## 配置案例

```vortexros-config
ip vpn-instance BLUE
 ipv4-family
  route-distinguisher 65000:100
  vpn-target 65000:100 both
 ipv6-family
  route-distinguisher 65000:100
  vpn-target 65000:100 both
#
interface Ethernet 1
 ip binding vpn-instance BLUE
 ip address 192.0.2.1 255.255.255.0
 ipv6 address 2001:db8:100::1 64
#
return
```

在各 PE 绑定客户接口后提交。配置 PE–CE 路由和 MP-BGP 地址族，两端 RD 按各自规划设置。撤销时先停止发布并确认远端路由撤销，再解除客户接口绑定。

### IPv4 核心同时承载 VPNv4 和 VPNv6

CE1 — PE1 Ethernet1 — IPv4 MPLS 核心 — PE2 Ethernet1 — CE2。复用 [两端 LDP](ldp.md) 的 Ethernet0 与两台 PE 的 IPv4 环回，核心口保留 ipv6 enable，仅用 IPv4 IGP 和 LDP。CE1 用 203.0.113.2/25 与 2001:db8:1::2/64。CE2 用 203.0.113.130/25 与 2001:db8:2::2/64。默认网关为各自 PE 的客户侧 IPv4 和 IPv6 地址。

**本端设备**

```vortexros-config
interface LoopBack 0
 ip address 198.51.100.1 255.255.255.255
#
ip vpn-instance BLUE
 ipv4-family
  route-distinguisher 65000:101
  vpn-target 65000:100 both
 #
 ipv6-family
  route-distinguisher 65000:201
  vpn-target 65000:100 both
#
interface Ethernet 1
 ip binding vpn-instance BLUE
 ip address 203.0.113.1 255.255.255.128
 ipv6 enable
 ipv6 address 2001:db8:1::1 64
#
bgp 65000
 router-id 198.51.100.1
 peer 198.51.100.2 as-number 65000
 peer 198.51.100.2 connect-interface LoopBack0
 ipv4-family vpnv4
  peer 198.51.100.2 enable
 #
 ipv6-family vpnv6
  peer 198.51.100.2 enable
 #
 ipv4-family vpn-instance BLUE
  import-route direct
 #
 ipv6-family vpn-instance BLUE
  import-route direct
#
return
```

**对端设备**

```vortexros-config
interface LoopBack 0
 ip address 198.51.100.2 255.255.255.255
#
ip vpn-instance BLUE
 ipv4-family
  route-distinguisher 65000:102
  vpn-target 65000:100 both
 #
 ipv6-family
  route-distinguisher 65000:202
  vpn-target 65000:100 both
#
interface Ethernet 1
 ip binding vpn-instance BLUE
 ip address 203.0.113.129 255.255.255.128
 ipv6 enable
 ipv6 address 2001:db8:2::1 64
#
bgp 65000
 router-id 198.51.100.2
 peer 198.51.100.1 as-number 65000
 peer 198.51.100.1 connect-interface LoopBack0
 ipv4-family vpnv4
  peer 198.51.100.1 enable
 #
 ipv6-family vpnv6
  peer 198.51.100.1 enable
 #
 ipv4-family vpn-instance BLUE
  import-route direct
 #
 ipv6-family vpn-instance BLUE
  import-route direct
#
return
```

```vortexros-cli
display bgp vpnv4 all
display bgp vpnv6 all
display ip routing-table vpn-instance BLUE
display ipv6 routing-table vpn-instance BLUE
display mpls forwarding-table
```

PE1 应在 BLUE 看到 PE2 的 203.0.113.128/25 和 2001:db8:2::/64，VPNv6 下一跳为 IPv4 映射地址。PE2 应看到反向前缀。CE 两端互 ping，默认路由表中不应学习这些 VPN 前缀。

### 增加备用核心链路并验证切换

在已有 VPNv4/VPNv6 的两端 LDP 案例上，将两台 PE 的 Ethernet2 额外互联。主链路仍使用 Ethernet0，备用用 192.0.2.4/30，OSPF 成本设为 1000。两台设备分别录入增量后提交。独立四节点核心同理，可用现有 IGP 及 LDP 协议逐段确认。

**PE1**

```vortexros-config
mpls lsr-id 198.51.100.1
mpls
#
mpls ldp
#
interface Ethernet 2
 ip address 192.0.2.5 255.255.255.252
 ipv6 enable
 mpls
 mpls ldp
 ospf network-type p2p
 ospf cost 1000
#
ospf 1
 area 0.0.0.0
  network 192.0.2.5 0.0.0.0
#
return
```

**PE2**

```vortexros-config
mpls lsr-id 198.51.100.2
mpls
#
mpls ldp
#
interface Ethernet 2
 ip address 192.0.2.6 255.255.255.252
 ipv6 enable
 mpls
 mpls ldp
 ospf network-type p2p
 ospf cost 1000
#
ospf 1
 area 0.0.0.0
  network 192.0.2.6 0.0.0.0
#
return
```

```vortexros-cli
display ospf 1 interface
display mpls ldp interface
display mpls forwarding-table
display ip routing-table protocol ospf
```

两端先检查备用口启用 MPLS/LDP，远端 PE 环回仍优选主链路。断开 Ethernet0，远端环回与标签转发路径应改经 Ethernet2，CE 间双栈通信应在收敛后恢复。重新接回 Ethernet0，确认主路径恢复。完成后可移除备用接口在 OSPF 的 network 项及接口上的 LDP、MPLS 和测试地址。

[VPN 实例](../04-ip-routing/vpn-instance.md) · [BGP 与 MP-BGP](../05-dynamic-routing/bgp.md)

## 验证配置

```vortexros-cli
display bgp vpnv4 vpn-instance BLUE routing-table
display bgp vpnv6 vpn-instance BLUE routing-table
display ip routing-table vpn-instance BLUE
display ipv6 routing-table vpn-instance BLUE
display mpls forwarding-table
```

在 PE 核对远端 VPN 前缀及标签路径。从两端客户设备分别测试 IPv4 与 IPv6 的双向转发。
