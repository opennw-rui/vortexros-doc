---
nav_title: OSPF（IPv4）
nav_overview: 介绍
nav_feature: true
---


(section-operator-05-dynamic-routing-ospf-1)=
# OSPF（IPv4）

<span id="overview"></span>

OSPF 为 IPv4 域内路由交换链路状态，可用多区域组织网络。

<span id="principles"></span>

(section-operator-05-dynamic-routing-ospf-2)=
## 工作原理

OSPF 路由器通过 Hello 发现同链路邻居，再在区域内同步链路状态。邻接完成后使用 SPF 选路。多接入网络中部分邻居可停留在 2-Way，判断时结合网络类型与 DR 角色。

支持通过 area 的 network 或接口命令激活。不同区域类型和接口开销用于控制拓扑与路由发布。

<span id="examples"></span>

(section-operator-05-dynamic-routing-ospf-3)=
## 配置与验证

(case-conditions-05-dynamic-routing-ospf)=
### 配置条件

为每台路由器选独立的 Router ID。检查链路地址、区域、网络类型和计时两端一致。

```{toctree}
:maxdepth: 1

ospf/cases/example-1
ospf/cases/example-2
ospf/cases/example-3
ospf/cases/area-zero-adjacency
ospf/cases/vpn-adjacency
```

(case-verification-05-dynamic-routing-ospf)=
### 通用验证

```vortexros-cli
display ospf peer brief
display ip routing-table protocol ospf
```

核对邻接状态、学习的前缀及下一跳，并从下游测试连通性。

(section-operator-05-dynamic-routing-ospf-4)=
### 验证与撤销

```vortexros-cli
display ospf 1 brief
display ospf 1 peer brief
display ospf 1 peer 10.0.0.2
display ospf 1 interface
display ospf 1 lsdb
display ospf 1 routing
```

`display ospf peer brief`按以下顺序显示，Interface位于Neighbor id左侧：

```text
Area Id    Pri  Up Time   Dead Time  Interface   Neighbor id  State
0.0.0.0      1  00:12:31  00:00:38   Vlanif12    10.0.0.2     Full
```

修改与删除示例：

```text
interface Vlanif 12
 undo ospf dr-priority
 undo ospf network-type
 undo ospf enable 1
undo ospf 1
commit
```

撤销接口激活只影响该接口；删除进程会撤销该进程的全部邻居和路由。

<span id="observed"></span>

(recorded-result-05-dynamic-routing-ospf)=
### 运行查询实测节选

三节点 IPv4 OSPF 实测。P2 在区域 0 中与 1.1.1.1 和 3.3.3.3 都到达 Full。

```text
<VortexROS> display ospf 1 peer brief
OSPF Process 1 with Router ID 2.2.2.2
                  Peer Statistic Information
 ---------------------------------------------------------------------------------------------
 Area Id    Pri   Up Time        Dead Time       Interface         Neighbor id      State

 0.0.0.0    110   5.748s         9.239s          host-p2e12        1.1.1.1          Full
 0.0.0.0    110   2.830s         10.855s         host-p2e23        3.3.3.3          Full
 ---------------------------------------------------------------------------------------------
 Total Peer(s):     2
```

<span id="precautions"></span>

(section-operator-05-dynamic-routing-ospf-5)=
## 注意事项

同一进程不要混用两种接口激活方式。邻居未到 Full 时，先核对两端 Area、计时、网络类型和 MTU。

(section-operator-05-dynamic-routing-ospf-6)=
### 验证与撤销

```vortexros-cli
display ospf 1 brief
display ospf 1 peer brief
display ospf 1 peer 10.0.0.2
display ospf 1 interface
display ospf 1 lsdb
display ospf 1 routing
```

`display ospf peer brief`按以下顺序显示，Interface位于Neighbor id左侧：

```text
Area Id    Pri  Up Time   Dead Time  Interface   Neighbor id  State
0.0.0.0      1  00:12:31  00:00:38   Vlanif12    10.0.0.2     Full
```

修改与删除示例：

```text
interface Vlanif 12
 undo ospf dr-priority
 undo ospf network-type
 undo ospf enable 1
undo ospf 1
commit
```

撤销接口激活只影响该接口；删除进程会撤销该进程的全部邻居和路由。

<p data-legacy-id="id1" class="manual-previous-section" data-section-moved><a href="#overview">介绍</a></p>
<p data-legacy-id="id2" class="manual-previous-section" data-section-moved><a href="#case-conditions-05-dynamic-routing-ospf">配置准备</a></p>
<p data-legacy-id="id3" class="manual-previous-section" data-section-moved><a href="#examples">配置案例</a></p>
<p data-legacy-id="id6" class="manual-previous-section" data-section-moved><a href="#case-verification-05-dynamic-routing-ospf">验证配置</a></p>
<p data-legacy-id="id5" class="manual-previous-section" data-section-moved><a href="#precautions">验证与撤销</a></p>
<p data-legacy-id="areanetwork" class="manual-previous-section" data-section-moved><a href="cases/example-1/">使用area下的network激活</a></p>
<p data-legacy-id="id4" class="manual-previous-section" data-section-moved><a href="cases/example-2/">使用接口命令激活</a></p>
<p data-legacy-id="stubnssa" class="manual-previous-section" data-section-moved><a href="cases/example-3/">Stub、NSSA与区域汇总</a></p>
<p data-legacy-id="area-0" class="manual-previous-section" data-section-moved><a href="cases/area-zero-adjacency/">两台设备建立 Area 0 邻接</a></p>
<p data-legacy-id="vpn-ospf" class="manual-previous-section" data-section-moved><a href="cases/vpn-adjacency/">在管理 VPN 内建立独立 OSPF 邻居</a></p>
