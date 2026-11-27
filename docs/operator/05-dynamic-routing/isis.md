---
nav_title: IS-IS
nav_overview: 介绍
nav_feature: true
---


(section-operator-05-dynamic-routing-isis-1)=
# IS-IS

<span id="overview"></span>

IS-IS 通过交换链路状态建立 IPv4 或 IPv6 域内路由，可按 Level-1、Level-2 划分邻接范围。

<span id="principles"></span>

(section-operator-05-dynamic-routing-isis-2)=
## 工作原理

IS-IS 在链路上建立邻接并同步链路状态数据库。Level-1 负责区域内路径，Level-2 连接区域间路径。排查时按相同级别核对邻居和前缀，避免把邻接存在当成业务路由已经可用。

IS-IS 支持 Level-1、Level-2 以及 IPv4、IPv6 路由交换。端口可指定邻接级别和开销。

<span id="examples"></span>

(section-operator-05-dynamic-routing-isis-3)=
## 配置与验证

(case-conditions-05-dynamic-routing-isis)=
### 配置条件

为每台设备分配唯一 NET 与 System ID，统一链路两端的 Level、计时和认证。

```{toctree}
:maxdepth: 1

isis/cases/example-1
isis/cases/example-2
```

(case-verification-05-dynamic-routing-isis)=
### 通用验证

```vortexros-cli
display isis peer
display isis route
display ip routing-table
```

确认建立预期级别的邻接，核对远端网段与出接口，再从业务终端测试。

<span id="observed"></span>

实测节选中的物理接口按文档端口编号记为 EthernetX。其他表项保留原始验证值。

(recorded-result-05-dynamic-routing-isis)=
### 运行查询实测节选

实际 IS-IS 邻接回显。测试使用进程 20，查看邻居、接口、级别与状态。

```text
<VortexROS> display isis 20 peer
Peer information for ISIS(20)
                          ------------------------------
 System Id        Interface       Circuit Id   State HoldTime Type PRI
 VortexROS        Ethernet0       2020.2020.2020 Up    28s      2    -
 VortexROS        Ethernet1       2020.2020.2020 Up    29s      2    -
 Total Peer(s): 2
```

<span id="precautions"></span>

(section-operator-05-dynamic-routing-isis-4)=
## 注意事项

为每台设备分配唯一的 NET。对端级别、网络类型和认证应兼容；加入接口的 VPN 应与进程一致。

<p data-legacy-id="id1" class="manual-previous-section" data-section-moved><a href="#overview">介绍</a></p>
<p data-legacy-id="id2" class="manual-previous-section" data-section-moved><a href="#case-conditions-05-dynamic-routing-isis">配置准备</a></p>
<p data-legacy-id="id3" class="manual-previous-section" data-section-moved><a href="#examples">配置案例</a></p>
<p data-legacy-id="id4" class="manual-previous-section" data-section-moved><a href="#case-verification-05-dynamic-routing-isis">验证配置</a></p>
<p data-legacy-id="level-2" class="manual-previous-section" data-section-moved><a href="cases/example-2/">Level-2 双栈邻接与路由</a></p>
