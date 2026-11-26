---
nav_title: 在核心端口启用 MPLS
---


# 在核心端口启用 MPLS

## 拓扑

![入口 PE → 发送 MPLS 标签的核心链路 → 出口 PE](example-1.svg)

## 配置条件

为每台设备准备唯一 LSR ID，通过 IGP 交换其地址，并在核心接口准备对端连通。

## 配置步骤

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

## 验证方法

对照{ref}`本功能页的实测结果 <recorded-result-10-mpls-l3vpn-mpls>`可以核对设备实际显示的字段或业务表现。不同拓扑请按本案例的地址和接口检查。

对照以下命令和预期结果核对设备状态。

```vortexros-cli
display mpls interface
display mpls forwarding-table
```

确认核心接口启用 MPLS。建立标签路径后，核对标签绑定、目的与下一跳。
