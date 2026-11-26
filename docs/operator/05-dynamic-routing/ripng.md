# RIPng（IPv6）

## 功能介绍

RIPng 根据跳数交换 IPv6 路由。可在指定三层接口接收和发送路由更新。

## 配置准备

准备已配置 IPv6 的链路。如果使用 BLUE，先创建并配置相应的 IPv6 VPN 实例。

## 配置案例

```text
ripng 2 vpn-instance BLUE
 network 2001:db8:100::/64
 import-route static
 default-route originate
```

RIPng 视图中的 `import-route ospf` 导入 OSPFv3 路由。

```vortexros-cli
display rip 1 interface
display rip 1 database
display rip 1 route
display ripng 2 interface
display ripng 2 route
```

精确撤销：

```text
rip 1
 undo network 10.0.0.0
 undo timers rip
undo rip 1
undo ripng 2 vpn-instance BLUE
commit
```

如需移除 IPv4 RIP 进程，请参见 [RIP（IPv4）](rip.md)。

## 验证配置

```vortexros-cli
display ripng 2 route
display ipv6 routing-table vpn-instance BLUE
```

确认学到的前缀出现在对应 VPN 和接口。撤销进程后，相关学到的路由应退出路由表。
