# TCP MSS 调整

## 功能介绍

当三层路径中存在封装开销时，TCP MSS 调整可限制握手协商的报文段大小。

## 配置准备

仅在三层接口或受支持的隧道上配置。核对路径 MTU，以及 TCP 流量的实际入口和出口。

## 配置案例

TCP MSS Clamp只处理包含MSS选项的TCP SYN报文。报文中的MSS大于出接口MTU允许的上限时才会被改小；原值已经足够小或报文不是SYN时不会修改。

自动模式随接口MTU变化重新计算上限：

```text
interface Tunnel 1
 tcp mss clamp
```

也可以指定固定MSS：

```text
interface Tunnel 1
 tcp mss 1360
```

接口MTU变化后，自动模式无需重新配置。使用 `display this` 和接口统计检查配置及报文变化。删除：

```text
interface Tunnel 1
 undo tcp mss
commit
```

## 验证配置

```vortexros-cli
display interface Tunnel 1
display current-configuration | include tcp mss
```

检查接口 MTU 和已提交的 MSS 规则。通过实际 TCP 连接确认 SYN 中的 MSS 符合预期。
