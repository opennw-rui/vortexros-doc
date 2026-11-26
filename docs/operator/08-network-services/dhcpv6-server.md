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

服务端根据客户端所在链路选择地址池。经过中继时，使用中继提供的链路信息选择子网。可用地址池、已经分配的租约和客户端实际可用状态需要分别核对。

可按地址池分配 IPv6 单播地址或委派前缀。租约查询区分地址与前缀。

<span id="examples"></span>

(section-operator-08-network-services-dhcpv6-server-3)=
## 配置与验证

(section-operator-08-network-services-dhcpv6-server-4)=
### 拓扑

![IPv6 客户端 → 服务接口 → DHCPv6 地址池](dhcpv6-server/cases.svg)

(case-conditions-08-network-services-dhcpv6-server)=
### 配置条件

准备三层接口、地址池和 IPv6 前缀。地址与委派前缀应使用统一的有效和首选生命周期。

(section-operator-08-network-services-dhcpv6-server-5)=
### 配置步骤

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

(case-verification-08-network-services-dhcpv6-server)=
### 验证方法

对照以下命令和预期结果核对设备状态。

```vortexros-cli
display dhcp service verbose
display ipv6 pool
display dhcpv6 pool name LAN6 used
```

让客户端发起租约请求。确认地址或委派前缀、DUID、IAID 与剩余租期。

<span id="observed"></span>

(result-operator-08-network-services-dhcpv6-server)=
### 双端服务与中继的实测结果

服务端分别向同一链路的客户端和经另一节点中继的客户端发放 IPv6 地址。中继场景通过三层 Vlanif 上联，客户端的 DHCPv6 Reply 实际承载 IA_NA 地址 2001:db8:81::100，有效租期 600 秒。

<span id="precautions"></span>

(section-operator-08-network-services-dhcpv6-server-6)=
## 注意事项

有效期与首选期需要合理设置，首选期不应超过有效期。IPv6 默认网关另用 RA 或静态配置。

<p data-legacy-id="id1" class="manual-previous-section" data-section-moved><a href="#overview">介绍</a></p>
<p data-legacy-id="id2" class="manual-previous-section" data-section-moved><a href="#case-conditions-08-network-services-dhcpv6-server">配置准备</a></p>
<p data-legacy-id="id3" class="manual-previous-section" data-section-moved><a href="#examples">配置案例</a></p>
<p data-legacy-id="id4" class="manual-previous-section" data-section-moved><a href="#case-verification-08-network-services-dhcpv6-server">验证配置</a></p>
