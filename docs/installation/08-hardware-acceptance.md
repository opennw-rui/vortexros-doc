---
nav_title: 真机验收
nav_overview: 介绍
nav_feature: true
---


# 真机验收

<span id="overview"></span>

| 项目 | 通过条件 |
| --- | --- |
| 离线安装 | 从实体 U 盘启动，离线完成验签和安装。拔盘后能从目标盘登录。 |
| 控制台 | 从实际需要的串口或本地显示进入安装器与已安装系统。 |
| 存储与固件 | 识别目标盘和所需控制器，能从目标盘独立引导。 |
| 网络驱动与 DPDK | 核对 PCI、驱动、IOMMU 组与 Active Mode。接管和撤销后验证实际流量。 |
| CPU、内存与队列 | 核对在线 CPU、SMT、NUMA、大页、队列和实际绑定。 |
| 业务与恢复 | 从隔离对端验证静态与动态路由、双向转发、管理登录和重启后恢复。 |
| 升级和回退 | 用签名包从已知版本试启动、确认后回退，并复核配置和业务。 |

<span id="principles"></span>

## 工作原理

首次部署可用 Console、存储、接口、管理与业务路径检查硬件适配。

<span id="examples"></span>

## 配置与验证

### 拓扑

![管理终端或测试对端 → 被测真机 → 业务对端](08-hardware-acceptance/cases.svg)

(case-conditions-installation-08-hardware-acceptance)=
### 配置条件

准备待验硬件、真实管理或业务对端、安装介质和不受该试验影响的 Console。

### 配置步骤

| 项目 | 通过条件 |
| --- | --- |
| 离线安装 | 从实体 U 盘启动，离线完成验签和安装。拔盘后能从目标盘登录。 |
| 控制台 | 从实际需要的串口或本地显示进入安装器与已安装系统。 |
| 存储与固件 | 识别目标盘和所需控制器，能从目标盘独立引导。 |
| 网络驱动与 DPDK | 核对 PCI、驱动、IOMMU 组与 Active Mode。接管和撤销后验证实际流量。 |
| CPU、内存与队列 | 核对在线 CPU、SMT、NUMA、大页、队列和实际绑定。 |
| 业务与恢复 | 从隔离对端验证静态与动态路由、双向转发、管理登录和重启后恢复。 |
| 升级和回退 | 用签名包从已知版本试启动、确认后回退，并复核配置和业务。 |

用 `display interface brief` 和 `display dataplane interfaces topological` 记录接口和归属。保留镜像版本、校验值、端口连接、对端和通过条件，便于重现实测结果。

(case-verification-installation-08-hardware-acceptance)=
### 验证方法

对照以下命令和预期结果核对设备状态。

```vortexros-cli
display version
display startup
display interface brief
display dataplane interfaces topological
```

确认运行及启动镜像与待验制品一致，接口、驱动归属和活动模式与接线及配置相符。逐条核对表中的条件，记录设备型号、镜像校验、两端地址和实际探测结果。

<span id="observed"></span>

(closeout-result-installation-08-hardware-acceptance)=
### 已覆盖的实机读回

一台使用 Intel N5105、四块 I225-V 和 NVMe 的 UEFI 真机经串口确认 r4。把一块备用网卡由 DPDK 切到 Linux，再切回 DPDK，分别实际绑定 igc 和 vfio-pci。读取到单 NUMA、1024 个 2 MiB 大页和各卡独立 IOMMU 组。满负载、物理显示及不同硬件组合按各自设备继续验证。

<span id="precautions"></span>

## 注意事项

维护窗口保留安装介质与配置备份。分别记录安装完成、实际硬件归属和转发结果。
