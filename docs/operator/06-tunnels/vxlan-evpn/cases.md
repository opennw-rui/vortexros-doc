---
nav_title: 配置案例
nav_overview: 案例索引
---


# BGP EVPN 与动态 VXLAN 配置案例

(case-conditions-06-tunnels-vxlan-evpn)=
## 配置条件

先配置两端底层接口、BGP EVPN 邻居和 VTEP 源。两个站点的 VNI 与 RT 相同，RD 分别配置。

```{toctree}
:maxdepth: 1

cases/example-1
cases/example-2
cases/example-3
```

(case-verification-06-tunnels-vxlan-evpn)=
## 通用验证

```vortexros-cli
display bgp peer
display bridge-domain 65536
display vxlan tunnel
display mac-address
```

先确认 BGP 邻居已建立，再检查远端 VTEP 和 MAC。移动终端后，确认旧位置的表项撤销且新位置学习正常。
