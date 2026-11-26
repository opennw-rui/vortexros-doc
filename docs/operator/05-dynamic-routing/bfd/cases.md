---
nav_title: 配置案例
nav_overview: 案例索引
---


# BFD 快速故障检测 配置案例

(case-conditions-05-dynamic-routing-bfd)=
## 配置条件

确保两端已经具有可用的三层路径。按链路条件确定计时及检测次数。

BFD可建立独立会话，也可由OSPF、IS-IS、RIP和BGP邻居调用。协议会话默认发送间隔1000ms、接收间隔1000ms、检测次数3。

```{toctree}
:maxdepth: 1

cases/example-1
cases/example-2
cases/example-3
cases/example-4
```

(case-verification-05-dynamic-routing-bfd)=
## 通用验证

```vortexros-cli
display bfd configuration
display bfd session all
display bfd statistics
```

先确认会话 Up。受控断开链路后，检查会话 Down 和引用该会话的协议是否切换，恢复链路后复查。
