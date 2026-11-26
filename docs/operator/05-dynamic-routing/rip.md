---
nav_title: RIP（IPv4）
nav_overview: 介绍
nav_feature: true
---


(section-operator-05-dynamic-routing-rip-1)=
# RIP（IPv4）

<span id="overview"></span>

RIP 根据跳数交换 IPv4 路由，适用于已有 RIP 设备的小型网络。

<span id="principles"></span>

(section-operator-05-dynamic-routing-rip-2)=
## 工作原理

RIP 用到目的地的跳数计算度量。相邻设备周期通告，路由也可能因超时失效。需要核对接收接口、选中的下一跳和跳数是否与拓扑一致。

RIPv2 用跳数发布 IPv4 路由。可调整更新计时、默认开销及等价路径数。

<span id="examples"></span>

(section-operator-05-dynamic-routing-rip-3)=
## 配置与验证

(case-conditions-05-dynamic-routing-rip)=
### 配置条件

在同一 IPv4 链路上配置兼容的 RIP 版本并准备要通告的网段。

```{toctree}
:maxdepth: 1

rip/cases/example-1
rip/cases/example-2
```

(case-verification-05-dynamic-routing-rip)=
### 通用验证

```vortexros-cli
display rip 1 route
display ip routing-table
```

确认邻居通告的网段与跳数，使用业务终端确认远端网络可达。

<span id="observed"></span>

(recorded-result-05-dynamic-routing-rip)=
### 运行查询实测节选

三节点拓扑实际 RIP 路由回显节选。测试采用 RIP 进程 10，实际地址与案例可不同。

```text
<VortexROS> display rip 10 route
RIP Process 10 Routing Table
Destination/Mask                            Cost  NextHop                                  Interface/Source       Tag  TimeLeft
10.255.1.1/32                               2     10.201.12.1                              10.201.12.1            0    00:24
10.255.3.3/32                               2     10.201.23.3                              10.201.23.3            0    00:29
172.30.41.1/32                              2     10.201.12.1                              10.201.12.1            0    00:24
192.0.2.0/30                                2     10.201.12.1                              10.201.12.1            0    00:24
192.0.2.4/30                                2     10.201.12.1                              10.201.12.1            0    00:24
Total Routes: 5
```

<span id="precautions"></span>

(section-operator-05-dynamic-routing-rip-4)=
## 注意事项

network 使用主类网络地址，匹配的接口会参与路由交换。核对真实通告范围，并控制无须建立邻居的接口。

<p data-legacy-id="id1" class="manual-previous-section" data-section-moved><a href="#overview">介绍</a></p>
<p data-legacy-id="id2" class="manual-previous-section" data-section-moved><a href="#case-conditions-05-dynamic-routing-rip">配置准备</a></p>
<p data-legacy-id="id3" class="manual-previous-section" data-section-moved><a href="#examples">配置案例</a></p>
<p data-legacy-id="id4" class="manual-previous-section" data-section-moved><a href="#case-verification-05-dynamic-routing-rip">验证配置</a></p>
<p data-legacy-id="ripv2-ipv4" class="manual-previous-section" data-section-moved><a href="cases/example-2/">RIPv2 两端交换 IPv4 前缀</a></p>
