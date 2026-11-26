---
nav_title: DHCPv4 中继
nav_overview: 介绍
nav_feature: true
---


(section-operator-08-network-services-dhcpv4-relay-1)=
# DHCPv4 中继

<span id="overview"></span>

DHCPv4 中继将本地客户端的请求转发到其他子网的 DHCPv4 服务器，使多个接入网段可以共用服务。

<span id="principles"></span>

(section-operator-08-network-services-dhcpv4-relay-2)=
## 工作原理

中继把客户端本地链路上的请求送到另一网段的服务器。客户端侧用三层接口接入；接入口为二层时应把中继配置在相应 Vlanif。检查中继出口和服务器返回路径之后，再在客户端确认租约。

把客户端广播请求转交指定 DHCPv4 服务器，服务端按接入网段选地址。

<span id="examples"></span>

(section-operator-08-network-services-dhcpv4-relay-3)=
## 配置与验证

(case-conditions-08-network-services-dhcpv4-relay)=
### 配置条件

在客户端网段准备三层接口与地址。确认服务器有该网段的地址池，并能路由回中继地址。

```{toctree}
:maxdepth: 1

dhcpv4-relay/cases/example-1
dhcpv4-relay/cases/example-2
```

(case-verification-08-network-services-dhcpv4-relay)=
### 通用验证

```vortexros-cli
display dhcp relay
display ip interface brief
```

检查目标服务器和接口。让接入终端实际发起 DHCP 请求，并检查其获取的地址、网关和续租。

<span id="observed"></span>

(recorded-result-08-network-services-dhcpv4-relay)=
### 中继运行状态的实测回显

在另一套双栈拓扑中，中继目标是服务器 198.18.82.2。行中的 `running` 表示中继正在运行。客户端能否取得地址仍用实际租约验证。

```text
<VortexROS> display dhcp relay interface Ethernet0
Interface  Address-Family  Role   Pool/Servers  VPN-Instance  State    Address  Delegated-Prefix
Ethernet0  IPv4            relay  198.18.82.2   default       running  -        -
```

<span id="precautions"></span>

(section-operator-08-network-services-dhcpv4-relay-4)=
## 注意事项

中继配置在客户端所在的三层接口。服务端需有匹配的池和到中继的回程。

<p data-legacy-id="id1" class="manual-previous-section" data-section-moved><a href="#overview">介绍</a></p>
<p data-legacy-id="id2" class="manual-previous-section" data-section-moved><a href="#case-conditions-08-network-services-dhcpv4-relay">配置准备</a></p>
<p data-legacy-id="id3" class="manual-previous-section" data-section-moved><a href="#examples">配置案例</a></p>
<p data-legacy-id="id5" class="manual-previous-section" data-section-moved><a href="#case-verification-08-network-services-dhcpv4-relay">验证配置</a></p>
<p data-legacy-id="id4" class="manual-previous-section" data-section-moved><a href="cases/example-2/">三节点中继和服务端回程</a></p>
