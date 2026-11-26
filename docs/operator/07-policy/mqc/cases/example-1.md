---
nav_title: 建立分类、动作与接口绑定
---


# 建立分类、动作与接口绑定

## 拓扑

![客户端 → 入口分类与策略 → 目标出口或 VPN](example-1.svg)

## 配置条件

先建立案例使用的 ACL WEB-IN 和 VPN BLUE，检查目标 VPN 有正确路由。

## 配置步骤

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

## 验证方法

对照以下命令和预期结果核对设备状态。

```vortexros-cli
display traffic classifier user-defined WEB-CLASS
display traffic behavior user-defined WEB-BEHAVIOR
display traffic policy user-defined WEB-POLICY
```

修改被MQC引用的ACL后，新的匹配规则在本次commit成功后生效；无需解除并重新绑定traffic policy。
