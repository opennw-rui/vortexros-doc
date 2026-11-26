---
nav_title: OSPFv3（IPv6）
nav_overview: 介绍
nav_feature: true
---


(section-operator-05-dynamic-routing-ospfv3-1)=
# OSPFv3（IPv6）

<span id="overview"></span>

OSPFv3 为 IPv6 域内业务学习路由，在指定链路的三层接口建立邻居。

<span id="principles"></span>

(section-operator-05-dynamic-routing-ospfv3-2)=
## 工作原理

OSPFv3 使用 IPv6 链路本地地址建立邻接，发布待转发的 IPv6 前缀。对端链路本地地址只在所在接口有效，因此路由表应同时显示正确的一跳地址和出接口。Full 及实包分别证明邻接和业务。

按三层接口建立 IPv6 邻接，可用独立 VPN 的进程和不同区域组织路由。

<span id="examples"></span>

(section-operator-05-dynamic-routing-ospfv3-3)=
## 配置与验证

(case-conditions-05-dynamic-routing-ospfv3)=
### 配置条件

准备 IPv6 上联、非重复的 Router ID 和两端相同的区域。

```{toctree}
:maxdepth: 1

ospfv3/cases/example-1
ospfv3/cases/example-2
```

(case-verification-05-dynamic-routing-ospfv3)=
### 通用验证

```vortexros-cli
display ospfv3 peer
display ospfv3 routing
display ipv6 routing-table
```

确认邻接建立、远端 IPv6 前缀可见并在相应实例中从端点完成测试。

<span id="observed"></span>

(recorded-result-05-dynamic-routing-ospfv3)=
### 邻接建成、断开和恢复的实测结果

测试中在主路径上制造邻接故障，再恢复链路。看同一个 Router ID 与接口的状态转换，最后一条 `Full` 表示邻接重新同步完成。以下为实际协议事件节选。

```text
2026/11/26 06:15:32 OSPF6: [GHN28-AMRE7] AdjChg: Nbr 2.2.2.2(default) on 2.2.2.2%host-p1e12: Loading -> Full (LoadingDone)
2026/11/26 06:15:45 OSPF6: [GHN28-AMRE7] AdjChg: Nbr 2.2.2.2(default) on 2.2.2.2%host-p1e12: Loading -> Full (LoadingDone)
2026/11/26 06:15:57 OSPF6: [GHN28-AMRE7] AdjChg: Nbr 2.2.2.2(default) on 2.2.2.2%host-p1e12: Loading -> Full (LoadingDone)
2026/11/26 06:15:45 OSPF6: [GHN28-AMRE7] AdjChg: Nbr 2.2.2.2(default) on 2.2.2.2%host-p1e12: Full -> Down (InactivityTimer)
```

(section-operator-05-dynamic-routing-ospfv3-4)=
### 运行查询实测节选

三节点 IPv6 OSPF 的实际邻接回显节选。对端 Router ID、接口和状态须与拓扑相符。

```text
<VortexROS> display ospfv3 1 peer brief
OSPFv3 Process (1)

Neighbor ID     Pri  State          Dead Time  Interface
1.1.1.1         0    Full/PointToPoint 00:00:10   host-p2e12
3.3.3.3         0    Full/PointToPoint 00:00:11   host-p2e23
```

<span id="precautions"></span>

(section-operator-05-dynamic-routing-ospfv3-5)=
## 注意事项

检查两端 IPv6 与区域，VPN 内接口和进程必须一致。同一 VPN 仅建立一个 OSPFv3 进程。

<p data-legacy-id="id1" class="manual-previous-section" data-section-moved><a href="#overview">介绍</a></p>
<p data-legacy-id="id2" class="manual-previous-section" data-section-moved><a href="#case-conditions-05-dynamic-routing-ospfv3">配置准备</a></p>
<p data-legacy-id="id3" class="manual-previous-section" data-section-moved><a href="#examples">配置案例</a></p>
<p data-legacy-id="id5" class="manual-previous-section" data-section-moved><a href="#case-verification-05-dynamic-routing-ospfv3">验证配置</a></p>
<p data-legacy-id="id4" class="manual-previous-section" data-section-moved><a href="cases/example-2/">双节点 OSPFv3 发布 IPv6 环回</a></p>
