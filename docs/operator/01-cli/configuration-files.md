---
nav_title: 配置备份、导入与启动文件
nav_overview: 介绍
nav_feature: true
---


(section-operator-01-cli-configuration-files-1)=
# 配置备份、导入与启动文件

<span id="overview"></span>

可以把当前配置导出备份，也可以载入另一份配置到当前会话，或指定设备下次启动时使用的文件。

<span id="principles"></span>

(section-operator-01-cli-configuration-files-2)=
## 工作原理

可导出运行配置、将文件载入候选配置，以及独立选择下次启动文件。载入、提交和启动选择是不同操作。

<span id="examples"></span>

(section-operator-01-cli-configuration-files-3)=
## 配置与验证

(section-operator-01-cli-configuration-files-4)=
### 操作流程

![当前运行配置 → 导出或载入配置文件 → 候选或下次启动](configuration-files/cases.svg)

(case-conditions-01-cli-configuration-files)=
### 配置条件

用具备权限的管理员登录，确认备份路径可写，输入文件符合当前版本的命令语法。含口令或密钥的备份按凭据材料保管。

(section-operator-01-cli-configuration-files-5)=
### 配置步骤

```vortexros-cli
export configuration /tmp/backup.cfg
save maintenance.cfg
startup saved-configuration maintenance.cfg
display startup
```

需要手工回放配置时，先使用 `load configuration FILE` 查看待提交内容，确认后再执行 commit。按实际路径替换 FILE。

(case-verification-01-cli-configuration-files)=
### 验证方法

对照以下命令和预期结果核对设备状态。

```vortexros-cli
display configuration candidate
display configuration storage
display startup
```

核对待应用差异、保存位置和下次启动文件。要复查内容，可用具备权限的账户执行 display saved-configuration。

<span id="observed"></span>

(r4-result-operator-01-cli-configuration-files)=
### 空盘首启后配置存储的实测回显

r4 空盘首启后的实际配置来源与三个代次。例中下一次启动继续使用选定 CFG，运行、已保存和实际状态的代次相同。

```text
<VortexROS> display configuration storage
Running generation     : 1
Saved generation       : 1
Actual generation      : 1
Reconcile state        : in-sync
Default config file    : /vortexros/config/config.cfg
Selected startup CFG   : /vortexros/config/config.cfg
```

<span id="precautions"></span>

(section-operator-01-cli-configuration-files-6)=
## 注意事项

在切换启动文件前检查文件名和内容。保存含密钥或本地用户校验值的配置时，按凭据材料管理。

需要把启动配置与设备身份一并备份时，使用{ref}`加密设备备份 <encrypted-device-backup>`。

<p data-legacy-id="id2" class="manual-previous-section" data-section-moved><a href="#overview">介绍</a></p>
<p data-legacy-id="id3" class="manual-previous-section" data-section-moved><a href="#case-conditions-01-cli-configuration-files">配置准备</a></p>
<p data-legacy-id="id4" class="manual-previous-section" data-section-moved><a href="#examples">配置案例</a></p>
<p data-legacy-id="id5" class="manual-previous-section" data-section-moved><a href="#case-verification-01-cli-configuration-files">验证配置</a></p>
