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

### 两端 GRE 上的双向 MSS 调整

沿用 [GRE 双端案例](../06-tunnels/gre.md)。让客户端和服务器分别位于 R1 与 R2 后方，经 Tunnel1 互通。若要验证 IPv6，先在两端隧道配置 IPv6 地址和到对端网段的回程。以下是在已有隧道上的增量，两端分别录入并提交。

```text
interface Tunnel 1
 mtu 1472
 tcp mss clamp
quit
commit
```

```vortexros-cli
display interface Tunnel 1
display current-configuration | include tcp mss
```

两端应显示 Tunnel1 为 up、MTU 1472 且配置使用自动调整。让客户端新建 TCP 连接，从隧道两侧检查握手。对原本通告较大 MSS 的普通 IPv4 TCP SYN，预期调整到不大于 1432 字节。对 IPv6 TCP SYN，预期不大于 1412 字节。已经小于上限的 MSS 保持原值。撤销后用新连接复验。
