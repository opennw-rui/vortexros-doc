# 系统设置与远程管理

- [设备名称与登录提示](02-system-services/identity.md)。给设备配置名称，便于在终端和运维记录中识别。
- [本地 AAA 与用户权限](02-system-services/local-aaa.md)。本地 AAA 管理登录设备的账户和操作权限，适用于 Console 和 SSH 管理。默认认证域为 default，采用本地认证。Level 1 为只读、Level 2 为网络管理员、Level 3 为系统管理员。
- [STelnet 与 VTY](02-system-services/stelnet.md)。STelnet 通过 SSH 提供远程 CLI。VTY 管理远端会话数量和空闲超时。
- [SSH 公钥认证](02-system-services/ssh-public-key.md)。将用户的 OpenSSH 公钥导入设备并按名称关联到账户，适用于管理终端的免口令公钥认证。
- [本机 DNS 解析](02-system-services/dns.md)。动态 DNS 解析让设备通过主机名访问管理或网络服务。设备自身的 DNS 请求走默认路由表。
- [系统时区](02-system-services/timezone.md)。时区决定时间、运行状态和日志的本地显示方式。它不改变时间同步所使用的实际时刻。
- [NTP 时间同步](02-system-services/ntp.md)。NTP 使设备向指定时间源同步时钟。可使用 IPv4、IPv6 及独立的管理 VPN。
- [离线设备授权](02-system-services/licensing.md)。设备管理员可以导出授权申请文件并导入与本机匹配的授权文件。适用于不直接接入签发服务的设备。

```{toctree}
:maxdepth: 1
:hidden:

02-system-services/identity
02-system-services/local-aaa
02-system-services/stelnet
02-system-services/ssh-public-key
02-system-services/dns
02-system-services/timezone
02-system-services/ntp
02-system-services/licensing
```
