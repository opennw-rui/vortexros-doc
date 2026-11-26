# MPLS 核心转发

## 功能介绍

MPLS 通过标签转发报文，为 L3VPN 等业务提供核心传输。核心设备需能到达对端的稳定标识地址。

## 配置准备

为每台设备准备唯一 LSR ID，通过 IGP 交换其地址，并在核心接口准备对端连通。

## 配置案例

```vortexros-config
mpls lsr-id 192.0.2.1
mpls
#
interface Ethernet0
 ip address 198.51.100.1 255.255.255.252
 mpls
#
return
```

录入后提交。对端使用同一链路的另一地址及独立 LSR ID。要自动分发标签，在两端启用 LDP。

### 比较 Uniform 与 Pipe TTL 行为

沿用 [LDP 标签路径](ldp.md) 的核心，若需观察核心跳数，在两个 PE 之间接入至少一台转发标签的 P 节点。业务端持续 ping 远端。默认传播 TTL；要改成 Pipe，在两台入口 PE 的 MPLS 视图执行以下操作。

```text
system-view
mpls
undo ttl propagate
quit
commit
```

```vortexros-cli
display current-configuration
display mpls forwarding-table
```

配置应显示 `undo ttl propagate`，适用的标签路径以 Pipe 转发。从业务端核对核心跳数不向内层继续传播，业务仍应可达。恢复时用 `ttl propagate` 并提交，路径恢复 Uniform。

## 验证配置

```vortexros-cli
display mpls interface
display mpls lsp
display mpls forwarding-table
```

确认核心接口启用，建立标签路径后核对标签、下一跳和出接口。

[LDP 标签分发](ldp.md)
