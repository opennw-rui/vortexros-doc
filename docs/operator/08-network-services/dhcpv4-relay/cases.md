---
nav_title: 配置案例
nav_overview: 案例索引
---


# DHCPv4 中继 配置案例

(case-conditions-08-network-services-dhcpv4-relay)=
## 配置条件

在客户端网段准备三层接口与地址。确认服务器有该网段的地址池，并能路由回中继地址。

```{toctree}
:maxdepth: 1

cases/example-1
cases/example-2
```

(case-verification-08-network-services-dhcpv4-relay)=
## 通用验证

```vortexros-cli
display dhcp relay
display ip interface brief
```

检查目标服务器和接口。让接入终端实际发起 DHCP 请求，并检查其获取的地址、网关和续租。
