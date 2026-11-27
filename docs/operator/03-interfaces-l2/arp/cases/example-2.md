---
nav_title: 桥域静态 ARP 与超时撤销
---


# 桥域静态 ARP 与超时撤销

## 拓扑

![终端的固定 IPv4 和 MAC 绑定在 R1 的 BD 11](example-2.svg)

## 配置条件

选定具备 MAC、可以发送 ARP 的三层接口。先核对路由和实际可达性。

以 BD 11 和 Vbdif11 作为客户网关。终端地址为 10.11.0.2，网卡 MAC 为 02:11:22:33:44:55。先按 [Vbdif 网关案例](../../vbdif.md) 建好本地桥域，确保实际接入口归属 BD 11。确认终端配置固定地址后，在系统视图录入映射。

## 配置步骤

```text
arp static 10.11.0.2 02:11:22:33:44:55 bridge-domain 11
commit
```

执行 `display arp static`，应看到固定的 IPv4 和 MAC 映射，再从 Vbdif11 所在设备测试终端。维护时用对应的 `undo arp static` 撤销条目。仅需恢复默认老化时间时，使用 `undo arp timeout`，然后执行 `commit`。

## 验证方法

对照{ref}`本功能页的实测结果 <recorded-result-03-interfaces-l2-arp>`可以核对设备实际显示的字段或业务表现。不同拓扑请按本案例的地址和接口检查。

对照以下命令和预期结果核对设备状态。

```vortexros-cli
display arp static
```

静态列表应出现 10.11.0.2 和预设 MAC。终端应可达，撤销后相应静态映射消失。
