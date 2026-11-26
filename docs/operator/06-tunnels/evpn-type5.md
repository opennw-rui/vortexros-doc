# EVPN Type-5 租户路由

## 功能介绍

EVPN Type-5 在 VTEP 之间通告租户的 IPv4 和 IPv6 前缀。

## 配置准备

PE1 与 PE2 的 Ethernet0 以 192.0.2.0/24 相连，均使用租户 BLUE 和 L3VNI 50000。两端 RT 相同、RD 各自唯一。

同一 PE 为一个 L3VNI 通告两个地址族时，IPv4 和 IPv6 的 RD 及导入、导出 RT 使用相同值。

## 配置案例

两端分别录入并提交。该案例使用环回前缀模拟各站点业务。

**PE1**

```vortexros-config
interface Ethernet 0
 ip address 192.0.2.1 255.255.255.0
#
evpn-overlay enable
#
ip vpn-instance BLUE
 vxlan vni 50000
 ipv4-family
  route-distinguisher 65000:50101
  vpn-target 65000:50000 both
 #
 ipv6-family
  route-distinguisher 65000:50101
  vpn-target 65000:50000 both
#
interface LoopBack 100
 ip binding vpn-instance BLUE
 ip address 198.51.100.1 255.255.255.255
 ipv6 enable
 ipv6 address 2001:db8:1::1 128
#
interface Nve 1
 source 192.0.2.1
#
bgp 65000
 router-id 192.0.2.1
 peer 192.0.2.2 as-number 65000
 l2vpn-family evpn
  peer 192.0.2.2 enable
 #
 ipv4-family vpn-instance BLUE
  import-route direct
  advertise l2vpn evpn
 #
 ipv6-family vpn-instance BLUE
  import-route direct
  advertise l2vpn evpn
#
return
```

**PE2**

```vortexros-config
interface Ethernet 0
 ip address 192.0.2.2 255.255.255.0
#
evpn-overlay enable
#
ip vpn-instance BLUE
 vxlan vni 50000
 ipv4-family
  route-distinguisher 65000:50201
  vpn-target 65000:50000 both
 #
 ipv6-family
  route-distinguisher 65000:50201
  vpn-target 65000:50000 both
#
interface LoopBack 100
 ip binding vpn-instance BLUE
 ip address 198.51.100.2 255.255.255.255
 ipv6 enable
 ipv6 address 2001:db8:2::1 128
#
interface Nve 1
 source 192.0.2.2
#
bgp 65000
 router-id 192.0.2.2
 peer 192.0.2.1 as-number 65000
 l2vpn-family evpn
  peer 192.0.2.1 enable
 #
 ipv4-family vpn-instance BLUE
  import-route direct
  advertise l2vpn evpn
 #
 ipv6-family vpn-instance BLUE
  import-route direct
  advertise l2vpn evpn
#
return
```

## 验证配置

```vortexros-cli
display bgp evpn peer
display bgp evpn all routing-table prefix-route
display ip routing-table vpn-instance BLUE
display ipv6 routing-table vpn-instance BLUE
```

EVPN 邻居应建立，远端 Type-5 的下一跳是对端 VTEP。PE1 的 BLUE 应有 198.51.100.2/32 与 2001:db8:2::1/128，PE2 应有反向前缀。从 BLUE 测试双栈连通。撤销 PE2 相应地址族的 `advertise l2vpn evpn` 并提交后，PE1 应撤掉该地址族的远端前缀。
