---
nav_title: 配置案例
nav_overview: 案例索引
---


# IS-IS 配置案例

(case-conditions-05-dynamic-routing-isis)=
## 配置条件

为每台设备分配唯一 NET 与 System ID，统一链路两端的 Level、计时和认证。

```{toctree}
:maxdepth: 1

cases/example-1
cases/example-2
```

(case-verification-05-dynamic-routing-isis)=
## 通用验证

```vortexros-cli
display isis peer
display isis route
display ip routing-table
```

确认建立预期级别的邻接，核对远端网段与出接口，再从业务终端测试。
