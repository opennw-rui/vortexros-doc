---
nav_title: CPU、内存与数据面资源
nav_overview: 介绍
nav_feature: true
---


(section-operator-09-operations-resource-usage-1)=
# CPU、内存与数据面资源

<span id="overview"></span>

CPU 和内存查询用于辨别持续负载、短时峰值与数据面资源使用情况。

<span id="principles"></span>

(section-operator-09-operations-resource-usage-2)=
## 工作原理

显示 CPU、历史占用、内存和 VPP 运行资源，也可查看 CPU 与 NUMA 拓扑。

<span id="examples"></span>

(section-operator-09-operations-resource-usage-3)=
## 配置与验证

(section-operator-09-operations-resource-usage-4)=
### 操作流程

![业务时间窗 → 设备运行统计 → 对照负载](resource-usage/cases.svg)

(case-conditions-09-operations-resource-usage)=
### 配置条件

在出现性能问题的业务时间段读取状态。使用数据面查询前确认 VPP 已运行。

(section-operator-09-operations-resource-usage-5)=
### 配置步骤

```vortexros-cli
display cpu-usage
display cpu-usage history
display memory-usage
```

设备使用 DPDK 时进一步查看 VPP 的运行时明细。

(case-verification-09-operations-resource-usage)=
### 验证方法

对照以下命令和预期结果核对设备状态。

```vortexros-cli
display cpu-usage vpp verbose
display memory-usage vpp verbose
display dataplane cpu topological
display dataplane memory
```

比较各核心占用、近期历史与 VPP 工作线程及内存分配。按需要对照接口吞吐和丢包变化。

<span id="observed"></span>

(r4-result-operator-09-operations-resource-usage)=
### CPU 和内存的实测回显

r4 虚拟机在启动后不久查询。当前和五秒利用率已有读数，一分钟、五分钟的采样窗口尚未填满。内存量和比例以当前设备为准。

```text
<VortexROS> display cpu-usage
CPU utilization statistics at 2026-11-26 20:57:44.857
System CPU use rate is : 8%
CPU utilization for five seconds: 11%   one minute: --   five minutes: --
Max CPU Usage : 26%
Max CPU Usage Stat. Time : 2026-11-26 20:57:38.857
```

```text
<VortexROS> display memory-usage
Memory utilization statistics at 2026-11-26 20:57:45.466
System Total Memory Is: 5428592 kbytes
Total Memory Used Is: 2099168 kbytes
Memory Using Percentage Is: 39%
```

<span id="precautions"></span>

(section-operator-09-operations-resource-usage-6)=
## 注意事项

比较结果时采用一致的时间窗和流量负载。仅在 VPP 运行时查看相应数据面统计。

<p data-legacy-id="id1" class="manual-previous-section" data-section-moved><a href="#overview">介绍</a></p>
<p data-legacy-id="id2" class="manual-previous-section" data-section-moved><a href="#case-conditions-09-operations-resource-usage">配置准备</a></p>
<p data-legacy-id="id3" class="manual-previous-section" data-section-moved><a href="#examples">配置案例</a></p>
<p data-legacy-id="id4" class="manual-previous-section" data-section-moved><a href="#case-verification-09-operations-resource-usage">验证配置</a></p>
