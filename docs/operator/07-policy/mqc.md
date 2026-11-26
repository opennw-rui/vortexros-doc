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

## 验证配置

```vortexros-cli
display traffic classifier user-defined WEB-CLASS
display traffic behavior user-defined WEB-BEHAVIOR
display traffic policy user-defined WEB-POLICY
```

检查分类条件、动作及绑定。让命中和未命中的业务分别通过设备，检查出口和限速效果。
