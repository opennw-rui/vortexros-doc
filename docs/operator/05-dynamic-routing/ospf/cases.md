---
nav_title: 配置案例
nav_overview: 案例索引
---


# OSPF（IPv4） 配置案例

(case-conditions-05-dynamic-routing-ospf)=
## 配置条件

为每台路由器选独立的 Router ID。检查链路地址、区域、网络类型和计时两端一致。

```{toctree}
:maxdepth: 1

cases/example-1
cases/example-2
cases/example-3
cases/area-zero-adjacency
cases/vpn-adjacency
```

(case-verification-05-dynamic-routing-ospf)=
## 通用验证

```vortexros-cli
display ospf peer brief
display ip routing-table protocol ospf
```

核对邻接状态、学习的前缀及下一跳，并从下游测试连通性。

## 验证与撤销

```vortexros-cli
display ospf 1 brief
display ospf 1 peer brief
display ospf 1 peer 10.0.0.2
display ospf 1 interface
display ospf 1 lsdb
display ospf 1 routing
```

`display ospf peer brief`按以下顺序显示，Interface位于Neighbor id左侧：

```text
Area Id    Pri  Up Time   Dead Time  Interface   Neighbor id  State
0.0.0.0      1  00:12:31  00:00:38   Vlanif12    10.0.0.2     Full
```

修改与删除示例：

```text
interface Vlanif 12
 undo ospf dr-priority
 undo ospf network-type
 undo ospf enable 1
undo ospf 1
commit
```

撤销接口激活只影响该接口；删除进程会撤销该进程的全部邻居和路由。
