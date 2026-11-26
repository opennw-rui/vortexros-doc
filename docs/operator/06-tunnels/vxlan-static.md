# 静态 VXLAN 与 NVE

## 功能介绍

VXLAN 在 IP 网络上延伸二层业务。静态模式从 NVE 手动指定远端 VTEP，适用于远端固定的部署。

## 配置准备

为两台设备规划可达的 VTEP 地址，预建相同的 VNI 与本地桥域。示例源地址 192.0.2.1，远端 192.0.2.2。

## 配置案例

```text
interface Nve 1
 source 192.0.2.1
 vni 1011 head-end peer-list 192.0.2.2
```

使用 [Bridge Domain](../03-interfaces-l2/bridge-domain.md) 绑定本地业务。验证时可执行：

```vortexros-cli
display vxlan tunnel
display vxlan statistics source 192.0.2.1 peer 192.0.2.2 vni 1011
display bridge-domain 11
display mac-address
```

删除远端或整个NVE配置：

```text
interface Nve 1
 undo vni 1011 head-end peer-list 192.0.2.2
quit
undo interface Nve 1
commit
```

### 两个 VTEP 的静态二层互通

R1 和 R2 各用 Ethernet0 作为底层，地址为 192.0.2.1 和 .2。两个终端分别接两端 Ethernet1，使用同一个业务网段 203.0.113.0/24。两台设备都使用 VLAN 100、BD 11 和 VNI 1011。

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

分别查看状态。

```vortexros-cli
display vxlan tunnel
display bridge-domain 11
display mac-address
```

每端只有一个远端 VTEP，VNI 为 1011。终端互相 ping 后，检查桥域本地口和远端 MAC 出口，确认隧道计数增长。撤去静态列表条目后，相应远端应从该 VNI 消失。

## 验证配置

```vortexros-cli
display vxlan tunnel
display vxlan statistics source 192.0.2.1 peer 192.0.2.2 vni 1011
display bridge-domain 11
```

确认 VNI 与 VTEP 一致，从两端桥域内的终端测试互通，并检查 VXLAN 收发计数。
