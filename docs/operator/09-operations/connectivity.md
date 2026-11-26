# Ping、Tracert 与 MTR 连通性诊断

## 功能介绍

Ping 检查端到端可达性，Tracert 查看逐跳路径，MTR 持续观察丢包与延迟。可从指定 VPN 进行诊断。

## 配置准备

准备目标地址，先确认应该使用默认路由表还是业务 VPN。

## 配置案例

```vortexros-cli
ping 192.0.2.1
ping -vpn-instance BLUE 10.0.0.1
tracert 198.51.100.1
mtr -vpn-instance BLUE 10.0.0.1
```

按 Ctrl+C 结束当前诊断命令，保留登录会话。

## 验证配置

```vortexros-cli
display ip routing-table vpn-instance BLUE
display ip interface brief
```

确认目标已匹配所需路由及出接口。比较实际 Ping 和路径结果；防火墙阻止 ICMP 时，再验证业务所用的协议。
