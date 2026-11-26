# IP-in-IP 隧道

## 功能介绍

IP-in-IP 用 IP 包封装另一个 IP 包，连接跨底层网络的三层网段。按需搭配 IPv4 或 IPv6 内外层。

## 配置准备

确认两个外层地址互相可达，双方选择一致的封装协议。示例使用 IPv4 内层与 IPv4 外层。

## 配置案例

```vortexros-config
interface Tunnel 2
 tunnel-protocol ipv4-ipv4
 source 192.0.2.1
 destination 192.0.2.2
 ip address 10.0.12.1 255.255.255.252
#
return
```

对端对调源和目的并将内部接口设为 10.0.12.2，录入后提交。

### ipv4-ipv4 双端配置

R1 与 R2 的 Ethernet0 互联。外层使用两端真实接口地址，内层通过 Tunnel2 组成独立的业务网段。以下模式分别部署，不在同一个 Tunnel2 上叠加。

两台设备分别在系统视图录入各自的配置片段，退出功能视图后提交。

**R1**

```vortexros-config
interface Ethernet 0
 ip address 192.0.2.1 255.255.255.0
#
interface Tunnel 2
 tunnel-protocol ipv4-ipv4
 source 192.0.2.1
 destination 192.0.2.2
 ip address 10.0.12.1 255.255.255.252
#
return
```

**R2**

```vortexros-config
interface Ethernet 0
 ip address 192.0.2.2 255.255.255.0
#
interface Tunnel 2
 tunnel-protocol ipv4-ipv4
 source 192.0.2.2
 destination 192.0.2.1
 ip address 10.0.12.2 255.255.255.252
#
return
```

分别查看状态。

```vortexros-cli
display interface Tunnel 2
display ip interface brief
display ip routing-table protocol direct
```

隧道接口应为 up，直连前缀 10.0.12.0/30 指向 Tunnel2。分别从两端 ping 对端的隧道 IPv4 地址。

### ipv6-ipv4 双端配置

R1 与 R2 的 Ethernet0 互联。外层使用两端真实接口地址，内层通过 Tunnel2 组成独立的业务网段。以下模式分别部署，不在同一个 Tunnel2 上叠加。

两台设备分别在系统视图录入各自的配置片段，退出功能视图后提交。

**R1**

```vortexros-config
interface Ethernet 0
 ip address 192.0.2.1 255.255.255.0
#
interface Tunnel 2
 tunnel-protocol ipv6-ipv4
 source 192.0.2.1
 destination 192.0.2.2
 ipv6 enable
 ipv6 address 2001:db8:40::1 64
#
return
```

**R2**

```vortexros-config
interface Ethernet 0
 ip address 192.0.2.2 255.255.255.0
#
interface Tunnel 2
 tunnel-protocol ipv6-ipv4
 source 192.0.2.2
 destination 192.0.2.1
 ipv6 enable
 ipv6 address 2001:db8:40::2 64
#
return
```

分别查看状态。

```vortexros-cli
display interface Tunnel 2
display ipv6 interface brief
display ipv6 routing-table protocol direct
```

隧道接口应为 up，直连前缀 2001:db8:40::/64 指向 Tunnel2。分别从两端 ping 对端的隧道 IPv6 地址。

### ipv4-ipv6 双端配置

R1 与 R2 的 Ethernet0 互联。外层使用两端真实接口地址，内层通过 Tunnel2 组成独立的业务网段。以下模式分别部署，不在同一个 Tunnel2 上叠加。

两台设备分别在系统视图录入各自的配置片段，退出功能视图后提交。

**R1**

```vortexros-config
interface Ethernet 0
 ipv6 enable
 ipv6 address 2001:db8:12::1 64
#
interface Tunnel 2
 tunnel-protocol ipv4-ipv6
 source 2001:db8:12::1
 destination 2001:db8:12::2
 ip address 10.0.12.1 255.255.255.252
#
return
```

**R2**

```vortexros-config
interface Ethernet 0
 ipv6 enable
 ipv6 address 2001:db8:12::2 64
#
interface Tunnel 2
 tunnel-protocol ipv4-ipv6
 source 2001:db8:12::2
 destination 2001:db8:12::1
 ip address 10.0.12.2 255.255.255.252
#
return
```

分别查看状态。

```vortexros-cli
display interface Tunnel 2
display ip interface brief
display ip routing-table protocol direct
```

隧道接口应为 up，直连前缀 10.0.12.0/30 指向 Tunnel2。分别从两端 ping 对端的隧道 IPv4 地址。

### ipv6-ipv6 双端配置

R1 与 R2 的 Ethernet0 互联。外层使用两端真实接口地址，内层通过 Tunnel2 组成独立的业务网段。以下模式分别部署，不在同一个 Tunnel2 上叠加。

两台设备分别在系统视图录入各自的配置片段，退出功能视图后提交。

**R1**

```vortexros-config
interface Ethernet 0
 ipv6 enable
 ipv6 address 2001:db8:12::1 64
#
interface Tunnel 2
 tunnel-protocol ipv6-ipv6
 source 2001:db8:12::1
 destination 2001:db8:12::2
 ipv6 enable
 ipv6 address 2001:db8:40::1 64
#
return
```

**R2**

```vortexros-config
interface Ethernet 0
 ipv6 enable
 ipv6 address 2001:db8:12::2 64
#
interface Tunnel 2
 tunnel-protocol ipv6-ipv6
 source 2001:db8:12::2
 destination 2001:db8:12::1
 ipv6 enable
 ipv6 address 2001:db8:40::2 64
#
return
```

分别查看状态。

```vortexros-cli
display interface Tunnel 2
display ipv6 interface brief
display ipv6 routing-table protocol direct
```

隧道接口应为 up，直连前缀 2001:db8:40::/64 指向 Tunnel2。分别从两端 ping 对端的隧道 IPv6 地址。

## 验证配置

```vortexros-cli
display interface Tunnel 2
display ip routing-table protocol direct
```

检查接口和直连前缀，随后从两端分别 ping 对端隧道地址。用 undo interface Tunnel 2 删除不再使用的隧道。
