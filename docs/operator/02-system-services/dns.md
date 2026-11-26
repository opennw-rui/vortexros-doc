# 本机 DNS 解析

## 功能介绍

动态 DNS 解析让设备通过主机名访问管理或网络服务。设备自身的 DNS 请求走默认路由表。

## 配置准备

确认 DNS 服务器在默认路由表中可达。192.0.2.53 是示例地址。

## 配置案例

```vortexros-config
dns resolve
dns server 192.0.2.53
#
return
```

在系统视图录入后提交。撤销时用 `undo dns server 192.0.2.53` 删除该服务地址，用 `undo dns resolve` 关闭动态解析，随后提交。

## 验证配置

```vortexros-cli
display dns server
```

确认服务器列表显示配置地址，再用实际可解析的主机名测试。
