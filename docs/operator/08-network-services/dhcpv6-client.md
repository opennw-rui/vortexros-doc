---
nav_title: DHCPv6 客户端与前缀委派
nav_overview: 介绍
nav_feature: true
---


(section-operator-08-network-services-dhcpv6-client-1)=
# DHCPv6 客户端与前缀委派

<span id="overview"></span>

在三层上联获取 IPv6 地址或受委派前缀。IPv6 的默认网关由路由通告或静态路由提供。

<span id="principles"></span>

(section-operator-08-network-services-dhcpv6-client-2)=
## 工作原理

DHCPv6 客户端可请求 IPv6 地址或可委派前缀。前缀委派用于给下游网段分配前缀，和本口地址是不同结果。验证时分别核对地址、委派前缀和实际路由。

可请求接口 IPv6 地址、前缀委派和续租，默认路由另由 RA 或静态路由提供。

<span id="examples"></span>

(section-operator-08-network-services-dhcpv6-client-3)=
## 配置与验证

(case-conditions-08-network-services-dhcpv6-client)=
### 配置条件

确认上游支持有状态地址分配或前缀委派。如果还需要默认路由，请准备 RA。

```{toctree}
:maxdepth: 1

dhcpv6-client/cases/example-1
dhcpv6-client/cases/example-2
```

(case-verification-08-network-services-dhcpv6-client)=
### 通用验证

```vortexros-cli
display dhcpv6 client interface Ethernet 1
display dhcpv6 client prefix name CPE-PREFIX
display ipv6 interface brief
```

分别确认接口地址与委派前缀。需要对外通信时再检查 IPv6 默认路由。

[IPv6 路由通告与 SLAAC](../04-ip-routing/ipv6-router-advertisement.md)

<span id="observed"></span>

(recorded-result-08-network-services-dhcpv6-client)=
### 已获得租约的实测回显

测试客户端的 Ethernet1 取得地址后，查询在同一行显示 `running` 和实际租约地址。请核对地址确实落在服务端地址池内。

```text
<VortexROS> display dhcpv6 client interface Ethernet1

Ethernet1  IPv6            client                default       running  2001:db8:82::57/128  -
```

<span id="precautions"></span>

(section-operator-08-network-services-dhcpv6-client-4)=
## 注意事项

租约和委派前缀是不同项目。启用续租或撤销时分别查询两者，管理设备在地址切换后需复查连接。

<p data-legacy-id="id1" class="manual-previous-section" data-section-moved><a href="#overview">介绍</a></p>
<p data-legacy-id="id2" class="manual-previous-section" data-section-moved><a href="#case-conditions-08-network-services-dhcpv6-client">配置准备</a></p>
<p data-legacy-id="id3" class="manual-previous-section" data-section-moved><a href="#examples">配置案例</a></p>
<p data-legacy-id="id5" class="manual-previous-section" data-section-moved><a href="#case-verification-08-network-services-dhcpv6-client">验证配置</a></p>
<p data-legacy-id="id4" class="manual-previous-section" data-section-moved><a href="cases/example-2/">联动服务器的前缀委派</a></p>
