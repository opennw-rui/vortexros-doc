# IPv4 与 IPv6 接口地址

## 功能介绍

在三层接口配置 IPv4 或 IPv6 地址后，设备可以连接对应网段。同一 IPv4 接口可以有主地址和从地址，IPv6 地址逐条添加。

## 配置准备

准备 IPv4 掩码和 IPv6 前缀长度。接口必须处于三层模式。要使用 VPN，先绑定 VPN 再设地址。

## 配置案例

```vortexros-config
interface Ethernet 1
 ip address 192.0.2.2 255.255.255.0
 ipv6 address 2001:db8:10::2 64
#
interface LoopBack 0
 ipv6 address 2001:db8:100::1 64
 ipv6 address 2001:db8:200::1 64
#
return
```

在系统视图录入上述片段并提交。删除地址时用相同地址和掩码的 undo 命令。

## 验证配置

```vortexros-cli
display ip interface brief
display ipv6 interface brief
display ip routing-table protocol direct
display ipv6 routing-table protocol direct
```

核对接口上实际生效的地址和所属 VPN。接口在线时，检查相应的直连路由并从同网段对端测试。
