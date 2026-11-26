# 系统、访问与服务

Console 和受管 SSH 登录后直接进入产品 CLI。首次安装使用安装时设置的本地管理员密码。恢复出厂或从空配置启动后，先在 Console 完成首次改密。

## 本地 AAA、SSH 与 VTY

当前认证域为内建 `default`，使用本地认证。Level 1 为只读，Level 2 为网络管理员，Level 3 为系统管理员。在 AAA 视图配置 `local-user`。可按用户限制终端或 SSH 服务。启用远程登录前，保留可用的 Console 并准备已授权的账户。

```text
system-view
stelnet server enable
ssh server port 2222
user-interface maximum-vty 5
user-interface vty
idle-timeout 10
quit
commit
return
display users
display aaa user vortexros
```

在另一终端以 SSH 实际登录后执行 `save`。`display users` 显示 Console、VTY、远端地址和会话状态。`display ssh user login-info failed` 或 `display ssh user vortexros login-info succeeded` 可按结果和用户查询。

## 导入 SSH 公钥

在系统视图输入 `rsa peer-public-key workstation encoding-type openssh`。进入命名视图后执行 `public-key-code begin`，在下一行粘贴本机的 OpenSSH 公钥整行或 Base64 数据。执行 `public-key-code end` 完成录入，`peer-public-key end` 返回系统视图。

```text
ssh user vortexros assign rsa-key workstation
commit
return
display aaa user vortexros
```

Ed25519 使用 `ed25519 peer-public-key` 和 `assign ed25519-key`。撤销时用 `undo ssh user vortexros assign rsa-key workstation`，提交后从独立会话验证相应密钥已经失效。

Level 3 可通过 `display current-configuration configuration aaa` 查看已提交的 AAA 配置。已设口令以 `password irreversible-cipher` 对应的不可逆校验值显示。包含该字段的配置备份需按凭据材料保管。

## DNS、时区与 NTP

本机 DNS 查询使用默认路由表。配置 DNS 时先确认服务器在默认表可达。时区使用 IANA 名称，可用 `clock timezone ?` 选择。系统视图配置后执行 `commit`，用户视图的时区更改会立即提交。执行 `save` 使更改随启动配置回放。用 `display clock` 核对本地时间，`undo clock timezone` 恢复 UTC。

```text
system-view
dns resolve
dns server 192.0.2.53
clock timezone Asia/Shanghai
commit
return
display dns server
```

将示例地址换成环境中的 DNS 服务器。`undo dns server 192.0.2.53` 撤销此地址，`undo dns resolve` 关闭动态解析。

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

## 状态查询、监听端口与日志

```vortexros-cli
display service
display health
display alarm active
display process listen
display process tcp listen
display process udp listen
display logbuffer
display logbuffer service frr last 30
```

`display logbuffer` 可查询受管服务和协议状态，包括接口、Vlanif、Vbdif、动态路由邻居、BFD 与 VRRP。每条输出包含一份本地时间。跨日期或系统启动追溯时，使用带日期的系统 journal。

Console 默认显示实时日志，SSH 默认关闭。用户视图的 `terminal monitor` 或 `undo terminal monitor` 只影响当前终端。系统视图执行 `undo info-center enable` 并提交后，所有终端暂停实时显示。历史日志仍可查询。恢复全局显示用 `info-center enable` 并提交。

[首次启动](../installation/06-first-start.md) · [故障处理](09-operations.md)
