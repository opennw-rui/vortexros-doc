# LLDP 邻居发现

## 功能介绍

LLDP 发现直连链路另一端的设备与端口，适用于核对链路接线和邻接关系。

## 配置准备

在需观察的链路两端启用 LLDP，并确认物理链路已连接。

## 配置案例

```text
enable lldp
commit
display lldp neighbor brief
display lldp neighbor interface Ethernet0
```

关闭LLDP：

```text
undo lldp enable
commit
```

## 验证配置

```vortexros-cli
display lldp neighbor brief
display lldp neighbor interface Ethernet0
```

检查本地 Ethernet0 对应的远端设备和端口，等待下一个通告周期后复查变更。
