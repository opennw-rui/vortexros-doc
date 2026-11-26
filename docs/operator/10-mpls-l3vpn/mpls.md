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

## 验证配置

```vortexros-cli
display mpls interface
display mpls lsp
display mpls forwarding-table
```

确认核心接口启用，建立标签路径后核对标签、下一跳和出接口。

[LDP 标签分发](ldp.md)
