# MQC 分类、流量策略与重定向

## 功能介绍

MQC 将匹配、动作和应用位置分开。可按业务流分类，对匹配报文限速、重标记或重定向。

## 配置准备

先建立案例使用的 ACL WEB-IN 和 VPN BLUE，检查目标 VPN 有正确路由。

## 配置案例

```text
traffic classifier WEB-CLASS operator and
 if-match acl WEB-IN
#
traffic behavior WEB-BEHAVIOR
 car cir 100000 pir 100000 cbs 18750000 pbs 31250000 green pass yellow pass red discard
 redirect vpn-instance BLUE
#
traffic policy WEB-POLICY
 classifier WEB-CLASS behavior WEB-BEHAVIOR precedence 10
#
interface Vlanif 100
 traffic-policy WEB-POLICY inbound
```

`redirect vpn-instance BLUE`不改目的地址，IPv4/IPv6分别进入BLUE对应FIB查目的地址，支持直连、静态、动态、递归、ECMP和默认路由；无匹配时按FIB miss丢弃，不回退原VPN。table-only、next-hop和interface三种redirect互斥。

同一behavior可以同时执行CAR、remark和redirect。重定向到VPN后，报文只在目标VPN中重新查找一次路由，不会反复执行同一重定向形成循环。

```vortexros-cli
display traffic classifier user-defined WEB-CLASS
display traffic behavior user-defined WEB-BEHAVIOR
display traffic policy user-defined WEB-POLICY
```

修改被MQC引用的ACL后，新的匹配规则在本次commit成功后生效；无需解除并重新绑定traffic policy。

### 按 TCP 端口选择 VPN 的出口

客户端 192.0.2.10 经 Ethernet0 入站。服务器 198.51.100.2 经 BLUE 的 Ethernet1 出站。先在隔离网络提供 BLUE 到客户端的回程，或使用单向接收验证。这里仅允许命中该分类的报文改用 BLUE 查路。

```vortexros-config
ip vpn-instance BLUE
 ipv4-family
#
acl name WEB-IN advance
 rule 10 permit tcp destination-port eq 443
#
traffic classifier WEB-CLASS operator and
 if-match acl WEB-IN
#
traffic behavior WEB-BEHAVIOR
 redirect vpn-instance BLUE
#
traffic policy WEB-POLICY
 classifier WEB-CLASS behavior WEB-BEHAVIOR precedence 10
#
interface Ethernet 0
 ip address 192.0.2.1 255.255.255.0
 traffic-policy WEB-POLICY inbound
#
interface Ethernet 1
 ip binding vpn-instance BLUE
 ip address 198.51.100.1 255.255.255.0
#
return
```

```vortexros-cli
display acl name WEB-IN
display traffic policy user-defined WEB-POLICY
display ip routing-table vpn-instance BLUE
```

从客户端发往同一服务器的 TCP 443 和另一个端口。服务器网口应收到 443 流量，其他端口继续按原路由表查找，原表无路由时不会经 BLUE 到达。修改分类器时，保留原策略绑定，提交后以新流验证结果。

## 验证配置

```vortexros-cli
display traffic classifier user-defined WEB-CLASS
display traffic behavior user-defined WEB-BEHAVIOR
display traffic policy user-defined WEB-POLICY
```

检查分类条件、动作及绑定。让命中和未命中的业务分别通过设备，检查出口和限速效果。

### 标记 TCP 流量并原位修改匹配条件

客户端经 Ethernet0 进入设备，通过已有三层路由到达对端服务器。只对目的端口 12345–12346 的 TCP 流量标记 DSCP 16。把同一连接与一个未命中连接作对照。

```vortexros-config
traffic classifier WEB-MARK operator and
 if-match protocol-number 6
 if-match destination-port 12345 to 12346
#
traffic behavior SET-DSCP
 permit
 remark dscp 16
#
traffic policy MARK-IN
 classifier WEB-MARK behavior SET-DSCP precedence 20
#
interface Ethernet 0
 traffic-policy MARK-IN inbound
#
return
```

```vortexros-cli
display traffic classifier user-defined WEB-MARK
display traffic behavior user-defined SET-DSCP
display traffic policy user-defined MARK-IN
```

设备应显示协议、端口条件和标记动作。提交后令客户端发起两种流量，从服务器侧检查报文。命中流量的 DSCP 应为 16，未命中流量保持原值。若要改成按来源端口 12000–12001 匹配，在原分类器执行以下命令，接口保持绑定。

```text
traffic classifier WEB-MARK
 undo if-match destination-port
 if-match source-port 12000 to 12001
quit
commit
```

再次查询分类器应看到来源端口，并用新连接确认标记效果。
