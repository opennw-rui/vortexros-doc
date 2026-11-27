---
nav_title: 提交与保存配置
nav_overview: 介绍
nav_feature: true
---


(section-operator-01-cli-configuration-1)=
# 提交与保存配置

<span id="overview"></span>

编辑会话中的配置后，使用 `commit` 提交，使用 `save` 将当前运行配置写入启动文件。

<span id="principles"></span>

(section-operator-01-cli-configuration-2)=
## 工作原理

每个登录会话持有自己的候选修改。commit 应用候选配置，save 将当前运行配置写入启动文件。

<span id="examples"></span>

(section-operator-01-cli-configuration-3)=
## 配置与验证

(section-operator-01-cli-configuration-4)=
### 操作流程

![终端会话 → 候选配置 → 运行配置 → 启动文件](configuration/cases.svg)

(case-conditions-01-cli-configuration)=
### 配置条件

维护前确认操作权限，查看正在使用的启动文件。多用户同时修改同一配置可能发生冲突。

(section-operator-01-cli-configuration-5)=
### 配置步骤

每个登录会话都有独立的待提交配置。另一个会话提交配置后，本会话中互不相关的修改仍可继续提交；如果两个会话修改同一参数、同时删除和修改同一对象，设备会拒绝提交并指出冲突位置。

| 步骤 | 输入命令 | 待提交配置变化 | commit后效果 | 验证命令 |
|---|---|---|---|---|
| 1 | `system-view` | 进入系统视图并取得当前配置副本 | 无 | `display configuration candidate` |
| 2 | 输入任意配置 | 只改当前会话，提示符出现 `*` | 无 | `display configuration candidate` |
| 3 | `commit` | 检查并提交本会话修改 | 查看提交是否被接受，以及运行状态是否已与配置一致 | `display current-configuration`、`display health` |
| 4 | `save` | 不改 待提交配置 | 原子写入启动配置 | `display configuration storage` |
| 5 | `clear configuration candidate` | 丢弃本会话未提交修改 | 不影响 运行配置 | 再次显示 待提交配置 |

退出到用户视图时若有未提交配置：

```text
Warning: Uncommitted configurations found, commit them before exiting? [Y(yes)/N(no)/C(cancel)]:
```

`Y`提交，`N`丢弃本会话尚未提交的修改后退出，`C`取消退出。断线或CLI异常退出也只丢弃当前会话的修改，不影响其他用户。

执行 `commit` 后，按提示判断配置和业务分别到了哪一步。

| 提交结果 | 设备状态与处理方式 |
| --- | --- |
| 提交被拒绝 | 运行配置保持原状。用 `display configuration candidate` 检查保留的候选修改，按报错修正后重新提交。 |
| 配置已接受，仍待收敛 | 新配置已进入运行配置，相关服务或转发可能还未按新配置工作。用 `display current-configuration` 核对已接受的配置，等设备完成恢复，再查健康和实际业务。 |
| 恢复失败或结果待确认 | 用 `display health verbose` 和 `display alarm active` 确认受影响的服务，再按报错检查实际接口、路由或业务。结果待确认时，先核对运行和启动配置，再决定是否重试。 |

检查配置和实际运行状态时，可以使用：

```vortexros-cli
display current-configuration
display health verbose
display alarm active
display service verbose
```

已执行 `commit` 但尚未 `save` 的配置，在控制服务或设备重启后不会自动保留。建议先验证业务，再执行 `save`。

可用 `save maintenance.cfg` 写入指定配置文件。使用 `startup saved-configuration ?` 查看配置目录中可用的 `.cfg`，选定后以 `display startup` 核对下一次启动所用文件。授权管理员可用 `display saved-configuration` 读取保存文件的原文。普通 `save` 不保存其他会话的修改。

下面的配置修改设备名称。输入后先查看待提交内容，再提交并保存。

```vortexros-config
#
sysname Manual-Test
#
return
```

```vortexros-cli
display configuration candidate
display this
commit
display current-configuration
save
```

`display this`和`display current-configuration`只显示已经提交的运行配置。
未提交内容只在`display configuration candidate`中显示；使用`merge`可查看把当前
待提交配置合并到运行配置后的完整预览。

(case-verification-01-cli-configuration)=
### 验证方法

对照以下命令和预期结果核对设备状态。

```vortexros-cli
display configuration candidate
display current-configuration
display startup
display configuration storage
```

提交前确认变更列表，提交后确认实际运行配置已更新。业务复验通过后执行 save，再核对启动文件。

<span id="observed"></span>

(r4-result-operator-01-cli-configuration)=
### 提交并保存后如何对照代次

首启已落盘的 r4 实测节选。修改配置后可对照三个代次判断生效和保存进度。Actual 赶上 Running 表示运行态同步，Saved 随保存推进。

```text
<VortexROS> display configuration storage
Running generation     : 1
Saved generation       : 1
Actual generation      : 1
Reconcile state        : in-sync
```

<span id="precautions"></span>

(section-operator-01-cli-configuration-6)=
## 注意事项

多会话修改同一对象可能产生冲突。设备重启或关闭前，用 display startup 核对文件，确认启动文件已保存。

<p data-legacy-id="id2" class="manual-previous-section" data-section-moved><a href="#overview">介绍</a></p>
<p data-legacy-id="id3" class="manual-previous-section" data-section-moved><a href="#case-conditions-01-cli-configuration">配置准备</a></p>
<p data-legacy-id="id4" class="manual-previous-section" data-section-moved><a href="#examples">配置案例</a></p>
<p data-legacy-id="id5" class="manual-previous-section" data-section-moved><a href="#case-verification-01-cli-configuration">验证配置</a></p>
