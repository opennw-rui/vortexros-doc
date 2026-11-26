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

## 验证配置

```vortexros-cli
display bgp vpnv4 vpn-instance BLUE routing-table
display bgp vpnv6 vpn-instance BLUE routing-table
display ip routing-table vpn-instance BLUE
display ipv6 routing-table vpn-instance BLUE
display mpls forwarding-table
```

在 PE 核对远端 VPN 前缀及标签路径。从两端客户设备分别测试 IPv4 与 IPv6 的双向转发。

[VPN 实例](../04-ip-routing/vpn-instance.md) · [BGP 与 MP-BGP](../05-dynamic-routing/bgp.md)
