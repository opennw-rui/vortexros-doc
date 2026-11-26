# 本地 AAA 与用户权限

## 功能介绍

本地 AAA 管理登录设备的账户和操作权限，适用于 Console 和 SSH 管理。默认认证域为 default，采用本地认证。Level 1 为只读、Level 2 为网络管理员、Level 3 为系统管理员。

## 配置准备

使用 Level 3 登录。新增管理员时保留已验证的 Console 会话。

## 配置案例

创建一个只读账户 audit。输入密码命令时按交互提示录入设备专用口令。

```text
system-view
aaa
local-user audit privilege level 1
local-user audit password irreversible-cipher
local-user audit service-type terminal ssh
quit
commit
return
```

## 验证配置

```vortexros-cli
display aaa user audit
display current-configuration configuration aaa
```

检查 audit 的权限等级和允许的服务，再用该账户登录，确认可以查询状态。已保存的口令显示为不可逆校验值。新增后先验证再执行 save。
