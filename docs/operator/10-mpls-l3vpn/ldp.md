# LDP 标签分发

## 功能介绍

LDP 在 MPLS 核心的邻居之间交换标签绑定，供目的前缀建立标签转发路径。

## 配置准备

先规划两端 LSR ID、核心三层链路和 IGP 路由。以下配置包含 PE1 的接口、IGP 和 LDP。

## 配置案例

在核心链路开通 IPv4 底层连通，使用稳定且全网唯一的 LSR ID，并在 IGP 中通告其主机地址。两端在核心三层接口启用 MPLS 和 LDP。以下示例使用一条核心链路。

```vortexros-config
#
sysname PE1
#
mpls lsr-id 192.0.2.1
mpls
#
mpls ldp
#
interface LoopBack0
 ip address 192.0.2.1 255.255.255.255
#
interface Ethernet0
 ip address 198.51.100.1 255.255.255.252
 mpls
 mpls ldp
 ospf network-type p2p
#
ospf 1 router-id 192.0.2.1
 area 0.0.0.0
  network 192.0.2.1 0.0.0.0
  network 198.51.100.1 0.0.0.0
#
return
```

对端使用同一链路的另一有效地址及独立的 LSR ID。提交后核对两端 IGP 路由，再核对 LDP 会话、标签绑定和实际转发表。

```vortexros-cli
display mpls interface
display mpls ldp interface
display mpls ldp peer
display mpls ldp binding
display mpls lsp
display mpls forwarding-table
```

## 验证配置

```vortexros-cli
display mpls ldp interface
display mpls ldp peer
display mpls ldp binding
display mpls forwarding-table
```

确认两端 LDP 邻接已建立，远端 LSR ID 的标签可以从下一跳送出。没有业务引用时再撤销接口 LDP。
