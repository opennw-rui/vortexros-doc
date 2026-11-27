---
nav_title: 标记 TCP 流量并原位修改匹配条件
---


# 标记 TCP 流量并原位修改匹配条件

## 拓扑

![客户端、R1、服务器 的设备互联](example-3.svg)

## 配置条件

先建立案例使用的 ACL WEB-IN 和 VPN BLUE，检查目标 VPN 有正确路由。

客户端经 Ethernet0 进入设备，通过已有三层路由到达对端服务器。只对目的端口 12345–12346 的 TCP 流量标记 DSCP 16。把同一连接与一个未命中连接作对照。

## 配置步骤

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

## 验证方法

对照{ref}`本功能页的实测结果 <recorded-result-07-policy-mqc>`可以核对设备实际显示的字段或业务表现。不同拓扑请按本案例的地址和接口检查。

对照以下命令和预期结果核对设备状态。

```vortexros-cli
display traffic classifier user-defined WEB-MARK
display traffic behavior user-defined SET-DSCP
display traffic policy user-defined MARK-IN
```

检查显示中的动作 DSCP 16 和匹配方向。改为按源端口匹配后建立新流，只有命中流的标记改变。
