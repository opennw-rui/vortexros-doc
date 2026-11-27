---
nav_feature: true
---

# LoopBack 接口

LoopBack 是设备自身的逻辑三层接口。它适合为设备提供稳定的管理地址、路由协议源地址或隧道端点。

## 工作原理

LoopBack 的地址与某条网线的载波独立。远端到达该地址仍需要一条可用的路由。IPv4 常用 /32，IPv6 常用 /128。将接口放入 VPN 实例后，在该实例的路由表中检查它。

## 配置与验证

### 配置稳定的双栈地址

本例给 R1 的 LoopBack0 赋址。若其他设备需要访问这两个地址，在现有路由协议中通告对应前缀，或在对端配置可达的静态路由。先在 R1 的用户视图进入系统视图。

```vortexros-cli
system-view
interface LoopBack 0
 ip address 198.51.100.1 255.255.255.255
 ipv6 enable
 ipv6 address 2001:db8:100::1 128
 quit
commit
return
```

```vortexros-cli
display interface LoopBack 0
display ip routing-table protocol direct
display ipv6 routing-table protocol direct
```

预期在 IPv4 表中看到 `198.51.100.1/32`、在 IPv6 表中看到 `2001:db8:100::1/128`，两条路由均关联 LoopBack0。若对端已经安装路由，从对端分别对两个地址发起探测。两端的接线、完整路由配置和查询方法见[双栈静态路由案例](../04-ip-routing/static-routes/cases/example-2.md)。

在已验证的 VPN 场景中，`display ip routing-table vpn-instance ALL` 显示过以下表项。该场景使用 LoopBack200，与上面使用的地址不同。

```text
Destination/Mask   Proto   Pre  Cost    Flags  NextHop          Interface       VPN-Instance
 172.31.255.1/32   Direct  0    0         D    -                LoopBack200     ALL
```

## 注意事项

准备停用 LoopBack 前，先检查 BGP 对等体、隧道源地址和管理访问是否引用它。地址或 VPN 归属变更后，从实际对端复查会话，再保存配置。
