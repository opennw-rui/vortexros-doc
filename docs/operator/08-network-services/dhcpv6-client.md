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

### 联动服务器的前缀委派

服务器与客户端 Ethernet0 直连，传输网段使用 2001:db8:20::/64。服务器把 2001:db8:100::/56 划分成 /64 委派给客户端。两台设备分别录入并提交。

**本端设备**

```vortexros-config
enable dhcp server
#
dhcpv6 pool PD
 prefix-delegation 2001:db8:100::/56 64 life-time 3600 1800
#
interface Ethernet 0
 ipv6 enable
 ipv6 address 2001:db8:20::1 64
 dhcpv6 server PD
#
return
```

**对端设备**

```vortexros-config
interface Ethernet 0
 ipv6 enable
 ipv6 address 2001:db8:20::2 64
 dhcpv6 client pd CPE-PREFIX
#
return
```

```vortexros-cli
display dhcpv6 pool name PD used
display dhcpv6 client prefix name CPE-PREFIX
```

第一条在服务器查询，第二条在客户端查询。服务器应有 IA_PD 记录，客户端所获前缀与服务器相同，长度为 /64。撤销客户端的 PD 后复查该接口不再使用委派前缀。

## 验证配置

```vortexros-cli
display dhcpv6 client interface Ethernet 1
display dhcpv6 client prefix name CPE-PREFIX
display ipv6 interface brief
```

分别确认接口地址与委派前缀。需要对外通信时再检查 IPv6 默认路由。

[IPv6 路由通告与 SLAAC](../04-ip-routing/ipv6-router-advertisement.md)
