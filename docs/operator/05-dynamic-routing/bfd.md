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

## 验证配置

```vortexros-cli
display bfd configuration
display bfd session all
display bfd statistics
```

先确认会话 Up。受控断开链路后，检查会话 Down 和引用该会话的协议是否切换，恢复链路后复查。
