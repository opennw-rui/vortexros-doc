# CLI、Candidate、commit 与 save

## 视图与帮助

登录后处于用户视图：

```text
<VortexROS> system-view
[~VortexROS] interface Vlanif 100
[~VortexROS-Vlanif100] return
<VortexROS>
```

`?` 显示当前位置的关键字、参数范围或已有对象。Tab 在唯一匹配时补齐词并进入下一词位。命令关键字可以缩写到当前上下文中的唯一前缀。接口视图的二层和三层命令随当前候选配置变化，例如切到 `portswitch` 后，帮助不列出三层地址和 DHCP 命令。

分页默认每 30 行显示 `---more---`：空格下一页、Enter下一行、`q`或 Ctrl+C结束显示。结束分页不会关闭会话，也不会产生多余空行。

输出过滤：

```vortexros-cli
display current-configuration | include ospf
display interface brief | include eth
```

表格过滤保留必要的标题、分隔线和汇总行。

## 每个会话独立的待提交配置

每个登录会话都有独立的待提交配置。另一个会话提交配置后，本会话中互不相关的修改仍可继续提交；如果两个会话修改同一参数、同时删除和修改同一对象，设备会拒绝提交并指出冲突位置。

| 步骤 | 输入命令 | Candidate变化 | commit后效果 | 验证命令 |
|---|---|---|---|---|
| 1 | `system-view` | 进入系统视图并取得当前配置副本 | 无 | `display configuration candidate` |
| 2 | 输入任意配置 | 只改当前会话，提示符出现 `*` | 无 | `display configuration candidate` |
| 3 | `commit` | 检查并应用本会话修改 | 配置正式生效；失败时不会接受未完成的配置 | `display health` |
| 4 | `save` | 不改 Candidate | 原子写入启动配置 | `display configuration storage` |
| 5 | `clear configuration candidate` | 丢弃本会话未提交修改 | 不影响 Running | 再次显示 Candidate |

退出到用户视图时若有未提交配置：

```text
Warning: Uncommitted configurations found, commit them before exiting? [Y(yes)/N(no)/C(cancel)]:
```

`Y`提交，`N`丢弃本会话尚未提交的修改后退出，`C`取消退出。断线或CLI异常退出也只丢弃当前会话的修改，不影响其他用户。

## 提交失败

执行 `commit` 时，设备先检查命令之间的依赖关系，再应用配置并确认运行状态。失败时：

- Candidate保留，便于修改；
- 已经生效的配置不会被未完成的结果覆盖；
- 设备会尽量恢复到提交前状态；
- 无法自动恢复时会产生告警，并在健康状态中指出受影响的功能。

不要反复敲 `commit`掩盖同一错误；先查看：

```vortexros-cli
display health verbose
display alarm active
display service verbose
```

## 保存与重启

已执行 `commit` 但尚未 `save` 的配置，在控制服务或设备重启后不会自动保留。建议先验证业务，再执行 `save`。

可用 `save maintenance.cfg` 写入指定配置文件。使用 `startup saved-configuration ?` 查看配置目录中可用的 `.cfg`，选定后以 `display startup` 核对下一次启动所用文件。授权管理员可用 `display saved-configuration` 读取保存文件的原文。普通 `save` 不保存其他会话的修改。

## 常见错误

| 现象 | 原因 | 处理 |
|---|---|---|
| 输入后提示符仍为 `~` | 命令幂等或被拒绝进入 Candidate | 查看错误和 `display configuration candidate` |
| commit报告规范路径冲突 | 其他会话提交了同一对象 | 使用 `refresh configuration candidate`后处理冲突 |
| quit后仍有空行/会话不退出 | Linux终端或CLI退出路径异常 | 保存`vortexrosd`日志和终端类型信息后进行故障处理 |
| display输出较慢 | 查询对象很多或输出量很大 | 优先使用摘要、对象名和管道过滤缩小范围 |

## 最小配置示例

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

`display this`和`display current-configuration`只显示已经提交的Running。
未提交内容只在`display configuration candidate`中显示；使用`merge`可查看把当前
Candidate合并到Running后的完整预览。
