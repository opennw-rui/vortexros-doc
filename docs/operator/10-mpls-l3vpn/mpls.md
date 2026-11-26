---
nav_title: MPLS 核心转发
nav_overview: 介绍
nav_feature: true
---


(section-operator-10-mpls-l3vpn-mpls-1)=
# MPLS 核心转发

<span id="overview"></span>

MPLS 通过标签转发报文，为 L3VPN 等业务提供核心传输。核心设备需能到达对端的稳定标识地址。

<span id="principles"></span>

(section-operator-10-mpls-l3vpn-mpls-2)=
## 工作原理

MPLS 转发设备按标签决定出接口和标签动作。核心下一跳由底层路由提供，业务标签可以和传输标签同时出现。用标签表与线侧抓包交叉核对。

按标签转发报文，支持核心链路的 MPLS 启用和 TTL 传播模式。

<span id="examples"></span>

(section-operator-10-mpls-l3vpn-mpls-3)=
## 配置与验证

(case-conditions-10-mpls-l3vpn-mpls)=
### 配置条件

为每台设备准备唯一 LSR ID，通过 IGP 交换其地址，并在核心接口准备对端连通。

```{toctree}
:maxdepth: 1

mpls/cases/example-1
mpls/cases/example-2
```

(case-verification-10-mpls-l3vpn-mpls)=
### 通用验证

```vortexros-cli
display mpls interface
display mpls lsp
display mpls forwarding-table
```

确认核心接口启用，建立标签路径后核对标签、下一跳和出接口。

[LDP 标签分发](ldp.md)

<span id="observed"></span>

(recorded-result-10-mpls-l3vpn-mpls)=
### 双标签与 TTL 模式的实测结果

四节点实包中，入口 PE 压入传输和 VPN 两层标签。业务经过 IPv4 MPLS 核心，覆盖 VPNv4、6VPE 及中转链路故障恢复。Pipe 和 Uniform 两种 TTL 模式分别验证。

(query-result-10-mpls-l3vpn-mpls)=
### 命令回显实测节选

四节点 MPLS 实测的转发条目节选。将环境改为 Pipe 或 Uniform 后，应在活动标签项中核对 TTL 模式。

```text
<P1> display mpls forwarding-table
path:63  labels:[[19 uniform ttl:0 exp:0]]
lcp-mpls-payload:[6] ip4-fib:1 ip6-fib:1 uniform
```

<span id="precautions"></span>

(section-operator-10-mpls-l3vpn-mpls-4)=
## 注意事项

调整 TTL 传播前说明对诊断跳数的影响。移除核心标签配置前确认上层 L3VPN 或 6PE 依赖。

<p data-legacy-id="id1" class="manual-previous-section" data-section-moved><a href="#overview">介绍</a></p>
<p data-legacy-id="id2" class="manual-previous-section" data-section-moved><a href="#case-conditions-10-mpls-l3vpn-mpls">配置准备</a></p>
<p data-legacy-id="id3" class="manual-previous-section" data-section-moved><a href="#examples">配置案例</a></p>
<p data-legacy-id="id4" class="manual-previous-section" data-section-moved><a href="#case-verification-10-mpls-l3vpn-mpls">验证配置</a></p>
<p data-legacy-id="uniform-pipe-ttl" class="manual-previous-section" data-section-moved><a href="cases/example-2/">比较 Uniform 与 Pipe TTL 行为</a></p>
