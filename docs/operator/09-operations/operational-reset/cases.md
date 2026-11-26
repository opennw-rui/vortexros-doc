---
nav_title: 配置案例
nav_overview: 案例索引
---


# 清理运行状态与服务恢复 配置案例

(case-conditions-09-operations-operational-reset)=
## 配置条件

选择影响范围最小的操作。清空动态表项或重启服务前确认业务窗口和可用的 Console。

```{toctree}
:maxdepth: 1

cases/example-1
cases/example-2
```

(case-verification-09-operations-operational-reset)=
## 通用验证

```vortexros-cli
display service verbose
display bgp peer
display ip routing-table
display alarm active
```

确认服务状态恢复、BGP 对端重新建立邻接，目标路由与实际转发已恢复。
