# 服务状态与监听端口

## 功能介绍

设备提供服务、健康状态和监听端口查询，可用来区分连通性问题与本地服务未启动。

## 配置准备

确定希望排查的服务和协议。远程排查前保留当前会话。

## 配置案例

以 SSH 不通为例，先确认管理接口与路由，再核对 TCP 监听和 SSH 登录记录。服务状态异常时同时查看告警。

```vortexros-cli
display ip interface brief
display process tcp listen
display ssh user login-info failed
```

## 验证配置

```vortexros-cli
display service verbose
display health
display process listen
display process udp listen
display alarm active
```

核对协议、监听地址、端口和主进程。恢复后从远端新建连接，确认业务可用。
