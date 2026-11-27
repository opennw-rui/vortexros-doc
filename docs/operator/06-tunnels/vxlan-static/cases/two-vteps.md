---
nav_title: 两个 VTEP 的静态二层互通
---


# 两个 VTEP 的静态二层互通

## 拓扑

![两个站点通过各自 Ethernet1 接入 VLAN 100 并跨 VXLAN 互通](two-vteps.svg)

## 配置条件

两端 VTEP 的底层地址彼此可达，启用相应的桥域和数据面。选择相同 VNI，并规划每端本地接入口。

R1 和 R2 各用 Ethernet0 作为底层，地址分别为 192.0.2.1/24 和 192.0.2.2/24。终端 A、B 分别接 R1、R2 的 Ethernet1，地址分别为 203.0.113.11/24 和 203.0.113.12/24。两台设备都使用 VLAN 100、BD 11 和 VNI 1011。

## 配置步骤

两台设备分别在系统视图录入各自的配置片段，退出功能视图后提交。

**R1**

```vortexros-config
interface Ethernet 0
 ip address 192.0.2.1 255.255.255.0
#
enable switch
#
vlan 100
#
interface Ethernet 1
 portswitch
 port link-type access
 port default vlan 100
#
bridge-domain 11
 l2 binding vlan 100
 vxlan vni 1011
#
interface Nve 1
 source 192.0.2.1
 vni 1011 head-end peer-list 192.0.2.2
#
return
```

**R2**

```vortexros-config
interface Ethernet 0
 ip address 192.0.2.2 255.255.255.0
#
enable switch
#
vlan 100
#
interface Ethernet 1
 portswitch
 port link-type access
 port default vlan 100
#
bridge-domain 11
 l2 binding vlan 100
 vxlan vni 1011
#
interface Nve 1
 source 192.0.2.2
 vni 1011 head-end peer-list 192.0.2.1
#
return
```

## 验证方法

对照{ref}`本功能页的实测结果 <recorded-result-06-tunnels-vxlan-static>`可以核对设备实际显示的字段或业务表现。不同拓扑请按本案例的地址和接口检查。

对照以下命令和预期结果核对设备状态。

```vortexros-cli
display vxlan tunnel
display bridge-domain 11
display mac-address
```

每端只有一个远端 VTEP，VNI 为 1011。终端互相 ping 后，检查桥域本地口和远端 MAC 出口，确认隧道计数增长。撤去静态列表条目后，相应远端应从该 VNI 消失。
