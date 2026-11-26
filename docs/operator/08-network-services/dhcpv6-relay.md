---
nav_title: DHCPv6 中继
nav_overview: 介绍
nav_feature: true
---


(section-operator-08-network-services-dhcpv6-relay-1)=
# DHCPv6 中继

<span id="overview"></span>

在不同 IPv6 网段之间传递 DHCPv6 请求，使接入网段可使用远端服务器。

<span id="principles"></span>

(section-operator-08-network-services-dhcpv6-relay-2)=
## 工作原理

中继把客户端本地链路上的请求送到另一网段的服务器。客户端侧用三层接口接入；接入口为二层时应把中继配置在相应 Vlanif。检查中继出口和服务器返回路径之后，再在客户端确认租约。

支持按指定目的地址或上联接口把 IPv6 客户租约交换转发到服务端。

<span id="examples"></span>

(section-operator-08-network-services-dhcpv6-relay-3)=
## 配置与验证

(case-conditions-08-network-services-dhcpv6-relay)=
### 配置条件

在客户端所在的三层接口配置中继，确认目标服务器可达并为接入链路准备 IPv6 地址池。

```{toctree}
:maxdepth: 1

dhcpv6-relay/cases/example-1
dhcpv6-relay/cases/example-2
```

(case-verification-08-network-services-dhcpv6-relay)=
### 通用验证

```vortexros-cli
display dhcpv6 relay
display ipv6 routing-table
```

核对中继接口与目标地址，用接入客户端实际请求租约并检查服务器返回的地址或前缀。

<span id="observed"></span>

(recorded-result-08-network-services-dhcpv6-relay)=
### 中继运行状态的实测回显

在另一套双栈拓扑中，指定的中继上联为 Ethernet1。行中的 `running` 表示中继正在运行。客户端能否取得地址仍用实际租约验证。

```text
<VortexROS> display dhcpv6 relay interface Ethernet0
Interface  Address-Family  Role   Pool/Servers         VPN-Instance  State    Address  Delegated-Prefix
Ethernet0  IPv6            relay  interface Ethernet1  default       running  -        -
```

<span id="precautions"></span>

(section-operator-08-network-services-dhcpv6-relay-4)=
## 注意事项

在接入网段的三层接口配置下联。服务端地址池及回程需匹配客户端网段。

<p data-legacy-id="id1" class="manual-previous-section" data-section-moved><a href="#overview">介绍</a></p>
<p data-legacy-id="id2" class="manual-previous-section" data-section-moved><a href="#case-conditions-08-network-services-dhcpv6-relay">配置准备</a></p>
<p data-legacy-id="id3" class="manual-previous-section" data-section-moved><a href="#examples">配置案例</a></p>
<p data-legacy-id="id5" class="manual-previous-section" data-section-moved><a href="#case-verification-08-network-services-dhcpv6-relay">验证配置</a></p>
<p data-legacy-id="id4" class="manual-previous-section" data-section-moved><a href="cases/example-2/">上联接口模式与三节点租约</a></p>
