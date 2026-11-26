---
nav_title: IPIP Tunnel
nav_overview: 介绍
nav_feature: true
---


(section-operator-06-tunnels-ip-in-ip-1)=
# IPIP Tunnel

<span id="overview"></span>

IP-in-IP 用 IP 包封装另一个 IP 包，连接跨底层网络的三层网段。按需搭配 IPv4 或 IPv6 内外层。

<span id="principles"></span>

(section-operator-06-tunnels-ip-in-ip-2)=
## 工作原理

外层地址族决定底层运输方式，内层地址族决定实际承载的业务。两端分别设置相反的源和目的，底层路由选择必须能解析外层目的，验证用内层流量而非仅 ping 外层地址。

隧道模式由内层、外层地址族决定，两端必须一致。

| 模式 | 内层 | 外层 |
| --- | --- | --- |
| `ipv4-ipv4` | IPv4 | IPv4 |
| `ipv6-ipv4` | IPv6 | IPv4 |
| `ipv4-ipv6` | IPv4 | IPv6 |
| `ipv6-ipv6` | IPv6 | IPv6 |

与 [GRE Tunnel](gre.md) 一样，外层端点不完整时显示 `^down`。PHY up 要求隧道已启用且本端有可用的底层转发路径。Protocol up 还要求内层地址有效。

<span id="examples"></span>

(section-operator-06-tunnels-ip-in-ip-3)=
## 配置与验证

(case-conditions-06-tunnels-ip-in-ip)=
### 配置条件

准备两个可达的三层外层端点，并按内层和外层地址族选择相同的封装模式。隧道网络与底层链路使用不同网段。

配置前确认两个外层地址互相可达。以下四个案例独立使用，同一个 Tunnel 只选一种模式。

```{toctree}
:maxdepth: 1

ip-in-ip/cases/ipv4-over-ipv4
ip-in-ip/cases/ipv6-over-ipv4
ip-in-ip/cases/ipv4-over-ipv6
ip-in-ip/cases/ipv6-over-ipv6
```

(case-verification-06-tunnels-ip-in-ip)=
### 通用验证

```vortexros-cli
display interface Tunnel 2
display ip routing-table protocol direct
```

检查接口和直连前缀，随后从两端分别 ping 对端隧道地址。用 undo interface Tunnel 2 删除不再使用的隧道。

<span id="observed"></span>

(recorded-result-06-tunnels-ip-in-ip)=
### 四种封装组合的实测结果

实包验证了 IPv4 over IPv4、IPv6 over IPv4、IPv4 over IPv6、IPv6 over IPv6。四种组合都能双向转发，重置数据面后恢复。删除单条隧道时，只撤销该隧道及其转发，其他组合保持可用。

<span id="precautions"></span>

(section-operator-06-tunnels-ip-in-ip-4)=
## 注意事项

- 底层应能独立到达远端外层地址。不要把到该地址的路径指回同一 Tunnel。
- 外层 IPv6 的基础头比外层 IPv4 更长。切换外层地址族后，按实际路径 MTU 核对内层报文大小。

<p data-legacy-id="id1" class="manual-previous-section" data-section-moved><a href="#overview">介绍</a></p>
<p data-legacy-id="id2" class="manual-previous-section" data-section-moved><a href="#principles">功能特性</a></p>
<p data-legacy-id="id5" class="manual-previous-section" data-section-moved><a href="#precautions">注意事项</a></p>
<p data-legacy-id="id3" class="manual-previous-section" data-section-moved><a href="#examples">配置案例</a></p>
<p data-legacy-id="id4" class="manual-previous-section" data-section-moved><a href="#case-verification-06-tunnels-ip-in-ip">验证配置</a></p>
<p data-legacy-id="ipv4-ipv4" class="manual-previous-section" data-section-moved><a href="cases/ipv4-over-ipv4/">IPv4 业务经 IPv4 底层</a></p>
<p data-legacy-id="ipv6-ipv4" class="manual-previous-section" data-section-moved><a href="cases/ipv6-over-ipv4/">IPv6 业务经 IPv4 底层</a></p>
<p data-legacy-id="ipv4-ipv6" class="manual-previous-section" data-section-moved><a href="cases/ipv4-over-ipv6/">IPv4 业务经 IPv6 底层</a></p>
<p data-legacy-id="ipv6-ipv6" class="manual-previous-section" data-section-moved><a href="cases/ipv6-over-ipv6/">IPv6 业务经 IPv6 底层</a></p>
