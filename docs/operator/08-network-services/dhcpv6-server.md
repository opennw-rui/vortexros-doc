# DHCPv6 服务器

## 功能介绍

DHCPv6 服务器可向客户端分配 IPv6 地址，也可在支持的地址池中分配委派前缀。IPv6 默认路由另由 RA 或静态配置提供。

## 配置准备

准备三层接口、地址池和 IPv6 前缀。地址与委派前缀应使用统一的有效和首选生命周期。

## 配置案例

```text
dhcpv6 pool LAN6
 address prefix 2001:db8:100::/64
 dns-server 2001:4860:4860::8888
#
interface Vlanif 100
 dhcpv6 server LAN6
```

验证和撤销：

```text
display dhcp service verbose
display ipv6 pool
interface Vlanif 100
 undo dhcpv6 server
commit
```

录入接口和地址池后提交，再测试租约。

```vortexros-cli
display dhcpv6 pool name LAN6 used
display ipv6 pool name LAN6 all
```

## 验证配置

```vortexros-cli
display dhcp service verbose
display ipv6 pool
display dhcpv6 pool name LAN6 used
```

让客户端发起租约请求。确认地址或委派前缀、DUID、IAID 与剩余租期。
