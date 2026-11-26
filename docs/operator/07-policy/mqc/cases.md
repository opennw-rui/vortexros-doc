---
nav_title: 配置案例
nav_overview: 案例索引
---


# MQC 分类、流量策略与重定向 配置案例

(case-conditions-07-policy-mqc)=
## 配置条件

先建立案例使用的 ACL WEB-IN 和 VPN BLUE，检查目标 VPN 有正确路由。

```{toctree}
:maxdepth: 1

cases/example-1
cases/example-2
cases/example-3
```

(case-verification-07-policy-mqc)=
## 通用验证

```vortexros-cli
display traffic classifier user-defined WEB-CLASS
display traffic behavior user-defined WEB-BEHAVIOR
display traffic policy user-defined WEB-POLICY
```

检查分类条件、动作及绑定。让命中和未命中的业务分别通过设备，检查出口和限速效果。
