---
nav_title: 清除 NAT 计数并恢复 BGP
---


# 清除 NAT 计数并恢复 BGP

## 操作流程

![R1、R2 的设备互联](example-1.svg)

## 配置条件

选择影响范围最小的操作。清空动态表项或重启服务前确认业务窗口和可用的 Console。

为复查 NAT 命中，可清理策略计数，再重复对应的流量。

## 配置步骤

```vortexros-cli
clear nat-policy counters
display nat-policy statistics
```

如已确认 BGP 服务需要恢复，执行下列命令并按提示确认。

```vortexros-cli
reset service bgp
```

## 验证方法

对照{ref}`本功能页的实测结果 <recorded-result-09-operations-operational-reset>`可以核对设备实际显示的字段或业务表现。不同拓扑请按本案例的地址和接口检查。

对照以下命令和预期结果核对设备状态。

```vortexros-cli
display nat-policy statistics
display bgp peer
display ip routing-table
```

清除计数后用新流量验证活动统计。重启 BGP 后应重新建立邻居并恢复预期路由。
