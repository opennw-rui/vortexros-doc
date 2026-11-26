---
nav_title: 配置案例
nav_overview: 案例索引
---


# MAC 地址表 配置案例

(case-conditions-03-interfaces-l2-mac-table)=
## 配置条件

在已经可以收发流量的 VLAN 上观察动态学习。全局老化时间调整会影响已有 VLAN。

```{toctree}
:maxdepth: 1

cases/example-1
cases/example-2
```

(case-verification-03-interfaces-l2-mac-table)=
## 通用验证

```vortexros-cli
display mac-address
display current-configuration | include aging-time
```

检查动态表项的 VLAN、MAC 和出接口。停止指定终端的流量后，可观察表项何时从列表中移除。
