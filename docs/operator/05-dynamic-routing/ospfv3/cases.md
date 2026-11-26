---
nav_title: 配置案例
nav_overview: 案例索引
---


# OSPFv3（IPv6） 配置案例

(case-conditions-05-dynamic-routing-ospfv3)=
## 配置条件

准备 IPv6 上联、非重复的 Router ID 和两端相同的区域。

```{toctree}
:maxdepth: 1

cases/example-1
cases/example-2
```

(case-verification-05-dynamic-routing-ospfv3)=
## 通用验证

```vortexros-cli
display ospfv3 peer
display ospfv3 routing
display ipv6 routing-table
```

确认邻接建立、远端 IPv6 前缀可见并在相应实例中从端点完成测试。
