---
nav_title: MPLS L3VPN、VPNv4 与 VPNv6
nav_overview: 介绍
nav_feature: true
---


(section-operator-10-mpls-l3vpn-l3vpn-1)=
# MPLS L3VPN、VPNv4 与 VPNv6

<span id="overview"></span>

L3VPN 在 MPLS 核心中承载相互隔离的客户路由。IPv6 客户流量可以通过 IPv4 的 MPLS 核心传输。

<span id="principles"></span>

(section-operator-10-mpls-l3vpn-l3vpn-2)=
## 工作原理

MP-BGP 通告 VPN 前缀、Route Target 及业务标签，核心转发表用传输标签把报文送到远端 PE。VPNv6 可经过 IPv4 MPLS 核心。远端导入、标签链路和业务双向性都需验证。

使用不同 VPN 实例隔离客户地址。PE 可在同一 MPLS 核心上同时运行 VPNv4 与 VPNv6。

<span id="examples"></span>

(section-operator-10-mpls-l3vpn-l3vpn-3)=
## 配置与验证

(case-conditions-10-mpls-l3vpn-l3vpn)=
### 配置条件

预先建立 PE 之间的 MPLS/LDP 与 MP-BGP 会话，准备客户接口、独立 RD 及两端匹配的 RT。

```{toctree}
:maxdepth: 1

l3vpn/cases/example-1
l3vpn/cases/example-2
l3vpn/cases/example-3
```

(case-verification-10-mpls-l3vpn-l3vpn)=
### 通用验证

```vortexros-cli
display bgp vpnv4 vpn-instance BLUE routing-table
display bgp vpnv6 vpn-instance BLUE routing-table
display ip routing-table vpn-instance BLUE
display ipv6 routing-table vpn-instance BLUE
display mpls forwarding-table
```

在 PE 核对远端 VPN 前缀及标签路径。从两端客户设备分别测试 IPv4 与 IPv6 的双向转发。

<span id="observed"></span>

实测节选中的物理接口按文档端口编号记为 EthernetX。其他表项保留原始验证值。

(recorded-result-10-mpls-l3vpn-l3vpn)=
### VPNv4 和 6VPE 的实测结果

在四节点 IPv4 MPLS 核心上分别验证租户 IPv4、IPv6 转发。改动一个租户的导入和导出 RT 后，核对该租户路由随之导入或撤销。IPv4、IPv6 缺省路由可独立启用和撤销。

(query-result-10-mpls-l3vpn-l3vpn)=
### 命令回显实测节选

在测试租户 CUST-A 中核对 IPv6 路由。BGP 安装了远端 IPv6 路由，下一跳使用 IPv4 映射形式。实际双向转发还应从租户 CE 发包验证。

```text
<P1> display ipv6 routing-table vpn-instance CUST-A
Destination  : 2001:db8:4::             PrefixLength : 64
NextHop      : ::ffff:4.4.4.4            Preference   : 254
Protocol     : BGP                       Flags        : DT
Interface    : Ethernet0                 VPN-Instance : default
```

<span id="precautions"></span>

(section-operator-10-mpls-l3vpn-l3vpn-4)=
## 注意事项

核对 RD、导入导出 RT、PE 到客户的回程及标签转发。IPv4-only 核心承载 VPNv6 时按案例核对核心口设置。

<p data-legacy-id="id1" class="manual-previous-section" data-section-moved><a href="#overview">介绍</a></p>
<p data-legacy-id="id2" class="manual-previous-section" data-section-moved><a href="#case-conditions-10-mpls-l3vpn-l3vpn">配置准备</a></p>
<p data-legacy-id="id3" class="manual-previous-section" data-section-moved><a href="#examples">配置案例</a></p>
<p data-legacy-id="id5" class="manual-previous-section" data-section-moved><a href="#case-verification-10-mpls-l3vpn-l3vpn">验证配置</a></p>
<p data-legacy-id="ipv4-vpnv4-vpnv6" class="manual-previous-section" data-section-moved><a href="cases/example-2/">IPv4 核心同时承载 VPNv4 和 VPNv6</a></p>
<p data-legacy-id="id4" class="manual-previous-section" data-section-moved><a href="cases/example-3/">增加备用核心链路并验证切换</a></p>
