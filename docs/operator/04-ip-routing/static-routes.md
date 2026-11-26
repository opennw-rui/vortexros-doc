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

## 验证配置

```vortexros-cli
display ip routing-table protocol static
display ip routing-table vpn-instance BLUE
display ipv6 routing-table protocol static
display ip fib
display ipv6 fib
```

检查优选路由的目的前缀、下一跳和出接口。DPDK 数据面还可查看 FIB。存在多条等价路径时，核对每条有效路径并验证实际转发。
