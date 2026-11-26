# SNMP 监控

## 功能介绍

SNMP 允许网管系统读取设备状态并接收通知。只读轮询支持 SNMPv2c，SNMPv3 支持 authPriv。

## 配置准备

准备管理站和设备管理接口。下例使用 v2c 联调，请将 COMMUNITY 替换为设备专用的团体名。

## 配置案例

```vortexros-config
interface Ethernet 0
 ip address 192.0.2.2 255.255.255.0
#
snmp-agent
snmp-agent sys-info version v2c
snmp-agent community read COMMUNITY
snmp-agent protocol source-interface Ethernet0
#
return
```

在系统视图录入并提交。

只读轮询支持 SNMPv2c，SNMPv3 使用 `authPriv`、SHA2-256 和 AES128。使用 `snmp-agent protocol source-interface vpn-instance NAME IFNAME` 时，先确认接口与管理实例一致且具有 IPv4 地址。授权凭据应使用设备专用值。

```vortexros-cli
display snmp-agent sys-info
display process udp listen
```

来自管理站的轮询应经实际配置的接口和路由表验证。设备查询监听使用 UDP 161，通知发送到配置的 IPv4 目标。用 `undo snmp-agent` 删除整套 SNMP 配置，并在提交后检查监听已撤销。

## 验证配置

```vortexros-cli
display snmp-agent sys-info
display snmp-agent community
display process udp listen
```

检查 UDP 161 和绑定的接口，再从实际管理站发起只读轮询。使用管理 VPN 时，检查网管路径经过正确的 VPN。
