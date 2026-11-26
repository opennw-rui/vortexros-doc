---
nav_title: 配置和激活数据面
nav_overview: 介绍
nav_feature: true
---


(section-installation-05-vpp-startup-1)=
# 配置和激活数据面

<span id="overview"></span>

设备可以选择由 Linux 或 DPDK 管理物理端口。配置数据面时还可为所选端口安排队列和处理资源。

<span id="principles"></span>

(section-installation-05-vpp-startup-2)=
## 工作原理

可按 PCI 设备选择 DPDK 模式，并配置队列、CPU 和大页。保存后通过 reset dataplane 激活。

<span id="examples"></span>

(section-installation-05-vpp-startup-3)=
## 配置与验证

(section-installation-05-vpp-startup-4)=
### 操作流程

![设备 PCI 网口 → 配置并激活数据面 → 接口拓扑与转发](05-vpp-startup/cases.svg)

(case-conditions-installation-05-vpp-startup)=
### 配置条件

在系统视图进入 `dataplane`，根据实际 PCI 设备设置所需模式。用 `device ?` 查找可选设备或参数，已有受管设备可通过 `device name Ethernet3` 进入对应视图。先核对网卡驱动、IOMMU 分组、CPU 与内存，再设置队列、描述符或大页。

(section-installation-05-vpp-startup-5)=
### 配置步骤

使用下列示例为所选端口配置 DPDK，并替换为设备上实际支持的 PCI 地址和接口编号。

```vortexros-config
dataplane
 device 0000:03:00.0 name Ethernet 0
  mode dpdk
  queues rx 2 tx 2
  descriptors rx 1024 tx 1024
#
return
```

保存本次数据面配置后，在用户视图执行 `reset dataplane`。该操作可能短时中断相关链路及业务。启用 CPU 隔离等引导参数时，按 CLI 提示安排重启，并在重启后核对线程和实际接口归属。

(case-verification-installation-05-vpp-startup)=
### 验证方法

对照以下命令和预期结果核对设备状态。

```text
<VortexROS> display dataplane interfaces topological
<VortexROS> display interface brief
<VortexROS> display interface hardware offload Ethernet0
```

接口已被 VPP 接管时，在接口摘要及数据面拓扑中核对 DPDK 类型或活动模式。要回到 Linux，调整目标设备模式、提交、保存，再执行 `reset dataplane`，从独立控制台复查驱动、地址和双向转发。

[接口](../operator/interfaces.md) · [二层交换](../operator/layer2-switching.md)

<span id="observed"></span>

(section-installation-05-vpp-startup-6)=
### 接口已接管的实测回显

两块 Virtio 口在空盘启动后绑定 `vfio-pci`。`Desired` 表示配置目标，`Active` 和 `Driver` 用于确认当前运行结果。

```text
<VortexROS> display dataplane interfaces topological
Dataplane interfaces
  PCI            Interface       NUMA     Group    Desired    Active       Driver           RX queues
  0000:00:08.0   Ethernet0       unknown  3        dpdk       DPDK         vfio-pci         1/1
  0000:00:09.0   Ethernet1       unknown  4        dpdk       DPDK         vfio-pci         1/1
```

<span id="precautions"></span>

(section-installation-05-vpp-startup-7)=
## 注意事项

激活可能中断转发和远程登录。核对物理拓扑、队列和 IOMMU，需要时安排重启。

<p data-legacy-id="id2" class="manual-previous-section" data-section-moved><a href="#overview">介绍</a></p>
<p data-legacy-id="id3" class="manual-previous-section" data-section-moved><a href="#case-conditions-installation-05-vpp-startup">配置准备</a></p>
<p data-legacy-id="id4" class="manual-previous-section" data-section-moved><a href="#examples">配置案例</a></p>
<p data-legacy-id="id5" class="manual-previous-section" data-section-moved><a href="#case-verification-installation-05-vpp-startup">验证配置</a></p>
