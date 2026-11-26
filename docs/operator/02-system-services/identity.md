# 设备名称与登录提示

## 功能介绍

设备名称用于区分不同站点和角色的设备。设置后，CLI 提示符会显示新名称，便于运维人员确认当前会话。

## 配置准备

按站点和角色选用设备名称。下例使用 EDGE-01，可替换为实际名称。

## 配置案例

在系统视图输入以下配置并提交。

```vortexros-config
sysname EDGE-01
#
return
```

如果原会话还显示旧提示符，可开启新会话查看。确认后执行 `save`。

## 验证配置

```vortexros-cli
display current-configuration | include sysname
display version
```

检查配置中是否为 `sysname EDGE-01`，并从新会话核对 CLI 提示符。修改名称时重复同样步骤。
