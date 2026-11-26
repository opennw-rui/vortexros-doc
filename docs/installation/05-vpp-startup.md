# 配置和激活数据面

在系统视图进入 `dataplane`，根据实际 PCI 设备设置所需模式。用 `device ?` 查找可选设备或参数，已有受管设备可通过 `device name` 进入对应视图。先核对网卡驱动、IOMMU 分组、CPU 与内存，再设置队列、描述符或大页。

保存本次数据面配置后，在用户视图执行 `reset dataplane`。该操作可能短时中断相关链路及业务。启用 CPU 隔离等引导参数时，按 CLI 提示安排重启，并在重启后核对线程和实际接口归属。

```text
<VortexROS> display dataplane interfaces topological
<VortexROS> display interface brief
<VortexROS> display interface hardware offload Ethernet0
```

接口已被 VPP 接管时，在接口摘要及数据面拓扑中核对 DPDK 类型或活动模式。要回到 Linux，调整目标设备模式、提交、保存，再执行 `reset dataplane`，从独立控制台复查驱动、地址和双向转发。

[接口、聚合与二层](../operator/03-interfaces-l2.md)
