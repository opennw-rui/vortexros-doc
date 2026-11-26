---
nav_title: 部署规划
nav_overview: 介绍
nav_feature: true
---


# 部署规划

<span id="overview"></span>

VortexROS 开发版面向 amd64。测试环境可使用 BIOS 或 UEFI 的虚拟机，给系统盘配置稳定的虚拟磁盘序列号，使用 Virtio 网卡。真机应记录引导方式、网卡 PCI 地址、存储设备型号、目标盘和控制台能力。

<span id="principles"></span>

## 工作原理

系统支持从 Live ISO 安装、从签名 TAR 升级，接口可选择 Linux 或 DPDK 模式。

<span id="examples"></span>

## 配置与验证

### 操作流程

![设备硬件和引导方式 → 安装或升级制品 → 维护与验收计划](00-planning/cases.svg)

(case-conditions-installation-00-planning)=
### 配置条件

在准备安装的设备或虚拟机旁记录硬件、安装目标和维护入口。

### 配置步骤

VortexROS 开发版面向 amd64。测试环境可使用 BIOS 或 UEFI 的虚拟机，给系统盘配置稳定的虚拟磁盘序列号，使用 Virtio 网卡。真机应记录引导方式、网卡 PCI 地址、存储设备型号、目标盘和控制台能力。

准备同一镜像系列的 Live ISO、升级 TAR 和对应 SHA-256 校验文件。ISO 用于首次安装。TAR 用于已安装设备的试启动和升级。升级前记录正在运行、默认、下一次启动和后备镜像，并保存可恢复的配置。

数据面有 Linux 和 DPDK 两种接口归属。新环境可以先按 Linux 模式验证管理和路由，再选择适合的 DPDK 端口和 CPU。依赖 VFIO 的设备需要对应的平台 IOMMU 支持。实际队列数、描述符及卸载能力由设备、驱动和工作模式决定。

[控制台](01-management-safety.md) · [安装步骤](03-install-vortexros.md)

(case-verification-installation-00-planning)=
### 验证方法

对照以下命令和预期结果核对设备状态。

安装前核对 ISO 或 TAR 的校验值。启动后执行 `display version`、`display startup`，确认设备使用计划中的镜像与启动方式。

<span id="observed"></span>

(closeout-result-installation-00-planning)=
### 已验证的安装组合

在隔离虚拟机上，r4 已完成 BIOS 虚拟光驱与 UEFI 虚拟 U 盘离线安装。UEFI 本地显示器的实际向导使用 SATA 目标盘，另有使用 Virtio 目标盘的串口实测。真机离线安装另覆盖 UEFI、实体 U 盘、NVMe 和串口。选型时按本机控制台和磁盘类型准备。

<span id="precautions"></span>

## 注意事项

在实际设备确认存储、网卡、IOMMU 和 Console。安装前在设备中核对目标盘和当前数据。
