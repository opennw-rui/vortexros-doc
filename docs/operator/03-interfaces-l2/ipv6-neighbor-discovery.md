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

### 按 VPN 或接口定位邻居

```vortexros-cli
display ipv6 neighbors Vlanif 10
display ipv6 neighbors interface Ethernet 1
display ipv6 neighbors vpn-instance BLUE
display ipv6 neighbors dynamic
```

如果 Vlanif10 与 BLUE 已存在，可从对应网段发起流量后核对动态邻居。查询静态邻居时应看到已配置的 IPv6、单播 MAC 与接口。

如需恢复默认老化、容量与回收，在系统视图执行下列命令。

```text
undo ipv6 nd stale-timeout
undo ipv6 nd max-number
undo ipv6 nd recycle
commit
```

提交后再次执行 `display ipv6 nd`，核对设备默认值。

## 验证配置

```vortexros-cli
display ipv6 nd
display ipv6 neighbors static
display ipv6 neighbors interface Vlanif10
```

确认老化时间、容量和回收策略符合预期。静态列表应出现配置的 IPv6、MAC 与接口。使用实际流量核对转发。
