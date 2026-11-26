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

### RIPng 两端交换 IPv6 环回

R1 与 R2 的 Ethernet0 接入 2001:db8:12::/64。各自通告 LoopBack0 的 /128。

两台设备分别在系统视图录入各自的配置片段，退出功能视图后提交。

**R1**

```vortexros-config
interface Ethernet 0
 ipv6 enable
 ipv6 address 2001:db8:12::1 64
#
interface LoopBack 0
 ipv6 enable
 ipv6 address 2001:db8:1::1 128
#
ripng 2
 network 2001:db8:12::/64
 network 2001:db8:1::1/128
#
return
```

**R2**

```vortexros-config
interface Ethernet 0
 ipv6 enable
 ipv6 address 2001:db8:12::2 64
#
interface LoopBack 0
 ipv6 enable
 ipv6 address 2001:db8:2::1 128
#
ripng 2
 network 2001:db8:12::/64
 network 2001:db8:2::1/128
#
return
```

分别查看状态。

```vortexros-cli
display ripng 2 interface
display ripng 2 route
display ipv6 routing-table protocol ripng
```

R1 应学到 2001:db8:2::1/128，下一跳为 R2 的链路本地地址，R2 可看到相反方向的路由。若撤销其中一个 network，等待更新后确认相应路由消失。

## 验证配置

```vortexros-cli
display ripng 2 route
display ipv6 routing-table vpn-instance BLUE
```

确认学到的前缀出现在对应 VPN 和接口。撤销进程后，相关学到的路由应退出路由表。
