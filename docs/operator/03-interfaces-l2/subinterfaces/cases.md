---
nav_title: 配置案例
nav_overview: 案例索引
---


# 802.1Q 与 QinQ 三层子接口 配置案例

(case-conditions-03-interfaces-l2-subinterfaces)=
## 配置条件

确保父接口按三层模式工作。对端须发送与相应子接口匹配的单标签或双标签。

```{toctree}
:maxdepth: 1

cases/example-1
cases/example-2
cases/example-3
```

(case-verification-03-interfaces-l2-subinterfaces)=
## 通用验证

```vortexros-cli
display interface Ethernet 1.100
display interface Ethernet 1.200
display ip routing-table protocol direct
```

核对两个子接口的状态和直连路由。分别从两种标签的对端发包，确认流量经对应子接口进入。
