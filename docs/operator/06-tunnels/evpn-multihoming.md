# EVPN All-Active 多归属

## 功能介绍

All-Active 允许一个客户以太网段同时通过两台 PE 转发。

## 配置准备

三台 PE 通过 Ethernet0 接同一个 IPv4 底层网段 192.0.2.0/24，建立全互联 EVPN 邻居。CE1 用静态双活聚合，一端接 PE1 的 Ethernet1，另一端接 PE2 的 Ethernet1。CE2 接 PE3 的 Ethernet1。两个客户位于同一 VLAN 和网段。

## 配置案例

分别录入以下配置并提交。PE1、PE2 使用相同 ESI。PE3 用普通接入口。

**PE1**

```vortexros-config
interface Ethernet 0
 ip address 192.0.2.1 255.255.255.0
#
enable switch
#
vlan 101
#
evpn-overlay enable
#
bridge-domain 101
 l2 binding vlan 101
 vxlan vni 5010
 evpn
  route-distinguisher 65000:101
  vpn-target 65000:5010 export-extcommunity
  vpn-target 65000:5010 import-extcommunity
#
interface Nve 1
 source 192.0.2.1
 vni 5010 head-end peer-list protocol bgp
#
interface Eth-Trunk 1
 mode manual
 trunkport Ethernet 1
 portswitch
 port link-type trunk
 port trunk allow-pass vlan 101
 port trunk pvid vlan 101
 esi 0000.0000.0000.0000.0001
#
bgp 65000
 router-id 192.0.2.1
 peer 192.0.2.2 as-number 65000
 peer 192.0.2.3 as-number 65000
 l2vpn-family evpn
  peer 192.0.2.2 enable
  peer 192.0.2.3 enable
#
return
```

**PE2**

```vortexros-config
interface Ethernet 0
 ip address 192.0.2.2 255.255.255.0
#
enable switch
#
vlan 101
#
evpn-overlay enable
#
bridge-domain 101
 l2 binding vlan 101
 vxlan vni 5010
 evpn
  route-distinguisher 65000:201
  vpn-target 65000:5010 export-extcommunity
  vpn-target 65000:5010 import-extcommunity
#
interface Nve 1
 source 192.0.2.2
 vni 5010 head-end peer-list protocol bgp
#
interface Eth-Trunk 1
 mode manual
 trunkport Ethernet 1
 portswitch
 port link-type trunk
 port trunk allow-pass vlan 101
 port trunk pvid vlan 101
 esi 0000.0000.0000.0000.0001
#
bgp 65000
 router-id 192.0.2.2
 peer 192.0.2.1 as-number 65000
 peer 192.0.2.3 as-number 65000
 l2vpn-family evpn
  peer 192.0.2.1 enable
  peer 192.0.2.3 enable
#
return
```

**PE3**

```vortexros-config
interface Ethernet 0
 ip address 192.0.2.3 255.255.255.0
#
enable switch
#
vlan 101
#
evpn-overlay enable
#
bridge-domain 101
 l2 binding vlan 101
 vxlan vni 5010
 evpn
  route-distinguisher 65000:301
  vpn-target 65000:5010 export-extcommunity
  vpn-target 65000:5010 import-extcommunity
#
interface Nve 1
 source 192.0.2.3
 vni 5010 head-end peer-list protocol bgp
#
interface Ethernet 1
 portswitch
 port link-type access
 port default vlan 101
#
bgp 65000
 router-id 192.0.2.3
 peer 192.0.2.1 as-number 65000
 peer 192.0.2.2 as-number 65000
 l2vpn-family evpn
  peer 192.0.2.1 enable
  peer 192.0.2.2 enable
#
return
```

## 验证配置

```vortexros-cli
display bgp evpn peer
display bgp evpn ethernet-segment verbose
display bgp evpn all routing-table ad-route
display bgp evpn all routing-table es-route
display mac-address
```

PE1 和 PE2 应看到同一 Ethernet Segment，其中一台为 DF。PE3 应收到两台的 Ethernet A-D 和 Ethernet Segment 路径。CE1 与 CE2 应互通。关闭 PE1 的客户成员后重新查询，PE3 应保留 PE2 路径并继续转发；恢复成员后确认双路径恢复。
