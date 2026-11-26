# 日志中心

## 功能介绍

日志中心用于查看接口、Vlanif、Vbdif、动态路由邻居、BFD 和 VRRP 的状态变化，也可按服务查询设备日志。Console 默认接收实时日志，SSH 默认关闭。

## 配置准备

先确定是临时调整当前终端，还是调整所有终端。查询历史记录可使用下面的 display 命令。

## 配置案例

在 SSH 用户视图开启当前终端的实时显示。用 `undo terminal monitor` 仅关闭当前终端。

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

## 验证配置

```vortexros-cli
display logbuffer
display logbuffer service frr last 30
display logbuffer last 20 since 15
display alarm active
```

核对事件涉及的接口或邻居、状态及本地时间。跨日期或跨启动周期时，在获准的系统维护环境查看带日期的 journal。
