# BFD 快速故障检测

## 功能介绍

BFD 快速检测两个转发端点之间的可达性。可独立建立会话，也可配合动态路由协议加速故障收敛。

## 配置准备

确保两端已经具有可用的三层路径。按链路条件确定计时及检测次数。

## 配置案例

BFD可建立独立会话，也可由OSPF、IS-IS、RIP和BGP邻居调用。协议会话默认发送间隔1000ms、接收间隔1000ms、检测次数3。

### 独立BFD会话

```text
bfd
bfd TO-P2 bind peer-ip 10.0.12.2 source-ip 10.0.12.1 interface Vlanif 12
 min-tx-interval 300
 min-rx-interval 300
 detect-multiplier 3
 log-session-changes
```

多跳会话需要显式指定 `source-ip`，VPN场景可追加 `vpn-instance BLUE`。

### 路由协议调用BFD

```text
interface Vlanif 12
 ospf bfd enable
 ospf bfd min-tx-interval 300 min-rx-interval 300 detect-multiplier 3
```

```text
bgp 64512
 peer 10.0.0.2 bfd enable
 peer 10.0.0.2 bfd min-tx-interval 300 min-rx-interval 300 detect-multiplier 3
```

IS-IS和RIP使用同样的接口形式，将命令前缀替换为 `isis bfd` 或 `rip bfd`。

```vortexros-cli
display bfd configuration
display bfd session all
display bfd statistics
```

恢复默认计时或删除会话：

```text
bfd TO-P2 bind peer-ip 10.0.12.2 source-ip 10.0.12.1 interface Vlanif 12
 undo min-tx-interval
 undo min-rx-interval
 undo detect-multiplier
undo bfd TO-P2
commit
```

### 直连双端独立 BFD 会话

两个 Ethernet0 位于 192.0.2.0/24。两端本地地址和对端地址互换，检测间隔 300 ms、倍数 3。

两台设备分别在系统视图录入各自的配置片段，退出功能视图后提交。

**R1**

```vortexros-config
interface Ethernet 0
 ip address 192.0.2.1 255.255.255.0
#
bfd
#
bfd TO-R2 bind peer-ip 192.0.2.2 source-ip 192.0.2.1 interface Ethernet 0
 min-tx-interval 300
 min-rx-interval 300
 log-session-changes
#
return
```

**R2**

```vortexros-config
interface Ethernet 0
 ip address 192.0.2.2 255.255.255.0
#
bfd
#
bfd TO-R1 bind peer-ip 192.0.2.1 source-ip 192.0.2.2 interface Ethernet 0
 min-tx-interval 300
 min-rx-interval 300
 log-session-changes
#
return
```

分别查看状态。

```vortexros-cli
display bfd session all
display bfd statistics
```

两端会话为 Up，发送和接收计数增加。受控断开链路并恢复时，记录 Down 和随后回到 Up 的过程。

### OSPFv3 联动 BFD

复用 OSPFv3 双节点的 Ethernet0 链路与环回，每端在互联口开启动态 BFD。若有备用链路，先建立其 OSPFv3 邻接并将成本设高。

两台设备分别在系统视图录入各自的配置片段，退出功能视图后提交。

**R1**

```vortexros-config
bfd
#
ospfv3 1 router-id 198.51.100.1
 area 0.0.0.0
#
interface Ethernet 0
 ipv6 enable
 ipv6 address 2001:db8:12::1 64
 ospfv3 1 area 0.0.0.0
 ospfv3 bfd enable
 ospfv3 bfd min-tx-interval 300 min-rx-interval 300
#
interface LoopBack 0
 ipv6 enable
 ipv6 address 2001:db8:1::1 128
 ospfv3 1 area 0.0.0.0
#
return
```

**R2**

```vortexros-config
bfd
#
ospfv3 1 router-id 198.51.100.2
 area 0.0.0.0
#
interface Ethernet 0
 ipv6 enable
 ipv6 address 2001:db8:12::2 64
 ospfv3 1 area 0.0.0.0
 ospfv3 bfd enable
 ospfv3 bfd min-tx-interval 300 min-rx-interval 300
#
interface LoopBack 0
 ipv6 enable
 ipv6 address 2001:db8:2::1 128
 ospfv3 1 area 0.0.0.0
#
return
```

分别查看状态。

```vortexros-cli
display bfd session all
display ospfv3 1 peer brief
display ipv6 routing-table
```

主链路 BFD 为 Up，OSPFv3 为 Full。故障时检查主邻接退出，存在备用路径时远端路由下一跳应切至备用链路。恢复后检查会话、主路径和双向转发。

## 验证配置

```vortexros-cli
display bfd configuration
display bfd session all
display bfd statistics
```

先确认会话 Up。受控断开链路后，检查会话 Down 和引用该会话的协议是否切换，恢复链路后复查。
