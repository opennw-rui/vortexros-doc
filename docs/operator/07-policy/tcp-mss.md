---
nav_title: TCP MSS 调整
nav_overview: 介绍
nav_feature: true
---


(section-operator-07-policy-tcp-mss-1)=
# TCP MSS 调整

<span id="overview"></span>

当三层路径中存在封装开销时，TCP MSS 调整可限制握手协商的报文段大小。

<span id="principles"></span>

(section-operator-07-policy-tcp-mss-2)=
## 工作原理

MSS 约束 TCP 对端可发送的最大数据段，主要在 SYN 协商时出现。调整之后用新连接抓取 SYN 验证；已有连接和 UDP 不适合验证这项设置。

可对三层 TCP SYN 按接口 MTU 自动限制 MSS，也可配置固定 MSS。

<span id="examples"></span>

(section-operator-07-policy-tcp-mss-3)=
## 配置与验证

(case-conditions-07-policy-tcp-mss)=
### 配置条件

仅在三层接口或受支持的隧道上配置。核对路径 MTU，以及 TCP 流量的实际入口和出口。

```{toctree}
:maxdepth: 1

tcp-mss/cases/example-1
tcp-mss/cases/example-2
```

(case-verification-07-policy-tcp-mss)=
### 通用验证

```vortexros-cli
display interface Tunnel 1
display current-configuration | include tcp mss
```

检查接口 MTU 和已提交的 MSS 规则。通过实际 TCP 连接确认 SYN 中的 MSS 符合预期。

<span id="observed"></span>

(recorded-result-07-policy-tcp-mss)=
### IPv4 与 IPv6 的 TCP 握手实测结果

IPv4 PAT 场景的同一条 TCP 流在出口观察到 MSS 1200。IPv6 组合策略将同一条流的 MSS 限制为 1240，撤销后在出口观察到 MSS 恢复为 1440。应核对 SYN 中实际通告的值。

<span id="precautions"></span>

(section-operator-07-policy-tcp-mss-4)=
## 注意事项

先核对隧道封装的路径 MTU。验证用新连接查看 SYN，既有连接无法反映新协商的值。

<p data-legacy-id="id1" class="manual-previous-section" data-section-moved><a href="#overview">介绍</a></p>
<p data-legacy-id="id2" class="manual-previous-section" data-section-moved><a href="#case-conditions-07-policy-tcp-mss">配置准备</a></p>
<p data-legacy-id="id3" class="manual-previous-section" data-section-moved><a href="#examples">配置案例</a></p>
<p data-legacy-id="id4" class="manual-previous-section" data-section-moved><a href="#case-verification-07-policy-tcp-mss">验证配置</a></p>
<p data-legacy-id="gre-mss" class="manual-previous-section" data-section-moved><a href="cases/example-2/">两端 GRE 上的双向 MSS 调整</a></p>
