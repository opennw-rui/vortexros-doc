# IP-in-IP 隧道

## 功能介绍

IP-in-IP 用 IP 包封装另一个 IP 包，连接跨底层网络的三层网段。按需搭配 IPv4 或 IPv6 内外层。

## 配置准备

确认两个外层地址互相可达，双方选择一致的封装协议。示例使用 IPv4 内层与 IPv4 外层。

## 配置案例

```vortexros-config
interface Tunnel 2
 tunnel-protocol ipv4-ipv4
 source 192.0.2.1
 destination 192.0.2.2
 ip address 10.0.12.1 255.255.255.252
#
return
```

对端对调源和目的并将内部接口设为 10.0.12.2，录入后提交。

## 验证配置

```vortexros-cli
display interface Tunnel 2
display ip routing-table protocol direct
```

检查接口和直连前缀，随后从两端分别 ping 对端隧道地址。用 undo interface Tunnel 2 删除不再使用的隧道。
