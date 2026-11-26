---
nav_title: 配置案例
nav_overview: 案例索引
---


# 应用桥、出口与端口发布 配置案例

(case-conditions-11-applications-application-network)=
## 配置条件

准备独立应用卷、支持应用桥的签名应用，以及在默认路由表可达的上联。先创建桥，再安装和启动使用该桥的应用。

```{toctree}
:maxdepth: 1

cases/example-1
cases/example-2
```

(case-verification-11-applications-application-network)=
## 通用验证

```vortexros-cli
display ip routing-table
display ipv6 routing-table
```

使用 app bridge-status 查看桥与策略。从应用和管理站分别测试允许和拒绝的流量。当 advertise 为 true 时，核对桥前缀是否按配置通告；清除策略后确认通告撤销。
