# DHCPv4 中继

## 功能介绍

DHCPv4 中继将本地客户端的请求转发到其他子网的 DHCPv4 服务器，使多个接入网段可以共用服务。

## 配置准备

在客户端网段准备三层接口与地址。确认服务器有该网段的地址池，并能路由回中继地址。

## 配置案例

```vortexros-config
interface Ethernet 1
 ip address 192.0.2.1 255.255.255.0
 dhcp select relay
 dhcp relay server-ip 198.51.100.10
#
return
```

录入配置并提交。在 DPDK 模式也可选择承载客户网段的 Vlanif。停用中继时，在相应接口视图执行 `undo dhcp relay server-ip 198.51.100.10` 和 `undo dhcp select`，再提交。

## 验证配置

```vortexros-cli
display dhcp relay
display ip interface brief
```

检查目标服务器和接口。让接入终端实际发起 DHCP 请求，并检查其获取的地址、网关和续租。
