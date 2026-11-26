# IPv6 路径 MTU

## 功能介绍

IPv6 路径 MTU 表示到目的地址的路径可传输的最大 IP 报文长度。小报文可达、大报文失败时，可结合此查询排查路径限制。

## 查询准备

确定目的地址和所属 VPN。路径 MTU 表来自运行中学习到的信息。先经过实际业务路径发送 IPv6 流量，再查看相关项。

## 查询案例

```vortexros-cli
display ipv6 pathmtu
display ipv6 pathmtu vpn-instance BLUE
display ipv6 routing-table vpn-instance BLUE
```

第一条查看默认实例，后两条查看 BLUE 中的路径信息和路由。将 BLUE 换成实际实例名。

## 验证结果

对照表中目的地址和 MTU，核对实际出接口以及路径中的隧道封装。没有学习到条目时，可从两端测试不同长度的 IPv6 报文，并检查网络是否传递 ICMPv6 Packet Too Big 消息。
