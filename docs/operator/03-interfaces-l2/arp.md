# ARP 与代理 ARP

## 功能介绍

ARP 用于查询同链路 IPv4 下一跳的 MAC 地址。代理 ARP 由设备代指定目标响应，用于终端无法直接解析目标但设备有正确转发路径的场景。

## 配置准备

选定具备 MAC、可以发送 ARP 的三层接口。先核对路由和实际可达性。

## 配置案例

```vortexros-config
enable switch
vlan 100
#
interface Vlanif 100
 ip address 10.10.10.1 255.255.255.0
#
arp timeout 900
arp proxy 10.10.10.12 10.10.10.14 interface Vlanif 100
#
return
```

提交后，设备从所选三层接口为指定范围代理应答。用 `undo arp timeout` 恢复默认的 1200 秒，使用下列命令删除代理范围。

```text
undo arp proxy 10.10.10.12 10.10.10.14 interface Vlanif 100
commit
```

## 验证配置

```vortexros-cli
display arp
display arp proxy
display arp interface Vlanif 100
```

核对表项状态、出口和代理地址范围。在同链路终端请求其中一个目标，检查收到的响应及目标连通性。老化时间设置适用于 DPDK 数据面的邻居表。
