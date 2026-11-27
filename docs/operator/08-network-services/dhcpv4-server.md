---
nav_title: DHCPv4 服务器
nav_overview: 介绍
nav_feature: true
---


(section-operator-08-network-services-dhcpv4-server-1)=
# DHCPv4 服务器

<span id="overview"></span>

为直连客户端分配 IPv4 地址、网关、DNS 及租期。可使用全局地址池，也可根据三层接口地址建立接口地址池。

<span id="principles"></span>

(section-operator-08-network-services-dhcpv4-server-2)=
## 工作原理

服务端根据客户端所在链路选择地址池。经过中继时，使用中继提供的链路信息选择子网。可用地址池、已经分配的租约和客户端实际可用状态需要分别核对。

支持全局池和基于接口的地址池。可指定起止地址、网关、DNS 与租期。

<span id="examples"></span>

(section-operator-08-network-services-dhcpv4-server-3)=
## 配置与验证

(case-conditions-08-network-services-dhcpv4-server)=
### 配置条件

准备三层接口及可用地址范围。一个地址池只绑定同一 VPN 内的一个服务接口。交换端口所在的网段应使用对应 Vlanif 提供 DHCP。

```{toctree}
:maxdepth: 1

dhcpv4-server/cases/example-1
dhcpv4-server/cases/example-2
dhcpv4-server/cases/vpn-static-lease
```

(case-verification-08-network-services-dhcpv4-server)=
### 通用验证

```vortexros-cli
display dhcp service verbose
display ip pool
display ip pool used
```

核对服务 Ready 和地址池配置，让终端重新请求租约，检查分配地址、网关与有效期。DHCP 中的 DNS 选项用于客户端。

<span id="observed"></span>

实测节选中的物理接口按文档端口编号记为 EthernetX。其他表项保留原始验证值。

(recorded-result-08-network-services-dhcpv4-server)=
(result-operator-08-network-services-dhcpv4-server)=
### 直连、中继和独立 VPN 的实测结果

两台设备完成直连客户端和经另一节点中继的 IPv4 取址。另在独立 VPN 实例配置 IPv4 地址池，客户端成功获取该实例中的地址，撤销服务后复查结果。

(lab-result-operator-08-network-services-dhcpv4-server)=
### 客户端侧实际拿到的 VPN 租约

服务端在 VPN 实例 ALL 中分配 IPv4 租约。隔离客户端读到的实际地址为 10.253.10.105/24。结合服务端的地址池和客户端显示，可核对同一个租约与 VPN。

```text
Interface   Address-Family  Role    Pool/Servers  VPN-Instance  State    Address           Delegated-Prefix
Ethernet2   IPv4            client  -             ALL           running  10.253.10.105/24  -
```

<span id="precautions"></span>

(section-operator-08-network-services-dhcpv4-server-4)=
## 注意事项

排除网关、设备本机地址和保留地址。确保当前子网只有预期的地址分配服务。

<p data-legacy-id="id1" class="manual-previous-section" data-section-moved><a href="#overview">介绍</a></p>
<p data-legacy-id="id2" class="manual-previous-section" data-section-moved><a href="#case-conditions-08-network-services-dhcpv4-server">配置准备</a></p>
<p data-legacy-id="id3" class="manual-previous-section" data-section-moved><a href="#examples">配置案例</a></p>
<p data-legacy-id="id4" class="manual-previous-section" data-section-moved><a href="#case-verification-08-network-services-dhcpv4-server">验证配置</a></p>
<p data-legacy-id="vortexros" class="manual-previous-section" data-section-moved><a href="cases/example-2/">使用一台 VortexROS 作为租约客户端</a></p>
