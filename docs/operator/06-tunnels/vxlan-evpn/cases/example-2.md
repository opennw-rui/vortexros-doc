---
nav_title: 两个 VTEP 的高位 BD 与动态学习
---


# 两个 VTEP 的高位 BD 与动态学习

## 拓扑

![左端站点 → R1 VTEP，BD 65536 → R2 VTEP，BD 65536 → 右端站点](example-2.svg)

## 配置条件

先配置两端底层接口、BGP EVPN 邻居和 VTEP 源。两个站点的 VNI 与 RT 相同，RD 分别配置。

R1、R2 的 Ethernet0 作为底层相连，使用 192.0.2.1 和 .2。两个客户终端接到两端 Ethernet1，地址为 203.0.113.11/24 和 .12/24。两端同用高位 BD 65536 和 VNI 65010，并选不同 RD。

## 配置步骤

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

## 验证方法

对照以下命令和预期结果核对设备状态。

```vortexros-cli
display bgp evpn all routing-table
display vxlan tunnel
display bridge-domain 65536
display mac-address bridge-domain 65536
```

对端 VTEP 应动态出现。终端收发后可在 EVPN 表看到 Type-3 和站点 MAC 对应的 Type-2。两个终端应互通。撤销 R2 的 NVE 下 VNI 65010 动态对等项后，应看到远端路径撤销，本地网段配置仍保留。重新添加可恢复。
