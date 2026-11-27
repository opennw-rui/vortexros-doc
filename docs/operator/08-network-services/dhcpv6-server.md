---
nav_title: DHCPv6 服务器
nav_overview: 介绍
nav_feature: true
---


(section-operator-08-network-services-dhcpv6-server-1)=
# DHCPv6 服务器

<span id="overview"></span>

DHCPv6 服务器可向客户端分配 IPv6 地址，也可在支持的地址池中分配委派前缀。IPv6 默认路由另由 RA 或静态配置提供。

<span id="principles"></span>

(section-operator-08-network-services-dhcpv6-server-2)=
## 工作原理

服务端根据客户端所在链路选择地址池。经过中继时，按中继提供的链路信息匹配子网。地址分配（IA_NA）用于给客户端自身接口赋址。前缀委派（IA_PD）用于向下游路由器提供可再划分的前缀。租约、客户端地址和默认路由需要分别核对。

<span id="examples"></span>

(section-operator-08-network-services-dhcpv6-server-3)=
## 配置与验证

(section-operator-08-network-services-dhcpv6-server-4)=
### 拓扑

![R1 和 R2 通过 Ethernet0 直连，由 R1 分配 IPv6 地址](dhcpv6-server/direct.svg)

(case-conditions-08-network-services-dhcpv6-server)=
### 配置条件

R1 和 R2 的 Ethernet0 均为三层口。R1 使用 `2001:db8:252:10::1/120`，R2 从 R1 获得 IA_NA 地址。本例使用静态链路路由验证连通性。实际网络也可通过 [RA](../04-ip-routing/ipv6-router-advertisement.md) 提供链路信息和默认路由。

(section-operator-08-network-services-dhcpv6-server-5)=
### 配置步骤

在 R1 创建地址池，并将其绑定到连接客户端的接口。排除 R1 自己使用的地址。`life-time` 的两个数值分别为有效期和首选期，单位为秒。

```vortexros-cli
system-view
enable dhcp server
dhcpv6 pool LAN6
 address prefix 2001:db8:252:10::/120 life-time 3600 1800
 excluded-address 2001:db8:252:10::1
 quit
interface Ethernet 0
 ipv6 enable
 ipv6 address 2001:db8:252:10::1 120
 dhcpv6 server LAN6
 quit
commit
return
```

在 R2 申请租约。DHCPv6 分配的是单个地址，本例加一条到该链路前缀的直连静态路由。

```vortexros-cli
system-view
interface Ethernet 0
 ipv6 enable
 ipv6 address auto dhcp
 quit
ipv6 route-static 2001:db8:252:10:: 120 Ethernet 0
commit
return
```

(case-verification-08-network-services-dhcpv6-server)=
### 验证方法

在 R1 核对服务运行和池使用情况。

```vortexros-cli
display dhcp service verbose
display dhcpv6 pool name LAN6 used
display ipv6 pool name LAN6 all
```

在 R2 核对客户端地址和业务可达性。

```vortexros-cli
display dhcpv6 client interface Ethernet 0
display ipv6 interface brief
ping ipv6 2001:db8:252:10::1
```

预期 R1 的已用租约出现 R2 的 DUID、IAID、分配地址和剩余租期，R2 接口显示同一地址并能到达 R1。签名开发镜像直连用例实测分配到 `2001:db8:252:10::3/128`，具体租约由地址池决定。

### 为下游路由器分配前缀

需要向下游网络委派子网时参见[服务器与客户端的前缀委派案例](dhcpv6-client/cases/example-2.md)。查看 DHCPv6 服务端的 IA_PD 租约，并在下游路由器检查前缀和使用该前缀的接口。

<span id="observed"></span>

(result-operator-08-network-services-dhcpv6-server)=
### 双端服务与中继的实测结果

服务端分别向同一链路的客户端和经另一节点中继的客户端发放 IPv6 地址。中继场景通过三层 Vlanif 上联，客户端的 DHCPv6 Reply 实际承载 IA_NA 地址 2001:db8:81::100，有效租期 600 秒。

<span id="precautions"></span>

(section-operator-08-network-services-dhcpv6-server-6)=
## 注意事项

首选期不应超过有效期。IPv6 默认网关另用 RA 或静态配置。撤销时先移除接口下的 `dhcpv6 server LAN6` 绑定，再删除已无其他引用的地址池。在客户端撤销自动地址和本例的静态路由，提交后复查客户端地址。

<p data-legacy-id="id1" class="manual-previous-section" data-section-moved><a href="#overview">介绍</a></p>
<p data-legacy-id="id2" class="manual-previous-section" data-section-moved><a href="#case-conditions-08-network-services-dhcpv6-server">配置准备</a></p>
<p data-legacy-id="id3" class="manual-previous-section" data-section-moved><a href="#examples">配置案例</a></p>
<p data-legacy-id="id4" class="manual-previous-section" data-section-moved><a href="#case-verification-08-network-services-dhcpv6-server">验证配置</a></p>
