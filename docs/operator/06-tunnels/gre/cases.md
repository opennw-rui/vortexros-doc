---
nav_title: 配置案例
nav_overview: 案例索引
---


# GRE Tunnel 配置案例

(case-conditions-06-tunnels-gre)=
## 配置条件

准备两台三层设备。各端的本机外层地址必须存在，且能在选定底层路由表中到达对端地址。规划独立的隧道内层网段。

```{toctree}
:maxdepth: 1

cases/default-routing-table
cases/vpn-underlay
```

(case-verification-06-tunnels-gre)=
## 通用验证

每个案例给出需要执行的查询命令和正常时的预期结果。先选择与实际拓扑相符的案例，再按对应步骤验证。
