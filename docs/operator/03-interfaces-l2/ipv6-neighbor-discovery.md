---
nav_title: IPv6 邻居发现与静态邻居
nav_overview: 介绍
nav_feature: true
---


(section-operator-03-interfaces-l2-ipv6-neighbor-discovery-1)=
# IPv6 邻居发现与静态邻居

<span id="overview"></span>

IPv6 邻居发现用于解析相邻节点的链路层地址。可为已知对端设置静态映射，或按需要调整数据面邻居表容量和老化时间。

<span id="principles"></span>

(section-operator-03-interfaces-l2-ipv6-neighbor-discovery-2)=
## 工作原理

IPv6 用邻居请求与通告解析同链路地址、维护可达性。解析状态和三层路由分别检查。存在一条路由时，下一跳的邻居仍可能未解析或已失效。

可按接口和 VPN 查询动态 IPv6 邻居，并可配置静态 IPv6 到 MAC 映射及邻居表老化。

<span id="examples"></span>

(section-operator-03-interfaces-l2-ipv6-neighbor-discovery-3)=
## 配置与验证

(case-conditions-03-interfaces-l2-ipv6-neighbor-discovery)=
### 配置条件

选定三层接口并确认对端 IPv6 和单播 MAC 地址。动态表项由流量学习。

```{toctree}
:maxdepth: 1

ipv6-neighbor-discovery/cases/example-1
ipv6-neighbor-discovery/cases/example-2
```

(case-verification-03-interfaces-l2-ipv6-neighbor-discovery)=
### 通用验证

```vortexros-cli
display ipv6 nd
display ipv6 neighbors static
display ipv6 neighbors interface Vlanif10
```

确认老化时间、容量和回收策略符合预期。静态列表应出现配置的 IPv6、MAC 与接口。使用实际流量核对转发。

<span id="observed"></span>

(recorded-result-03-interfaces-l2-ipv6-neighbor-discovery)=
(result-operator-03-interfaces-l2-ipv6-neighbor-discovery)=
### 静态邻居增删的实测结果

在开发镜像的三节点 IPv6 拓扑上验证静态邻居可通过配置添加和撤销。与动态项区分时，应核对目标 IPv6、链路层地址、接口及条目来源，再从相应接口发包确认。

<span id="precautions"></span>

(section-operator-03-interfaces-l2-ipv6-neighbor-discovery-4)=
## 注意事项

静态条目要关联已启用 IPv6 的三层接口。跨 VPN 时先核对接口归属；静态条目不会随动态回收移除。

<p data-legacy-id="id1" class="manual-previous-section" data-section-moved><a href="#overview">介绍</a></p>
<p data-legacy-id="id2" class="manual-previous-section" data-section-moved><a href="#case-conditions-03-interfaces-l2-ipv6-neighbor-discovery">配置准备</a></p>
<p data-legacy-id="id3" class="manual-previous-section" data-section-moved><a href="#examples">配置案例</a></p>
<p data-legacy-id="id4" class="manual-previous-section" data-section-moved><a href="#case-verification-03-interfaces-l2-ipv6-neighbor-discovery">验证配置</a></p>
<p data-legacy-id="vpn" class="manual-previous-section" data-section-moved><a href="cases/example-2/">按 VPN 或接口定位邻居</a></p>
