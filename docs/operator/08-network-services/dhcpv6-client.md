# DHCPv6 客户端与前缀委派

## 功能介绍

在三层上联获取 IPv6 地址或受委派前缀。IPv6 的默认网关由路由通告或静态路由提供。

## 配置准备

确认上游支持有状态地址分配或前缀委派。如果还需要默认路由，请准备 RA。

## 配置案例

有状态地址、前缀委派以及立即续租的示例：

```text
interface Ethernet 1
 ipv6 address auto dhcp
 dhcpv6 client pd CPE-PREFIX
commit
display dhcpv6 client interface Ethernet 1
display dhcpv6 client prefix name CPE-PREFIX
# 在接口视图立即请求续租：
interface Ethernet 1
 dhcpv6 client renew
```

`display dhcpv6 client`分别显示IA_NA地址和IA_PD委派前缀，不会用其中一个字段遮盖另一个字段。`dhcpv6 client renew`是立即执行的运行命令，不进入待提交配置或保存配置。

如需在同一接口通过 RA 接受默认路由，可在接口配置 `ipv6 nd ra default-route enable`。用对应的 undo 命令撤销地址获取、前缀委派或 RA 设置。

## 验证配置

```vortexros-cli
display dhcpv6 client interface Ethernet 1
display dhcpv6 client prefix name CPE-PREFIX
display ipv6 interface brief
```

分别确认接口地址与委派前缀。需要对外通信时再检查 IPv6 默认路由。

[IPv6 路由通告与 SLAAC](../04-ip-routing/ipv6-router-advertisement.md)
