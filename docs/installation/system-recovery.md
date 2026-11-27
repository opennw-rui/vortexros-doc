---
nav_title: 通过控制台进入救援
nav_overview: 介绍
nav_feature: true
---


(section-installation-system-recovery-1)=
# 通过控制台进入救援

<span id="overview"></span>

正常系统启动或管理入口不可用时，可从已安装系统的引导菜单进入救援，确认启动镜像和设备配置。

<span id="principles"></span>

(section-installation-system-recovery-2)=
## 工作原理

可在 GRUB 进入本地显示或串口救援。使用救援入口确认镜像和配置。

<span id="examples"></span>

(section-installation-system-recovery-3)=
## 配置与验证

(section-installation-system-recovery-4)=
### 操作流程

![独立 Console → GRUB 救援入口 → 恢复并验证正常启动](system-recovery/cases.svg)

(case-conditions-installation-system-recovery)=
### 配置条件

准备本地键盘和显示器，或可以看到 GRUB 的串口。若需要保留设备业务配置，先在可用环境导出并备份。

(section-installation-system-recovery-5)=
### 配置步骤

1. 重启设备并等待 GRUB 出现。保留系统盘，移除安装介质。
2. 根据连接选择 `VortexROS recovery (local display)` 或 `VortexROS recovery (serial)`。
3. 按 Console 提示核对镜像与配置。需要保留当前日志或已选择的启动配置时，参见[脱敏支持包与加密备份](../operator/09-operations/backup-support.md)中的救援命令。
4. 确认镜像与配置选项后返回正常启动。

(case-verification-installation-system-recovery)=
### 验证方法

对照以下命令和预期结果核对设备状态。

恢复后从 Console 登录常规 CLI。

```vortexros-cli
display startup
display health
display users
```

核对启动的镜像与配置文件，再验证正常账户登录和业务路径。需要清除设备设置时，参见[配置恢复与出厂重置](../operator/09-operations/factory-reset.md)。

<span id="observed"></span>

(closeout-result-installation-system-recovery)=
### 串口救援的实测结果

从已安装盘选择串口救援后，操作员完成认证，并导出了该次救援的系统日志。实际导出文件权限为 0600，读到救援服务的启动记录。异常试启动自动回退的完整状态见 [软件回退](software-rollback.md)。

<span id="precautions"></span>

(section-installation-system-recovery-6)=
## 注意事项

遇到配置损坏时先保留可读的备份。恢复后验证常用账户、服务与实际业务。

<p data-legacy-id="id2" class="manual-previous-section" data-section-moved><a href="#overview">介绍</a></p>
<p data-legacy-id="id3" class="manual-previous-section" data-section-moved><a href="#case-conditions-installation-system-recovery">配置准备</a></p>
<p data-legacy-id="id4" class="manual-previous-section" data-section-moved><a href="#examples">配置案例</a></p>
<p data-legacy-id="id5" class="manual-previous-section" data-section-moved><a href="#case-verification-installation-system-recovery">验证恢复</a></p>
