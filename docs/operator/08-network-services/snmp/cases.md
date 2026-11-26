---
nav_title: 配置案例
nav_overview: 案例索引
---


# SNMP 监控 配置案例

(case-conditions-08-network-services-snmp)=
## 配置条件

准备管理站和设备管理接口。下例使用 v2c 联调，请将 COMMUNITY 替换为设备专用的团体名。

```{toctree}
:maxdepth: 1

cases/example-1
cases/example-2
```

(case-verification-08-network-services-snmp)=
## 通用验证

```vortexros-cli
display snmp-agent sys-info
display snmp-agent community
display process udp listen
```

检查 UDP 161 和绑定的接口，再从实际管理站发起只读轮询。使用管理 VPN 时，检查网管路径经过正确的 VPN。
