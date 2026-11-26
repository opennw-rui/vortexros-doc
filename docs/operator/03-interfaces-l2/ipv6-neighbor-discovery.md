# IPv6 邻居发现与静态邻居

## 功能介绍

IPv6 邻居发现用于解析相邻节点的链路层地址。可为已知对端设置静态映射，或按需要调整数据面邻居表容量和老化时间。

## 配置准备

选定三层接口并确认对端 IPv6 和单播 MAC 地址。动态表项由流量学习。

## 配置案例

```vortexros-config
enable switch
vlan 10
#
interface Vlanif 10
 ipv6 enable
 ipv6 address 2001:db8:10::1 64
#
ipv6 nd stale-timeout 1800
ipv6 nd max-number 65536
ipv6 nd recycle enable
ipv6 neighbor 2001:db8:10::2 02:11:22:33:44:55 interface Vlanif10
#
return
```

录入后提交。表满时，回收策略只处理动态表项。要删除静态邻居，使用完整的 `undo ipv6 neighbor 2001:db8:10::2 02:11:22:33:44:55 interface Vlanif10` 后提交。

## 验证配置

```vortexros-cli
display ipv6 nd
display ipv6 neighbors static
display ipv6 neighbors interface Vlanif10
```

确认老化时间、容量和回收策略符合预期。静态列表应出现配置的 IPv6、MAC 与接口。使用实际流量核对转发。
