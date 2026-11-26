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

### 上联接口模式与三节点租约

服务器 Ethernet0 连中继 Ethernet0，使用 2001:db8:20::/64。中继 Ethernet1 连客户端，使用 2001:db8:10::/64。下例使用上联接口模式，单播目标模式见前例。

**服务器**

```vortexros-config
enable dhcp server
#
dhcpv6 pool ACCESS6
 address prefix 2001:db8:10::/64 life-time 3600 1800
 excluded-address 2001:db8:10::1
#
interface Ethernet 0
 ipv6 enable
 ipv6 address 2001:db8:20::10 64
 dhcpv6 server ACCESS6
#
ipv6 route-static 2001:db8:10:: 64 2001:db8:20::2
#
return
```

**中继**

```vortexros-config
interface Ethernet 0
 ipv6 enable
 ipv6 address 2001:db8:20::2 64
#
interface Ethernet 1
 ipv6 enable
 ipv6 address 2001:db8:10::1 64
 dhcpv6 relay interface Ethernet0
#
return
```

**客户端**

```vortexros-config
interface Ethernet 0
 ipv6 enable
 ipv6 address auto dhcp
#
ipv6 route-static 2001:db8:10:: 64 Ethernet0
#
return
```

分别提交。中继执行 `display dhcpv6 relay`，服务器执行 `display dhcpv6 pool name ACCESS6 used`，客户端执行 `display dhcpv6 client interface Ethernet0`。正常时中继在下联运行并指向 Ethernet0，服务器显示 IA_NA 租约，客户端取得 2001:db8:10::/64 内的地址并能 ping 中继的 ::1。其他网段的默认路由另配。

## 验证配置

```vortexros-cli
display dhcpv6 relay
display ipv6 routing-table
```

核对中继接口与目标地址，用接入客户端实际请求租约并检查服务器返回的地址或前缀。
