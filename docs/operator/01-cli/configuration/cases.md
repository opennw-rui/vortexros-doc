---
nav_title: 配置案例
---


# 提交与保存配置 配置案例

## 操作流程

![终端会话 → 候选配置 → 运行配置 → 启动文件](cases.svg)

(case-conditions-01-cli-configuration)=
## 配置条件

维护前确认操作权限，查看正在使用的启动文件。多用户同时修改同一配置可能发生冲突。

## 配置步骤

每个登录会话都有独立的待提交配置。另一个会话提交配置后，本会话中互不相关的修改仍可继续提交；如果两个会话修改同一参数、同时删除和修改同一对象，设备会拒绝提交并指出冲突位置。

| 步骤 | 输入命令 | 待提交配置变化 | commit后效果 | 验证命令 |
|---|---|---|---|---|
| 1 | `system-view` | 进入系统视图并取得当前配置副本 | 无 | `display configuration candidate` |
| 2 | 输入任意配置 | 只改当前会话，提示符出现 `*` | 无 | `display configuration candidate` |
| 3 | `commit` | 检查并应用本会话修改 | 配置正式生效；失败时不会接受未完成的配置 | `display health` |
| 4 | `save` | 不改 待提交配置 | 原子写入启动配置 | `display configuration storage` |
| 5 | `clear configuration candidate` | 丢弃本会话未提交修改 | 不影响 运行配置 | 再次显示 待提交配置 |

退出到用户视图时若有未提交配置：

```text
Warning: Uncommitted configurations found, commit them before exiting? [Y(yes)/N(no)/C(cancel)]:
```

`Y`提交，`N`丢弃本会话尚未提交的修改后退出，`C`取消退出。断线或CLI异常退出也只丢弃当前会话的修改，不影响其他用户。

执行 `commit` 时，设备先检查命令之间的依赖关系，再应用配置并确认运行状态。失败时：

- 待提交配置保留，便于修改；
- 已经生效的配置不会被未完成的结果覆盖；
- 设备会尽量恢复到提交前状态；
- 无法自动恢复时会产生告警，并在健康状态中指出受影响的功能。

不要反复敲 `commit`掩盖同一错误；先查看：

```vortexros-cli
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
## 验证方法

对照以下命令和预期结果核对设备状态。

```vortexros-cli
display configuration candidate
display current-configuration
display startup
display configuration storage
```

提交前确认变更列表，提交后确认实际运行配置已更新。业务复验通过后执行 save，再核对启动文件。
