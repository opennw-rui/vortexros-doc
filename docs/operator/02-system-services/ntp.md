# NTP 时间同步

## 功能介绍

NTP 使设备向指定时间源同步时钟。可使用 IPv4、IPv6 及独立的管理 VPN。

## 配置准备

确认时间源可达。使用 vpn-instance 前先创建相应的 VPN 并准备到服务器的路由。

## 配置案例

在系统视图用 `ntp-service unicast-server` 配置 IPv4，IPv6 使用 `ntp-service ipv6 unicast-server`。可指定 `vpn-instance`、`version 3` 或 `version 4`，以及 `preference`。未指定 VPN 时使用默认路由表，指定时先配置对应的 VPN 并确认服务器可达。

```text
system-view
ntp-service unicast-server 192.0.2.123 version 4
ntp-service ipv6 unicast-server 2001:db8::123 vpn-instance MGMT version 4
commit
return
display ntp-service status
display ntp-service sessions
```

设备配置只有管理实例 `MGMT` 已存在时，才可使用示例中的 VPN 参数。`display ntp-service sessions` 可核对地址、VPN、可达性和选源。用含相同地址和 VPN 的 `undo` 命令删除时间源。用 `ntp-service disable` 暂停同步，已设置的时间源会保留。用 `ntp-service enable` 恢复。

## 验证配置

```vortexros-cli
display ntp-service status
display ntp-service sessions
```

等待设备选源，核对同步状态、服务器地址、所属 VPN 和可达性。
