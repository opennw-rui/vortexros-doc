---
nav_title: 配置案例
---


# IPv6 路径 MTU 配置案例

## 拓扑

![探测发起端 → 实际 IPv6 路径 → 目的主机](cases.svg)

(case-conditions-04-ip-routing-ipv6-path-mtu)=
## 配置条件

确定目的地址和所属 VPN。路径 MTU 表来自运行中学习到的信息。先经过实际业务路径发送 IPv6 流量，再查看相关项。

## 配置步骤

```vortexros-cli
display ipv6 pathmtu
display ipv6 pathmtu vpn-instance BLUE
display ipv6 routing-table vpn-instance BLUE
```

第一条查看默认实例，后两条查看 BLUE 中的路径信息和路由。将 BLUE 换成实际实例名。

(case-verification-04-ip-routing-ipv6-path-mtu)=
## 验证方法

对照以下命令和预期结果核对设备状态。

```vortexros-cli
display ipv6 pathmtu vpn-instance BLUE
display ipv6 routing-table vpn-instance BLUE
```

对照目标地址和 MTU，核对出接口及隧道封装。存在活动路径 MTU 项时，其目的应与测试流量一致。没有学习到条目时，可从两端测试不同长度的 IPv6 报文，并检查网络是否传递 ICMPv6 Packet Too Big 消息。
