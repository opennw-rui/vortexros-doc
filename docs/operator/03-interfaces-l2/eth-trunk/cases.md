---
nav_title: 配置案例
nav_overview: 案例索引
---


# Eth-Trunk 链路聚合 配置案例

(case-conditions-03-interfaces-l2-eth-trunk)=
## 配置条件

示例使用 Ethernet1 和 Ethernet2。先移除成员上独立的二三层业务配置，并确保对端采用相同模式及 MTU。

```{toctree}
:maxdepth: 1

cases/example-1
cases/example-2
```

(case-verification-03-interfaces-l2-eth-trunk)=
## 通用验证

```vortexros-cli
display eth-trunk 10
display interface brief
```

确认成员状态符合预期。检查 Eth-Trunk10 及其成员，再断开一根链路验证剩余成员是否仍能转发。
