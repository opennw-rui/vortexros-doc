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

### 两端对照管理口接线

用一根网线把 R1 的 Ethernet0 接到 R2 的 Ethernet2。两端在系统视图都执行以下配置并提交。

```text
enable lldp
commit
```

```vortexros-cli
display lldp local
display lldp neighbor brief
display lldp neighbor interface Ethernet0
```

R1 应看到远端的设备名及 Ethernet2，R2 应在 Ethernet2 看到 R1 的 Ethernet0。更换接线后，等待旧条目过期并检查新条目。

## 验证配置

```vortexros-cli
display lldp neighbor brief
display lldp neighbor interface Ethernet0
```

检查本地 Ethernet0 对应的远端设备和端口，等待下一个通告周期后复查变更。
