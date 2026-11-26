# RIP（IPv4）

## 功能介绍

RIP 根据跳数交换 IPv4 路由，适用于已有 RIP 设备的小型网络。

## 配置准备

在同一 IPv4 链路上配置兼容的 RIP 版本并准备要通告的网段。

## 配置案例

```text
rip 1
 version 2
 network 10.0.0.0
 default-metric 2
 maximum load-balancing 4
 timers rip 30 180 120
 silent-interface LoopBack 0
```

`network`使用IPv4主类网络地址。提交后匹配接口参加RIP，silent-interface仍发布该接口网络，但不从该接口发送更新。



## 验证配置

```vortexros-cli
display rip 1 route
display ip routing-table
```

确认邻居通告的网段与跳数，使用业务终端确认远端网络可达。
