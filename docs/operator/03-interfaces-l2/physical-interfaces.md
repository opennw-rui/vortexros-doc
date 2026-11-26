# 物理接口与硬件卸载

## 功能介绍

物理接口可以作为三层端口或二层交换端口。接口配置包括描述、MTU、地址和受支持的硬件卸载功能。

## 配置准备

先检查网线、对端和实际接口名称。只有设备支持的卸载项才能配置。调整 MTU 前应统一链路两端参数。

## 配置案例

```text
interface Ethernet 1
 description uplink
 mtu 9000
 ip address 192.0.2.2 255.255.255.0
 undo hardware offload tso tx-checksum rx-checksum
```

先用 `display interface hardware offload Ethernet1` 查看设备支持的能力。示例同时关闭 TSO 与其依赖的收发校验和卸载。用 `hardware offload` 撤销禁用项，具体项以设备实际能力为准。



接口配置片段在系统视图录入，退出接口视图后执行 commit。

## 验证配置

```vortexros-cli
display interface brief
display interface Ethernet 1
display interface hardware offload Ethernet1
```

设备只允许一个转发平面管理物理接口。VPP未启用时，可在CLI中配置Linux能够识别的物理口；VPP接管完成后，只允许配置设备已经识别的业务接口。接管过程中接口配置暂时只读，避免同一接口同时由两套转发平面管理。

```vortexros-cli
display vpp interface-ownership verbose
display interface brief
display ip interface brief
display ipv6 interface brief
```

状态含义：`^down`表示配置对象已创建但尚不满足底层数据面创建条件；普通`down`表示底层对象存在但链路或协议条件未满足。接口无IP不应因此down。

`display interface brief`中的`CRC`只显示网卡驱动提供的硬件CRC/FCS坏帧计数；驱动或虚拟接口不支持该计数时显示`--`。它不会把接口down期间的发送尝试、转发丢弃或其他软件错误混入CRC。使用`display interface <接口>`查看CRC/FCS、丢弃、punt以及收发方向的软件错误明细。

如果 IP 简表暂时显示 unavailable 或 unknown，等待接口恢复后重新查看。

`display interface`中的最近up/down时间来自接口实际状态变化，不会因为执行display而重置。设备无法确认的历史时间显示 `-`；修改时区只会改变时间的显示方式。

InUti/OutUti 为最近 300 秒的平均速率占比。完整观察窗口形成前，摘要可能显示 0.0%。
