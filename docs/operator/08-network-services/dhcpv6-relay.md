# DHCPv6 中继

## 功能介绍

在不同 IPv6 网段之间传递 DHCPv6 请求，使接入网段可使用远端服务器。

## 配置准备

在客户端所在的三层接口配置中继，确认目标服务器可达并为接入链路准备 IPv6 地址池。

## 配置案例

```vortexros-config
interface Ethernet 1
 ipv6 enable
 ipv6 address 2001:db8:10::1 64
 dhcpv6 relay destination 2001:db8:20::10
#
return
```

录入后提交。在 DPDK 模式也可使用承载客户网段的 Vlanif。需取消时执行 `undo dhcpv6 relay destination 2001:db8:20::10` 后提交。

## 验证配置

```vortexros-cli
display dhcpv6 relay
display ipv6 routing-table
```

核对中继接口与目标地址，用接入客户端实际请求租约并检查服务器返回的地址或前缀。
