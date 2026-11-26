---
nav_title: LDP 标签分发
nav_overview: 介绍
nav_feature: true
---


(section-operator-10-mpls-l3vpn-ldp-1)=
# LDP 标签分发

<span id="overview"></span>

LDP 在 MPLS 核心的邻居之间交换标签绑定，供目的前缀建立标签转发路径。

<span id="principles"></span>

(section-operator-10-mpls-l3vpn-ldp-2)=
## 工作原理

LDP 邻接和会话交换的标签绑定与底层路由共同决定可用转发路径。邻居已建立但没有目标前缀的标签时，应先检查 IGP 可达性和该前缀的标签。

LDP 交换标签绑定，配合底层 IGP 建立到远端 LSR 的标签转发路径。

<span id="examples"></span>

(section-operator-10-mpls-l3vpn-ldp-3)=
## 配置与验证

(case-conditions-10-mpls-l3vpn-ldp)=
### 配置条件

先规划两端 LSR ID、核心三层链路和 IGP 路由。以下配置包含 PE1 的接口、IGP 和 LDP。

```{toctree}
:maxdepth: 1

ldp/cases/example-1
ldp/cases/example-2
```

(case-verification-10-mpls-l3vpn-ldp)=
### 通用验证

```vortexros-cli
display mpls ldp interface
display mpls ldp peer
display mpls ldp binding
display mpls forwarding-table
```

确认两端 LDP 邻接已建立，远端 LSR ID 的标签可以从下一跳送出。没有业务引用时再撤销接口 LDP。

<span id="observed"></span>

(recorded-result-10-mpls-l3vpn-ldp)=
### 四节点 LDP 的实测结果

在四节点 MPLS 环网中验证 LDP 建邻及传输标签。环网一条路径故障时，另一条路径接管转发。验证时需将 LDP 邻居状态、活动标签和实际报文三者对应起来。

(query-result-10-mpls-l3vpn-ldp)=
### 命令回显实测节选

四节点线性网络中间设备 P2 的 LDP 查询。两端均进入 OPERATIONAL。邻居建立后可沿同一核心校验标签绑定。

```text
<P2> display mpls ldp peer
AF   ID              State       Remote Address  Uptime
ipv4 1.1.1.1         OPERATIONAL 1.1.1.1         00:00:08
ipv4 3.3.3.3         OPERATIONAL 3.3.3.3         00:01:15
```

<span id="precautions"></span>

(section-operator-10-mpls-l3vpn-ldp-4)=
## 注意事项

先确保 IGP 能到达对端环回与核心链路，再核对 LDP 状态与标签表。

<p data-legacy-id="id1" class="manual-previous-section" data-section-moved><a href="#overview">介绍</a></p>
<p data-legacy-id="id2" class="manual-previous-section" data-section-moved><a href="#case-conditions-10-mpls-l3vpn-ldp">配置准备</a></p>
<p data-legacy-id="id3" class="manual-previous-section" data-section-moved><a href="#examples">配置案例</a></p>
<p data-legacy-id="id5" class="manual-previous-section" data-section-moved><a href="#case-verification-10-mpls-l3vpn-ldp">验证配置</a></p>
<p data-legacy-id="id4" class="manual-previous-section" data-section-moved><a href="cases/example-2/">两端建立标签路径</a></p>
