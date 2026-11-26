---
nav_title: 配置案例
nav_overview: 案例索引
---


# LDP 标签分发 配置案例

(case-conditions-10-mpls-l3vpn-ldp)=
## 配置条件

先规划两端 LSR ID、核心三层链路和 IGP 路由。以下配置包含 PE1 的接口、IGP 和 LDP。

```{toctree}
:maxdepth: 1

cases/example-1
cases/example-2
```

(case-verification-10-mpls-l3vpn-ldp)=
## 通用验证

```vortexros-cli
display mpls ldp interface
display mpls ldp peer
display mpls ldp binding
display mpls forwarding-table
```

确认两端 LDP 邻接已建立，远端 LSR ID 的标签可以从下一跳送出。没有业务引用时再撤销接口 LDP。
