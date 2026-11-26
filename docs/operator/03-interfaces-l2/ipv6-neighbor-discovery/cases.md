---
nav_title: 配置案例
nav_overview: 案例索引
---


# IPv6 邻居发现与静态邻居 配置案例

(case-conditions-03-interfaces-l2-ipv6-neighbor-discovery)=
## 配置条件

选定三层接口并确认对端 IPv6 和单播 MAC 地址。动态表项由流量学习。

```{toctree}
:maxdepth: 1

cases/example-1
cases/example-2
```

(case-verification-03-interfaces-l2-ipv6-neighbor-discovery)=
## 通用验证

```vortexros-cli
display ipv6 nd
display ipv6 neighbors static
display ipv6 neighbors interface Vlanif10
```

确认老化时间、容量和回收策略符合预期。静态列表应出现配置的 IPv6、MAC 与接口。使用实际流量核对转发。
