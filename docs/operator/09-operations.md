# 运行监控与故障处理

- [日志中心](operations/logs.md)。查看实时事件、历史记录和告警。
- [Ping、Tracert 与 MTR 连通性诊断](09-operations/connectivity.md)。Ping 检查端到端可达性，Tracert 查看逐跳路径，MTR 持续观察丢包与延迟。可从指定 VPN 进行诊断。
- [服务状态与监听端口](09-operations/service-health.md)。设备提供服务、健康状态和监听端口查询，可用来区分连通性问题与本地服务未启动。
- [CPU、内存与数据面资源](09-operations/resource-usage.md)。CPU 和内存查询用于辨别持续负载、短时峰值与数据面资源使用情况。
- [清理运行状态与服务恢复](09-operations/operational-reset.md)。清理命令用于重置计数或动态表项。恢复命令用于在故障期间重新启动受影响的服务。
- [配置恢复与出厂重置](09-operations/factory-reset.md)。可单独重置启动配置文件，或恢复整机出厂配置。出厂操作会清理受管账户与服务状态。
- [重启与关机](09-operations/power.md)。系统管理员可在用户视图重启设备或关机。操作会中断所有服务与连接。

```{toctree}
:maxdepth: 1
:hidden:

operations/logs
09-operations/connectivity
09-operations/service-health
09-operations/resource-usage
09-operations/operational-reset
09-operations/factory-reset
09-operations/power
```
