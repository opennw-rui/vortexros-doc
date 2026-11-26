# BGP EVPN 与动态 VXLAN

## 功能介绍

EVPN 通过 BGP 发布二层业务的远端信息，适用于无需逐个填写 VTEP 地址的 VXLAN 网络。

## 功能特性

EVPN Type-3 让同一 VNI 的 VTEP 发现彼此。Type-2 通告客户 MAC，携带 IP 时还可用于 ARP/ND 抑制。高位 BD 使用独立域编号，可和普通 VLAN 并行运行。

## 配置案例

先建立 VTEP 底层连通和 BGP EVPN 邻居。两端 VNI 与业务 RT 必须一致，RD 按设备分别指定。示例使用 VNI 65010。

```vortexros-config
evpn-overlay enable
#
bgp 65000
 router-id 192.0.2.1
 peer 192.0.2.2 as-number 65000
 l2vpn-family evpn
  peer 192.0.2.2 enable
#
bridge-domain 65536
 vxlan vni 65010
 evpn
  route-distinguisher 65000:1101
  vpn-target 65000:65010 import-extcommunity
  vpn-target 65000:65010 export-extcommunity
#
interface Nve 1
 source 192.0.2.1
 vni 65010 head-end peer-list protocol bgp
#
return
```

在两端分别录入配置并提交。对端 NVE 使用自己的源地址，RD 使用 65000:1102。将各自业务口关联到桥域。

### 两个 VTEP 的高位 BD 与动态学习

R1、R2 的 Ethernet0 作为底层相连，使用 192.0.2.1 和 .2。两个客户终端接到两端 Ethernet1，地址为 203.0.113.11/24 和 .12/24。两端同用高位 BD 65536 和 VNI 65010，并选不同 RD。

两台设备分别在系统视图录入各自的配置片段，退出功能视图后提交。

**R1**

```vortexros-config
interface Ethernet 0
 ip address 192.0.2.1 255.255.255.0
#
evpn-overlay enable
#
bgp 65000
 router-id 192.0.2.1
 peer 192.0.2.2 as-number 65000
 l2vpn-family evpn
  peer 192.0.2.2 enable
#
bridge-domain 65536
 vxlan vni 65010
 evpn
  route-distinguisher 65000:1101
  vpn-target 65000:65010 import-extcommunity
  vpn-target 65000:65010 export-extcommunity
#
interface Ethernet 1
 bridge-domain 65536
#
interface Nve 1
 source 192.0.2.1
 vni 65010 head-end peer-list protocol bgp
#
return
```

**R2**

```vortexros-config
interface Ethernet 0
 ip address 192.0.2.2 255.255.255.0
#
evpn-overlay enable
#
bgp 65000
 router-id 192.0.2.2
 peer 192.0.2.1 as-number 65000
 l2vpn-family evpn
  peer 192.0.2.1 enable
#
bridge-domain 65536
 vxlan vni 65010
 evpn
  route-distinguisher 65000:1102
  vpn-target 65000:65010 import-extcommunity
  vpn-target 65000:65010 export-extcommunity
#
interface Ethernet 1
 bridge-domain 65536
#
interface Nve 1
 source 192.0.2.2
 vni 65010 head-end peer-list protocol bgp
#
return
```

分别查看状态。

```vortexros-cli
display bgp evpn all routing-table
display vxlan tunnel
display bridge-domain 65536
display mac-address bridge-domain 65536
```

对端 VTEP 应动态出现。终端收发后可在 EVPN 表看到 Type-3 和站点 MAC 对应的 Type-2。两个终端应互通。撤销 R2 的 NVE 下 VNI 65010 动态对等项后，应看到远端路径撤销，本地网段配置仍保留。重新添加可恢复。

### 高位域隔离、组播订阅与 MAC/IP 迁移

在双端高位 BD 案例上增加第二个业务域。两端复用同一 VTEP 源，Ethernet1 保留原高位域，Ethernet2 加入 BD 65537。如果需要观察订阅只选择一个远端，可增加第三个 VTEP，并在它上面复用相同配置、不同 RD 和本地 VTEP 地址。

```vortexros-config
evpn-overlay enable
#
bgp 65000
 router-id 192.0.2.1
 peer 192.0.2.2 as-number 65000
 l2vpn-family evpn
  peer 192.0.2.2 enable
#
bridge-domain 65537
 vxlan vni 65020
 evpn
  route-distinguisher 65000:1201
  vpn-target 65000:65020 export-extcommunity
  vpn-target 65000:65020 import-extcommunity
#
interface Ethernet 2
 bridge-domain 65537
#
interface Nve 1
 source 192.0.2.1
 vni 65020 head-end peer-list protocol bgp
#
return
```

这是 R1 增量，保留当前 VNI 65010。R2 使用相同的业务接口、BD、VNI 和 RT，RD 改成 65000:1202。R2 沿用原双端案例的 Router ID、对端地址和 NVE 源地址。两端分别录入并提交。

```vortexros-cli
display bridge-domain 65536
display bridge-domain 65537
display bgp evpn all routing-table mac-route
display mac-address bridge-domain 65536
display mac-address bridge-domain 65537
```

1. 分别为两域配置测试终端，可以复用相同 IPv4/IPv6 和 MAC。每域的同域端点应互通，另一域的接入口不应收到报文。
2. 从某域两端生成 IPv4 ARP 和 IPv6 NS。首先确认远端 MAC/IP 通告已出现。发往已知端点的请求可由本地抑制处理，未知请求继续在本域内转发。
3. 迁移同一终端至同域另一台 PE，检查 Type-2 的下一跳改为新位置，旧出口撤销。另一 BD 的同名表项保持可用。
4. 测试组播时，在该域提供 IGMP 或 MLD 查询器，让接收端加入组后查看各端实际收包。存在有效查询器时只应转发至有订阅的成员及需要的组播路由器端口。取消订阅并等待相应组状态到期，再核对不再向该接入口复制报文。两个高位域可使用相同组地址。

[高位 Bridge Domain](../03-interfaces-l2/bridge-domain.md) · [BGP](../05-dynamic-routing/bgp.md)

## 验证配置

```vortexros-cli
display bgp peer
display bridge-domain 65536
display vxlan tunnel
display mac-address
```

先确认 BGP 邻居已建立，再检查远端 VTEP 和 MAC。移动终端后，确认旧位置的表项撤销且新位置学习正常。
