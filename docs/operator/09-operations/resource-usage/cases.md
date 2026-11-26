---
nav_title: 配置案例
---


# CPU、内存与数据面资源 配置案例

## 操作流程

![业务时间窗 → 设备运行统计 → 对照负载](cases.svg)

(case-conditions-09-operations-resource-usage)=
## 配置条件

在出现性能问题的业务时间段读取状态。使用数据面查询前确认 VPP 已运行。

## 配置步骤

```vortexros-cli
display cpu-usage
display cpu-usage history
display memory-usage
```

设备使用 DPDK 时进一步查看 VPP 的运行时明细。

(case-verification-09-operations-resource-usage)=
## 验证方法

对照以下命令和预期结果核对设备状态。

```vortexros-cli
display cpu-usage vpp verbose
display memory-usage vpp verbose
display dataplane cpu topological
display dataplane memory
```

比较各核心占用、近期历史与 VPP 工作线程及内存分配。按需要对照接口吞吐和丢包变化。
