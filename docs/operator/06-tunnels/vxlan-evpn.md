# BGP EVPN 与动态 VXLAN

## 功能介绍

EVPN 通过 BGP 发布二层业务的远端信息，适用于无需逐个填写 VTEP 地址的 VXLAN 网络。

## 配置准备

先建立 VTEP 底层连通和 BGP EVPN 邻居。两端 VNI 与业务 RT 必须一致，RD 按设备分别指定。示例使用 VNI 65010。

## 配置案例

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

## 验证配置

```vortexros-cli
display bgp peer
display bridge-domain 65536
display vxlan tunnel
display mac-address
```

先确认 BGP 邻居已建立，再检查远端 VTEP 和 MAC。移动终端后，确认旧位置的表项撤销且新位置学习正常。

[高位 Bridge Domain](../03-interfaces-l2/bridge-domain.md) · [BGP](../05-dynamic-routing/bgp.md)
