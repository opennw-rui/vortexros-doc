---
nav_title: 比较 Uniform 与 Pipe TTL 行为
---


# 比较 Uniform 与 Pipe TTL 行为

## 拓扑

![PE1、P1、PE2 的设备互联](example-2.svg)

## 配置条件

为每台设备准备唯一 LSR ID，通过 IGP 交换其地址，并在核心接口准备对端连通。

沿用 [LDP 标签路径](../../ldp.md) 的核心，若需观察核心跳数，在两个 PE 之间接入至少一台转发标签的 P 节点。业务端持续 ping 远端。默认传播 TTL；要改成 Pipe，在两台入口 PE 的 MPLS 视图执行以下操作。

## 配置步骤

```text
system-view
mpls
undo ttl propagate
quit
commit
```

## 验证方法

对照{ref}`本功能页的实测结果 <recorded-result-10-mpls-l3vpn-mpls>`可以核对设备实际显示的字段或业务表现。不同拓扑请按本案例的地址和接口检查。

对照以下命令和预期结果核对设备状态。

```vortexros-cli
display current-configuration
display mpls forwarding-table
```

配置应显示 `undo ttl propagate`，适用的标签路径以 Pipe 转发。从业务端核对核心跳数不向内层继续传播，业务仍应可达。恢复时用 `ttl propagate` 并提交，路径恢复 Uniform。
