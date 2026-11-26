# Eth-Trunk 链路聚合

## 功能介绍

将多条 Ethernet 链路合为一条逻辑接口，可增加可用带宽并承受单链路故障。可按对端选择手工聚合或 LACP。

## 配置准备

示例使用 Ethernet1 和 Ethernet2。先移除成员上独立的二三层业务配置，并确保对端采用相同模式及 MTU。

## 配置案例

聚合接口默认L3，支持static和LACP；成员必须是物理接口并满足兼容属性。加入后，成员不再允许独立配置L2/L3参数，聚合无关的ACL/QoS绑定按能力保留。

```text
interface Eth-Trunk 10
 mode lacp-static
 trunkport Ethernet 1 to Ethernet 2
 mtu 9000
 ip address 198.51.100.1 255.255.255.0
```

```vortexros-cli
display eth-trunk 10
display interface Eth-Trunk 10
```

删除单个成员或整个聚合接口：

```text
interface Eth-Trunk 10
 undo trunkport Ethernet 2
quit
undo interface Eth-Trunk 10
commit
```

成员口退出聚合后，才可重新配置其独立的二层/三层属性。

### 两台设备双链路 LACP

两端 Ethernet1 对接 Ethernet1、Ethernet2 对接 Ethernet2。清空成员口独立地址与交换配置。两端均用 Eth-Trunk10，管理地址为 192.0.2.1/24 和 .2/24。

**本端设备**

```vortexros-config
interface Eth-Trunk 10
 mode lacp-static
 trunkport Ethernet 1 to Ethernet 2
 ip address 192.0.2.1 255.255.255.0
#
return
```

**对端设备**

```vortexros-config
interface Eth-Trunk 10
 mode lacp-static
 trunkport Ethernet 1 to Ethernet 2
 ip address 192.0.2.2 255.255.255.0
#
return
```

```vortexros-cli
display eth-trunk 10
display interface brief
display ip interface brief
```

配置提交后，两端应看到 Eth-Trunk10 up，两个成员均被选中，接口简表里成员位于聚合项下方。持续 ping 对端后断开一根成员链路，聚合仍 up 并由另一根链路转发。接回后复查两成员。

## 验证配置

```vortexros-cli
display eth-trunk 10
display interface brief
```

确认成员状态符合预期。检查 Eth-Trunk10 及其成员，再断开一根链路验证剩余成员是否仍能转发。
