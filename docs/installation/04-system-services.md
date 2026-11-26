# 系统服务与状态

启动完成后，通过设备 CLI 核对服务、日志和监听端口。

```text
<VortexROS> display service
<VortexROS> display health
<VortexROS> display logbuffer
<VortexROS> display process listen
```

OpenSSH 负责受管登录，设备本地 AAA 决定访问权限。FRR 和数据面服务由系统按启动依赖编排。NTP 使用配置中的时间源，日志中心可显示接口和协议状态变化。

配置修改经 Candidate 提交并保存。使用整机镜像入口维护受管系统软件。时区、DNS、NTP、SSH 和日志的配置见[系统与访问管理](../operator/02-system-services.md)。
