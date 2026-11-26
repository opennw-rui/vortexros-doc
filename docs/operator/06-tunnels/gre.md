# GRE Tunnel

## 介绍

GRE 用于在可达的三层网络上承载另一条三层逻辑链路。隧道本身不提供加密。

## 功能特性

用 `display interface Tunnel 1` 或 `display interface brief` 查看状态。PHY 反映隧道自身和底层路径是否就绪，Protocol 还取决于隧道接口的三层地址。

| 状态 | 判定条件 |
| --- | --- |
| PHY up | GRE 协议和两端外层地址已配置，运行中的隧道已启用，源地址属于所选底层路由表，目的地址在同一表中有可用转发路径。 |
| Protocol up | PHY 已 up，且 Tunnel 接口具备有效的内层 IP 地址。没有内层地址时，PHY 可以是 up，Protocol 显示 down。 |
| `^down` | 协议或外层端点配置不完整，隧道等待创建。 |
| `down` | 配置已完整，但运行接口、源地址或底层路径尚未就绪。 |
| `*down` | 已通过 `shutdown` 管理关闭。 |

GRE 的 up 反映本端条件。两端配置是否一致、业务是否可用，以隧道内的双向流量为准。

## 配置案例

### 默认路由表中的双端 GRE

R1、R2 用 Ethernet0 上的 192.0.2.1 和 192.0.2.2 作为外层地址，经 Tunnel1 承载 10.0.12.0/30。双方 GRE key 均为 100。

两台设备分别在系统视图录入各自的配置片段，退出功能视图后提交。

**R1**

```vortexros-config
interface Ethernet 0
 ip address 192.0.2.1 255.255.255.0
#
interface Tunnel 1
 tunnel-protocol gre
 source 192.0.2.1
 destination 192.0.2.2
 gre key 100
 mtu 1472
 ip address 10.0.12.1 255.255.255.252
#
return
```

**R2**

```vortexros-config
interface Ethernet 0
 ip address 192.0.2.2 255.255.255.0
#
interface Tunnel 1
 tunnel-protocol gre
 source 192.0.2.2
 destination 192.0.2.1
 gre key 100
 mtu 1472
 ip address 10.0.12.2 255.255.255.252
#
return
```

分别查看状态。

```vortexros-cli
display interface Tunnel 1
display ip routing-table protocol direct
```

两端隧道为 up，10.0.12.0/30 为直连。R1 ping 10.0.12.2，R2 ping 10.0.12.1。撤掉某端底层可达路径后检查状态变化，恢复路径时复查双向流量。

### 使用 VPN 实例作为底层

沿用上例的两端地址。先在两台设备创建名为 TRANSIT 的 IPv4 VPN 实例，将持有外层地址的接口绑定到 TRANSIT，再为其配置地址。确认 TRANSIT 中能到达对端外层地址。保留 Tunnel1 的内层地址、MTU 和 GRE key，只改外层地址的查表范围。

**R1**

```text
interface Tunnel 1
 source 192.0.2.1 vpn-instance TRANSIT
 destination 192.0.2.2 vpn-instance TRANSIT
quit
commit
```

**R2**

```text
interface Tunnel 1
 source 192.0.2.2 vpn-instance TRANSIT
 destination 192.0.2.1 vpn-instance TRANSIT
quit
commit
```

```vortexros-cli
display ip routing-table vpn-instance TRANSIT
display interface Tunnel 1
```

两端的 TRANSIT 路由表都应能到达对端外层地址，Tunnel1 的 PHY 和 Protocol 均应为 up。再从 R1 和 R2 分别 ping 对端隧道地址。

## 注意事项

- 源地址和目的地址须使用同一底层路由表。底层 VPN 与 Tunnel 接口承载内层业务所用的 VPN 可分别选择。
- 两端的 GRE key 应一致。对称修改或撤销 key 后，用内层双向流量验证。
- 外层 IPv4 MTU 为 1500、使用 GRE key 且无其他额外封装时，内层 MTU 可设为 1472。实际路径 MTU 更小时应相应调小。
- 删除前先移除指向 Tunnel1 的静态路由和协议、策略引用。在系统视图执行 `undo interface Tunnel 1` 并提交，再检查接口及相关直连路由。
