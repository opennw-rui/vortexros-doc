---
nav_title: 启用终端监视及全局日志控制
---


# 启用终端监视及全局日志控制

## 操作流程

![接口或受管服务事件 → 本机日志中心 → 当前终端与历史查询](example-1.svg)

## 配置条件

先确定是临时调整当前终端，还是调整所有终端。查询历史记录可使用下面的 display 命令。

在 SSH 用户视图开启当前终端的实时显示。用 `undo terminal monitor` 仅关闭当前终端。

## 配置步骤

```vortexros-cli
terminal monitor
```

如需暂停所有终端的实时显示，在系统视图执行下列命令。历史日志仍可查询。用 `info-center enable` 并提交恢复。

```text
system-view
undo info-center enable
commit
return
```

## 验证方法

对照以下命令和预期结果核对设备状态。

```vortexros-cli
display logbuffer last 20
```

在测试控制台触发并恢复一个无业务接口状态。启用监视后应见实时记录，全局暂停后历史日志仍能查询。
