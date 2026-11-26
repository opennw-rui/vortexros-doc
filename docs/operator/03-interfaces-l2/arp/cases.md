---
nav_title: 配置案例
nav_overview: 案例索引
---


# ARP 与代理 ARP 配置案例

(case-conditions-03-interfaces-l2-arp)=
## 配置条件

选定具备 MAC、可以发送 ARP 的三层接口。先核对路由和实际可达性。

```{toctree}
:maxdepth: 1

cases/example-1
cases/example-2
```

(case-verification-03-interfaces-l2-arp)=
## 通用验证

```vortexros-cli
display arp
display arp proxy
display arp interface Vlanif 100
```

核对表项状态、出口和代理地址范围。在同链路终端请求其中一个目标，检查收到的响应及目标连通性。老化时间设置适用于 DPDK 数据面的邻居表。
