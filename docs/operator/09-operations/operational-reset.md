---
nav_title: 清理运行状态与服务恢复
nav_overview: 介绍
nav_feature: true
---


(section-operator-09-operations-operational-reset-1)=
# 清理运行状态与服务恢复

<span id="overview"></span>

清理命令用于重置计数或动态表项。恢复命令用于在故障期间重新启动受影响的服务。

<span id="principles"></span>

(section-operator-09-operations-operational-reset-2)=
## 工作原理

可以清理选定的动态表项、计数，或重新启动受管服务。

<span id="examples"></span>

(section-operator-09-operations-operational-reset-3)=
## 配置与验证

(case-conditions-09-operations-operational-reset)=
### 配置条件

选择影响范围最小的操作。清空动态表项或重启服务前确认业务窗口和可用的 Console。

```{toctree}
:maxdepth: 1

operational-reset/cases/example-1
operational-reset/cases/example-2
```

(case-verification-09-operations-operational-reset)=
### 通用验证

```vortexros-cli
display service verbose
display bgp peer
display ip routing-table
display alarm active
```

确认服务状态恢复、BGP 对端重新建立邻接，目标路由与实际转发已恢复。

<span id="observed"></span>

(recorded-result-09-operations-operational-reset)=
(closeout-result-operator-09-operations-operational-reset)=
### 清理运行配置并回放的实测结果

对三节点拓扑清理 Running 后数据面重启。继续加载已经保存的 CFG 并提交时，VPP 无须再次重启，BGP 进程仍保持原实例，启动文件也保留。最终检查到 Running 和 Actual 同步，并重新查询业务对象。

<span id="precautions"></span>

(section-operator-09-operations-operational-reset-4)=
## 注意事项

重置之前保留基线和管理入口。使用最小范围的操作，完成后检查相关协议及转发。

<p data-legacy-id="id2" class="manual-previous-section" data-section-moved><a href="#overview">介绍</a></p>
<p data-legacy-id="id3" class="manual-previous-section" data-section-moved><a href="#case-conditions-09-operations-operational-reset">配置准备</a></p>
<p data-legacy-id="id4" class="manual-previous-section" data-section-moved><a href="#examples">配置案例</a></p>
<p data-legacy-id="id5" class="manual-previous-section" data-section-moved><a href="#case-verification-09-operations-operational-reset">验证配置</a></p>
<p data-legacy-id="vpp" class="manual-previous-section" data-section-moved><a href="cases/example-2/">恢复 VPP 与核对接口状态</a></p>
