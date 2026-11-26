# 系统时区

## 功能介绍

时区决定时间、运行状态和日志的本地显示方式。它不改变时间同步所使用的实际时刻。

## 配置准备

用 `clock timezone ?` 查询有效的 IANA 时区名称。

## 配置案例

```vortexros-cli
system-view
clock timezone Asia/Shanghai
commit
return
display clock
save
```

也可在用户视图直接设置时区，此时更改立即提交。用 `undo clock timezone` 恢复 UTC。

## 验证配置

```vortexros-cli
display clock
display logbuffer last 10
```

核对时区与本地时间。需要保留该设置时执行 save。
