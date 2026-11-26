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

### 恢复 VPP 与核对接口状态

在独立 Console 上操作。记录当前接口归属、管理接入和可达的业务目的。确认计划重启数据面的影响范围后执行。

```vortexros-cli
display vpp api compatibility verbose
display vpp interface-ownership verbose
display vpp takeover transaction
display service verbose
reset service vpp
```

恢复后重新查看 VPP 服务、接口和最近一次接管状态。正常时原有 DPDK 接口应恢复归属，接口地址和转发表应恢复。最后从隔离对端验证双向转发。需要重新学习 MAC 时，可在维护窗口用 `reset mac-address` 清理动态表项，随后用 `display mac-address` 核对重新学习。

## 验证配置

```vortexros-cli
display service verbose
display bgp peer
display ip routing-table
display alarm active
```

确认服务状态恢复、BGP 对端重新建立邻接，目标路由与实际转发已恢复。
