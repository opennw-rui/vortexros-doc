---
nav_title: 配置 VNI、桥域与 EVPN 对端
---


# 配置 VNI、桥域与 EVPN 对端

## 拓扑

![两台 VTEP 建立 EVPN 对等关系并延伸二层业务](example-1.svg)

## 配置条件

先配置两端底层接口、BGP EVPN 邻居和 VTEP 源。两个站点的 VNI 与 RT 相同，RD 分别配置。

先建立 VTEP 底层连通和 BGP EVPN 邻居。两端 VNI 与业务 RT 必须一致，RD 按设备分别指定。示例使用 VNI 65010。

## 配置步骤

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

## 验证方法

对照{ref}`本功能页的实测结果 <recorded-result-06-tunnels-vxlan-evpn>`可以核对设备实际显示的字段或业务表现。不同拓扑请按本案例的地址和接口检查。

对照以下命令和预期结果核对设备状态。

```vortexros-cli
display bgp evpn peer
display bridge-domain 65536
display vxlan tunnel
```

核对 EVPN 邻居建立及 VNI 65010 的桥域与 VTEP，随后检查站点间终端转发。
