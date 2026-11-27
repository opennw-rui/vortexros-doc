---
nav_title: RIPng（IPv6）
nav_overview: 介绍
nav_feature: true
---


(section-operator-05-dynamic-routing-ripng-1)=
# RIPng（IPv6）

<span id="overview"></span>

RIPng 根据跳数交换 IPv6 路由。可在指定三层接口接收和发送路由更新。

<span id="principles"></span>

(section-operator-05-dynamic-routing-ripng-2)=
## 工作原理

RIPng 在 IPv6 接口上交换路由，路径度量仍为跳数。查看学习到的前缀时应同时核对其出接口和链路本地下一跳，再用 IPv6 流量验证双向可达。

RIPng 根据跳数发布 IPv6 路由，可在独立 VPN 内运行。

<span id="examples"></span>

(section-operator-05-dynamic-routing-ripng-3)=
## 配置与验证

(case-conditions-05-dynamic-routing-ripng)=
### 配置条件

准备已配置 IPv6 的链路。如果使用 BLUE，先创建并配置相应的 IPv6 VPN 实例。

```{toctree}
:maxdepth: 1

ripng/cases/example-1
ripng/cases/example-2
```

(case-verification-05-dynamic-routing-ripng)=
### 通用验证

```vortexros-cli
display ripng 2 route
display ipv6 routing-table vpn-instance BLUE
```

确认学到的前缀出现在对应 VPN 和接口。撤销进程后，相关学到的路由应退出路由表。

<span id="observed"></span>

实测节选中的物理接口按文档端口编号记为 EthernetX。其他表项保留原始验证值。

(recorded-result-05-dynamic-routing-ripng)=
### 运行查询实测节选

三节点拓扑实际 RIPng 路由回显，使用进程 11。核对前缀、跳数和所在接口。

```text
<VortexROS> display ripng 11 route
RIPng Process 11 Routing Table
Destination/Mask                            Cost  NextHop                                  Interface/Source       Tag  TimeLeft
2001:db8:ffff::1/128                        2     fe80::ff:fe01:1201                       Ethernet0              0    00:22
2001:db8:ffff::3/128                        2     fe80::ff:fe03:2303                       Ethernet1              0    00:19
Total Routes: 2
```

<span id="precautions"></span>

(section-operator-05-dynamic-routing-ripng-4)=
## 注意事项

核对启用的 IPv6 接口、链路本地下一跳及 VPN。变更通告后等待更新再查询。

<p data-legacy-id="id1" class="manual-previous-section" data-section-moved><a href="#overview">介绍</a></p>
<p data-legacy-id="id2" class="manual-previous-section" data-section-moved><a href="#case-conditions-05-dynamic-routing-ripng">配置准备</a></p>
<p data-legacy-id="id3" class="manual-previous-section" data-section-moved><a href="#examples">配置案例</a></p>
<p data-legacy-id="id5" class="manual-previous-section" data-section-moved><a href="#case-verification-05-dynamic-routing-ripng">验证配置</a></p>
<p data-legacy-id="id4" class="manual-previous-section" data-section-moved><a href="cases/example-2/">RIPng 两端交换 IPv6 环回</a></p>
