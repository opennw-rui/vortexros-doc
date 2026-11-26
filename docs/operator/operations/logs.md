# 日志中心

用 `display logbuffer` 查询受管服务和协议事件。可以指定服务、最近记录数或时间范围。例如 `display logbuffer service frr last 30` 显示最近 30 条 FRR 记录。终端输出显示本地时间，跨日期或启动周期时可查询原始 journal。

Console 默认接收实时日志，SSH 默认关闭。用户视图的 `terminal monitor` 和 `undo terminal monitor` 只控制当前终端。要暂停所有终端的实时输出，在系统视图执行 `undo info-center enable` 并提交。历史日志仍可查询。恢复时执行 `info-center enable` 并提交。

[系统、访问与服务](../02-system-services.md) · [诊断与恢复](../09-operations.md)
