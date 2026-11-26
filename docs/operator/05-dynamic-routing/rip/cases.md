---
nav_title: 配置案例
nav_overview: 案例索引
---


# RIP（IPv4） 配置案例

(case-conditions-05-dynamic-routing-rip)=
## 配置条件

在同一 IPv4 链路上配置兼容的 RIP 版本并准备要通告的网段。

```{toctree}
:maxdepth: 1

cases/example-1
cases/example-2
```

(case-verification-05-dynamic-routing-rip)=
## 通用验证

```vortexros-cli
display rip 1 route
display ip routing-table
```

确认邻居通告的网段与跳数，使用业务终端确认远端网络可达。
