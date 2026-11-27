---
nav_title: 指定单播中继目标
---


# 指定单播中继目标

## 拓扑

![DHCPv4 客户端、R1、DHCPv4 服务器 的设备互联](example-1.svg)

## 配置条件

在客户端网段准备三层接口与地址。确认服务器有该网段的地址池，并能路由回中继地址。

## 配置步骤

```vortexros-config
interface Ethernet 1
 ip address 192.0.2.1 255.255.255.0
 dhcp select relay
 dhcp relay server-ip 198.51.100.10
#
return
```

录入配置并提交。在 DPDK 模式也可选择承载客户网段的 Vlanif。停用中继时，在相应接口视图执行 `undo dhcp relay server-ip 198.51.100.10` 和 `undo dhcp select`，再提交。

## 验证方法

对照{ref}`本功能页的实测结果 <recorded-result-08-network-services-dhcpv4-relay>`可以核对设备实际显示的字段或业务表现。不同拓扑请按本案例的地址和接口检查。

对照以下命令和预期结果核对设备状态。

```vortexros-cli
display dhcp relay
display ip interface brief
```

核对中继运行在客户网段接口，目标是 198.51.100.10。实际客户端应能取得相应网段内的租约。
