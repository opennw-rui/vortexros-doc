---
nav_title: 配置代理 ARP 地址范围
---


# 配置代理 ARP 地址范围

## 拓扑

![终端接入 R1 的 VLAN 100，R1 为指定地址应答代理 ARP](example-1.svg)

## 配置条件

选定具备 MAC、可以发送 ARP 的三层接口。先核对路由和实际可达性。

## 配置步骤

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

## 验证方法

对照{ref}`本功能页的实测结果 <recorded-result-03-interfaces-l2-arp>`可以核对设备实际显示的字段或业务表现。不同拓扑请按本案例的地址和接口检查。

对照以下命令和预期结果核对设备状态。

```vortexros-cli
display arp proxy
display arp interface Vlanif 100
```

查询 Vlanif100 的代理范围。从同链路验证设备对指定地址应答，并检查真实目标可达。
