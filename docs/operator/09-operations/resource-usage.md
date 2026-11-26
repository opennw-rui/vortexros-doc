# CPU、内存与数据面资源

## 功能介绍

CPU 和内存查询用于辨别持续负载、短时峰值与数据面资源使用情况。

## 配置准备

在出现性能问题的业务时间段读取状态。使用数据面查询前确认 VPP 已运行。

## 配置案例

```vortexros-cli
display cpu-usage
display cpu-usage history
display memory-usage
```

设备使用 DPDK 时进一步查看 VPP 的运行时明细。

## 验证配置

```vortexros-cli
display cpu-usage vpp verbose
display memory-usage vpp verbose
display dataplane cpu topological
display dataplane memory
```

比较各核心占用、近期历史与 VPP 工作线程及内存分配。按需要对照接口吞吐和丢包变化。
