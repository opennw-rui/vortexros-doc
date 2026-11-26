---
nav_title: 配置案例
nav_overview: 案例索引
---


# IPIP Tunnel 配置案例

(case-conditions-06-tunnels-ip-in-ip)=
## 配置条件

准备两个可达的三层外层端点，并按内层和外层地址族选择相同的封装模式。隧道网络与底层链路使用不同网段。

配置前确认两个外层地址互相可达。以下四个案例独立使用，同一个 Tunnel 只选一种模式。

```{toctree}
:maxdepth: 1

cases/ipv4-over-ipv4
cases/ipv6-over-ipv4
cases/ipv4-over-ipv6
cases/ipv6-over-ipv6
```

(case-verification-06-tunnels-ip-in-ip)=
## 通用验证

```vortexros-cli
display interface Tunnel 2
display ip routing-table protocol direct
```

检查接口和直连前缀，随后从两端分别 ping 对端隧道地址。用 undo interface Tunnel 2 删除不再使用的隧道。
