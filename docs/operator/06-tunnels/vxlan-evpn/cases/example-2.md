---
nav_title: 两个 VTEP 的高位 BD 与动态学习
---


# 两个 VTEP 的高位 BD 与动态学习

## 拓扑

![终端 A 和终端 B 经两台 VTEP 及 VNI 65010 二层互联](example-2.svg)

## 配置条件

先配置两端底层接口、BGP EVPN 邻居和 VTEP 源。两个站点的 VNI 与 RT 相同，RD 分别配置。

R1、R2 通过各自的 Ethernet0 直连，地址分别为 192.0.2.1/24 和 192.0.2.2/24。终端 A 接 R1 的 Ethernet1，地址为 203.0.113.11/24，示例 MAC 为 `0200-0001-0011`。终端 B 接 R2 的 Ethernet1，地址为 203.0.113.12/24，示例 MAC 为 `0200-0002-0012`。两端同用高位 BD 65536 和 VNI 65010，并选不同 RD。

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

对照{ref}`本功能页的实测结果 <recorded-result-06-tunnels-vxlan-evpn>`可以核对设备实际显示的字段或业务表现。不同拓扑请按本案例的地址和接口检查。

对照以下命令和预期结果核对设备状态。

```vortexros-cli
display bgp evpn all routing-table inclusive-route
display bgp evpn all routing-table mac-route
display vxlan tunnel
display bridge-domain 65536
display mac-address bridge-domain 65536
```

先检查 Type-3 路由和对端 VTEP。终端 A 向终端 B 发起 ping 并收到响应后，用 Type-2 路由和 MAC 表核对两端的学习结果。

**R1 的预期 MAC 表**（使用本案例的终端 MAC）

```text
<VortexROS> display mac-address bridge-domain 65536
-------------------------------------------------------------------------------
MAC Address       VLAN/VSI/BD                    Learned-From        Type
-------------------------------------------------------------------------------
0200-0001-0011    -/-/65536                      Ethernet1           dynamic
0200-0002-0012    -/-/65536                      192.0.2.2           dynamic
-------------------------------------------------------------------------------
Total items displayed = 2
```

在 R2 上，终端 B 的 MAC 对应本地 `Ethernet1`，终端 A 的 MAC 对应远端 VTEP `192.0.2.1`。本例只做同网段二层互联，可在终端查看对端的 ARP 表项，并在 VTEP 上用 MAC 表验证转发路径。

撤销 R2 的 NVE 下 VNI 65010 动态对等项，确认远端路径撤销且本地接入配置仍在。重新添加后，确认远端 MAC 和终端互通恢复。
