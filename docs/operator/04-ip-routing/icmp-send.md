---
nav_feature: true
---

# IPv4 ICMP 发送控制

接口可按名称或 Type/Code 限制设备自己产生的 IPv4 ICMP 报文。这个功能用于控制设备主动探测、应答和错误反馈。

## 工作原理

在报文实际发出的三层接口上执行策略。对于去程与回程走不同端口的业务，应检查回程选中的出接口。经过设备转发的 ICMP 和 IPv6 ICMP 不属于此功能。

`icmp name ttl-exceeded` 对应 Type 11、Code 0。`icmp type 11` 覆盖 Type 11 的所有 Code，`icmp type 11 code 0` 只覆盖 Code 0。整类规则和精确规则独立存在。若两种同时配置，撤销精确规则时整类规则仍生效。

## 配置与验证

### 验证三层接口对 Ping 的本机应答

![测试终端通过 Ethernet0 连接 R1](icmp-send/echo.svg)

R1 的 Ethernet0 为 `192.0.2.1/24`，对端测试终端为 `192.0.2.2/24`。先确认对端能够 Ping 到 R1，并从独立管理连接配置该端口。

```vortexros-cli
system-view
interface Ethernet 0
 ip address 192.0.2.1 255.255.255.0
 icmp name echo-reply
 quit
commit
return
display icmp interface Ethernet 0
```

预期规则列表有 `name echo-reply`，`Configured` 显示 `deny`，实际负责本机发包的后端显示安装状态。有些设备的 VPP 不运行，按当前数据面核对相应列。对端再 Ping `192.0.2.1`，本机 Echo Reply 应停止。要确认普通业务正常，可另用已知可达的远端目的地址做经过 R1 的转发对照。

```vortexros-cli
system-view
interface Ethernet 0
 undo icmp name echo-reply
 quit
commit
return
display icmp interface Ethernet 0
```

撤销后复测 Ping。开发版的非对称回程实测还验证了另一种场景。仅在入接口禁用 TTL 超时反馈时仍收到 ICMP 11/0。改成实际出接口禁用后，反馈停止，同路径的普通 UDP 继续转发。

## 注意事项

限制 `fragmentneed-dfset`（Type 3、Code 4）可能影响 IPv4 路径 MTU 探测。远程设备修改前保留独立管理通道。两端验证后再保存。
