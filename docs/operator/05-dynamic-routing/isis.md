# IS-IS

## 功能介绍

IS-IS 通过交换链路状态建立 IPv4 或 IPv6 域内路由，可按 Level-1、Level-2 划分邻接范围。

## 配置准备

为每台设备分配唯一 NET 与 System ID，统一链路两端的 Level、计时和认证。

## 配置案例

进程号在设备内全局唯一。一个进程只能绑定一个VPN，一个VPN最多配置一个IS-IS进程；接口所属VPN必须与进程VPN一致。

```text
isis 10 vpn-instance BLUE
 network-entity 49.0001.0100.0000.0001.00
 is-level level-2
 cost-style wide
 log-adjacency-changes
interface Vlanif 100
 isis enable 10
 isis ipv6-enable 10
 isis circuit-type p2p
 isis circuit-level level-2
 isis cost 20
```

提交后，IPv4和IPv6在同一进程中运行。接口VPN不一致、同一接口引用另一个进程或同一VPN已存在其他进程时，命令会被拒绝。

`import-route`用于导入IPv4路由，`ipv6 import-route`用于导入IPv6路由：

```text
isis 10
 import-route static
 ipv6 import-route static
 ipv6 import-route ospfv3
```

重分发按 IS-IS 进程的级别生效。默认的 Level-1-2 进程可向两个级别重分发。

```vortexros-cli
display isis 10 brief
display isis 10 peer
display isis 10 interface
display isis 10 lsdb
display isis 10 route
```

撤销示例：

```text
interface Vlanif 100
 undo isis ipv6-enable 10
 undo isis enable
undo isis 10
commit
```

如果需要把进程迁移到另一个VPN，应先删除进程，再使用新VPN重新创建。

### Level-2 双栈邻接与路由

两台设备通过 Ethernet0 对接，使用 192.0.2.0/24 和 2001:db8:12::/64。每台设备具有独立的 NET 和双栈环回。

两台设备分别在系统视图录入各自的配置片段，退出功能视图后提交。

**R1**

```vortexros-config
isis 10
 network-entity 49.0001.0100.0000.0001.00
 is-level level-2
 cost-style wide
#
interface Ethernet 0
 ip address 192.0.2.1 255.255.255.0
 ipv6 enable
 ipv6 address 2001:db8:12::1 64
 isis enable 10
 isis ipv6-enable 10
 isis circuit-type p2p
 isis circuit-level level-2
#
interface LoopBack 0
 ip address 198.51.100.1 255.255.255.255
 ipv6 enable
 ipv6 address 2001:db8:1::1 128
 isis enable 10
 isis ipv6-enable 10
#
return
```

**R2**

```vortexros-config
isis 10
 network-entity 49.0001.0100.0000.0002.00
 is-level level-2
 cost-style wide
#
interface Ethernet 0
 ip address 192.0.2.2 255.255.255.0
 ipv6 enable
 ipv6 address 2001:db8:12::2 64
 isis enable 10
 isis ipv6-enable 10
 isis circuit-type p2p
 isis circuit-level level-2
#
interface LoopBack 0
 ip address 198.51.100.2 255.255.255.255
 ipv6 enable
 ipv6 address 2001:db8:2::1 128
 isis enable 10
 isis ipv6-enable 10
#
return
```

分别查看状态。

```vortexros-cli
display isis 10 peer
display isis 10 interface
display ip routing-table protocol isis
display ipv6 routing-table protocol isis
```

邻居为 Level-2、Up，Ethernet0 的 IPv4 与 IPv6 均已启用。R1 应看到 198.51.100.2/32 与 2001:db8:2::1/128，R2 应看到对称的路由。

## 验证配置

```vortexros-cli
display isis peer
display isis route
display ip routing-table
```

确认建立预期级别的邻接，核对远端网段与出接口，再从业务终端测试。
