---
nav_title: 配置案例
nav_overview: 案例索引
---


# NTP 时间同步 配置案例

(case-conditions-02-system-services-ntp)=
## 配置条件

确认时间源可达。使用 vpn-instance 前先创建相应的 VPN 并准备到服务器的路由。

```{toctree}
:maxdepth: 1

cases/example-1
cases/example-2
```

(case-verification-02-system-services-ntp)=
## 通用验证

```vortexros-cli
display ntp-service status
display ntp-service sessions
```

等待设备选源，核对同步状态、服务器地址、所属 VPN 和可达性。
