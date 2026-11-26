# IPv4 与 IPv6 静态路由

## 功能介绍

静态路由把指定目的前缀交给固定的下一跳或出接口，适用于默认出口、固定对端或备用路径。

## 配置准备

确认下一跳在正确的路由表内可达。使用跨 VPN 下一跳时先创建相应 VPN。

## 配置案例

```text
ip route-static 203.0.113.0 255.255.255.0 192.0.2.1 preference 60 tag 100 description TO-WAN
ip route-static vpn-instance BLUE 10.0.0.0 8 vpn-instance default 192.0.2.1 Tunnel 1
ipv6 route-static 2001:db8:100:: 64 2001:db8::1
```

输入后执行 commit。跨 VPN 路由按配置区分目标 VPN 与下一跳所在 VPN。确认业务后执行 save。

### 双栈主机路由与回程

R1 与 R2 的 Ethernet0 用 192.0.2.0/24 和 2001:db8:12::/64 对接。两端通过静态路由到达对方 LoopBack0 的 198.51.100.x/32 和 2001:db8:x::1/128。

两台设备分别在系统视图录入各自的配置片段，退出功能视图后提交。

**R1**

```vortexros-config
interface Ethernet 0
 ip address 192.0.2.1 255.255.255.0
 ipv6 enable
 ipv6 address 2001:db8:12::1 64
#
interface LoopBack 0
 ip address 198.51.100.1 255.255.255.255
 ipv6 enable
 ipv6 address 2001:db8:1::1 128
#
ip route-static 198.51.100.2 255.255.255.255 192.0.2.2
#
ipv6 route-static 2001:db8:2::1 128 2001:db8:12::2
#
return
```

**R2**

```vortexros-config
interface Ethernet 0
 ip address 192.0.2.2 255.255.255.0
 ipv6 enable
 ipv6 address 2001:db8:12::2 64
#
interface LoopBack 0
 ip address 198.51.100.2 255.255.255.255
 ipv6 enable
 ipv6 address 2001:db8:2::1 128
#
ip route-static 198.51.100.1 255.255.255.255 192.0.2.1
#
ipv6 route-static 2001:db8:1::1 128 2001:db8:12::1
#
return
```

分别查看状态。

```vortexros-cli
display ip routing-table protocol static
display ipv6 routing-table protocol static
display ip fib
display ipv6 fib
```

在 R1 应看到静态路由分别指向 192.0.2.2 和 2001:db8:12::2，R2 应看到对称结果。用源地址为环回的双向 ping 验证回程。FIB 查询适用于 DPDK，业务在 BLUE 时另查 `display ip fib vpn-instance BLUE` 与 `display ipv6 fib vpn-instance BLUE`。撤销静态路由后，远端环回应退出，互联地址继续可达。

## 验证配置

```vortexros-cli
display ip routing-table protocol static
display ip routing-table vpn-instance BLUE
display ipv6 routing-table protocol static
display ip fib
display ipv6 fib
```

检查优选路由的目的前缀、下一跳和出接口。DPDK 数据面还可查看 FIB。存在多条等价路径时，核对每条有效路径并验证实际转发。
