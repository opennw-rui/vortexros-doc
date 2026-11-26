---
nav_title: 重启与关机
nav_overview: 介绍
nav_feature: true
---


(section-operator-09-operations-power-1)=
# 重启与关机

<span id="overview"></span>

系统管理员可在用户视图重启设备或关机。操作会中断所有服务与连接。

<span id="principles"></span>

(section-operator-09-operations-power-2)=
## 工作原理

系统管理员可重启或关闭设备，重启后按下次启动项加载镜像和配置。

<span id="examples"></span>

(section-operator-09-operations-power-3)=
## 配置与验证

(section-operator-09-operations-power-4)=
### 操作流程

![系统管理员 → 保存配置并重启 → Console 与业务检查](power/cases.svg)

(case-conditions-09-operations-power)=
### 配置条件

安排维护窗口，准备能观察开机或恢复供电的独立控制台。若要保留已提交配置，先执行 save。

(section-operator-09-operations-power-5)=
### 配置步骤

以下为重启示例，按 CLI 提示完成确认。若需停止系统且由现场恢复电源，则使用 `poweroff`。

```vortexros-cli
save
display startup
reboot
```

(case-verification-09-operations-power)=
### 验证方法

对照以下命令和预期结果核对设备状态。

```vortexros-cli
display version
display startup
display health
```

重启后确认启动了预期镜像，设备管理和业务能够恢复。关机完成后从 Console 或设备电源状态确认结果。

<span id="observed"></span>

(closeout-result-operator-09-operations-power)=
### 重启后镜像确认的实测结果

r4 经重启启动了所选镜像，完成登录和健康确认后成为默认镜像。一次试启动失败时，自动重启恢复原镜像。按重启前后的实际版本、健康和业务流量复查，见 [升级](../../installation/software-upgrade.md)及[回退](../../installation/software-rollback.md)。

<span id="precautions"></span>

(section-operator-09-operations-power-6)=
## 注意事项

安排维护窗口。提前用独立 Console 确认启动目标、配置保存状态及设备电源恢复方式。

<p data-legacy-id="id2" class="manual-previous-section" data-section-moved><a href="#overview">介绍</a></p>
<p data-legacy-id="id3" class="manual-previous-section" data-section-moved><a href="#case-conditions-09-operations-power">配置准备</a></p>
<p data-legacy-id="id4" class="manual-previous-section" data-section-moved><a href="#examples">配置案例</a></p>
<p data-legacy-id="id5" class="manual-previous-section" data-section-moved><a href="#case-verification-09-operations-power">验证配置</a></p>
