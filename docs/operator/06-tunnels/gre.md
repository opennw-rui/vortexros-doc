# GRE 隧道

## 功能介绍

GRE 用于在可达的三层网络上承载另一条三层逻辑链路。隧道本身不提供加密。

## 配置准备

确定两端外层地址、VPN 和内层网段。保证外层目的地址经该 VPN 可达。

## 配置案例

```text
interface Tunnel 1
 description P1-P2-GRE
 tunnel-protocol gre
 source 192.0.2.1 vpn-instance default
 destination 192.0.2.2 vpn-instance default
 gre key 100
 mtu 1472
 ip address 10.0.12.1 255.255.255.252
```

source和destination必须按同一underlay VPN解析；GRE key可以与VPN绑定并存。修改/undo key后应重建所需参数且保持正确外层源地址，不能出现0.0.0.0。

```vortexros-cli
display interface Tunnel 1
```

提交后，Tunnel源地址必须能在指定underlay VPN中找到，目的地址也必须通过该VPN可达。隧道up后，Tunnel上的直连路由才应进入路由表。删除GRE隧道：

```text
undo interface Tunnel 1
commit
```

### 对接两个 IPv4 GRE 端点

R1、R2 用 Ethernet0 上的 192.0.2.1 和 192.0.2.2 作为外层地址，经 Tunnel1 承载 10.0.12.0/30。双方 GRE key 均为 100。

两台设备分别在系统视图录入各自的配置片段，退出功能视图后提交。

**R1**

```vortexros-config
interface Ethernet 0
 ip address 192.0.2.1 255.255.255.0
#
interface Tunnel 1
 tunnel-protocol gre
 source 192.0.2.1
 destination 192.0.2.2
 gre key 100
 mtu 1472
 ip address 10.0.12.1 255.255.255.252
#
return
```

**R2**

```vortexros-config
interface Ethernet 0
 ip address 192.0.2.2 255.255.255.0
#
interface Tunnel 1
 tunnel-protocol gre
 source 192.0.2.2
 destination 192.0.2.1
 gre key 100
 mtu 1472
 ip address 10.0.12.2 255.255.255.252
#
return
```

分别查看状态。

```vortexros-cli
display interface Tunnel 1
display ip routing-table protocol direct
```

两端隧道为 up，10.0.12.0/30 为直连。R1 ping 10.0.12.2，R2 ping 10.0.12.1。撤掉某端底层可达路径后检查状态变化，恢复路径时复查双向流量。

## 验证配置

```vortexros-cli
display interface Tunnel 1
display ip routing-table protocol direct
```

确认隧道和直连路由处于预期状态。在对端对调外层地址并配置同网段内层地址后，再验证双向流量。
