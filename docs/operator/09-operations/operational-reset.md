# 清理运行状态与服务恢复

## 功能介绍

清理命令用于重置计数或动态表项。恢复命令用于在故障期间重新启动受影响的服务。

## 配置准备

选择影响范围最小的操作。清空动态表项或重启服务前确认业务窗口和可用的 Console。

## 配置案例

为复查 NAT 命中，可清理策略计数，再重复对应的流量。

```vortexros-cli
clear nat-policy counters
display nat-policy statistics
```

如已确认 BGP 服务需要恢复，执行下列命令并按提示确认。

```vortexros-cli
reset service bgp
```

## 验证配置

```vortexros-cli
display service verbose
display bgp peer
display ip routing-table
display alarm active
```

确认服务状态恢复、BGP 对端重新建立邻接，目标路由与实际转发已恢复。
