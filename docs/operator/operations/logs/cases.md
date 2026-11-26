---
nav_title: 配置案例
nav_overview: 案例索引
---


# 日志中心 配置案例

(case-conditions-operations-logs)=
## 配置条件

先确定是临时调整当前终端，还是调整所有终端。查询历史记录可使用下面的 display 命令。

```{toctree}
:maxdepth: 1

cases/example-1
cases/example-2
```

(case-verification-operations-logs)=
## 通用验证

```vortexros-cli
display logbuffer
display logbuffer service frr last 30
display logbuffer last 20 since 15
display alarm active
```

核对事件涉及的接口或邻居、状态及本地时间。跨日期或跨启动周期时，在获准的系统维护环境查看带日期的 journal。
