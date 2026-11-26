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

### 桥域静态 ARP 与超时撤销

以 BD 11 和 Vbdif11 作为客户网关。终端地址为 10.11.0.2，网卡 MAC 为 02:11:22:33:44:55。先按 [Vbdif 网关案例](vbdif.md) 建好本地桥域，确保实际接入口归属 BD 11。确认终端配置固定地址后，在系统视图录入映射。

```text
arp static 10.11.0.2 02:11:22:33:44:55 bridge-domain 11
commit
```

执行 `display arp static`，应看到固定的 IPv4 和 MAC 映射，再从 Vbdif11 所在设备测试终端。维护时用对应的 `undo arp static` 撤销条目。仅需恢复默认老化时间时，使用 `undo arp timeout`，然后执行 `commit`。
