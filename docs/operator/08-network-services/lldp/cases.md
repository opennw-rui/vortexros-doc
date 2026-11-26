---
nav_title: 配置案例
nav_overview: 案例索引
---


# LLDP 邻居发现 配置案例

(case-conditions-08-network-services-lldp)=
## 配置条件

在需观察的链路两端启用 LLDP，并确认物理链路已连接。

```{toctree}
:maxdepth: 1

cases/example-1
cases/example-2
```

(case-verification-08-network-services-lldp)=
## 通用验证

```vortexros-cli
display lldp neighbor brief
display lldp neighbor interface Ethernet0
```

检查本地 Ethernet0 对应的远端设备和端口，等待下一个通告周期后复查变更。
