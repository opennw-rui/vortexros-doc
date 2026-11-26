# MAC 地址表

## 功能介绍

通过 MAC 地址表确认设备把流量转发到哪个端口，也可调整动态表项的老化时间。

## 配置准备

在已经可以收发流量的 VLAN 上观察动态学习。全局老化时间调整会影响已有 VLAN。

## 配置案例

启用交换功能后，每个VLAN对应的转发域默认采用以下行为：

- 动态MAC学习：开启；
- 广播和组播泛洪：开启；
- 未知单播泛洪：开启；
- 二层转发：开启；
- 动态MAC老化时间：300秒。

动态MAC老化时间是全局参数。需要修改时，在系统视图执行：

```text
mac-address aging-time 600
commit
```

提交后，所有VLAN对应转发域的动态MAC老化时间变为600秒。恢复默认值：

```text
undo mac-address aging-time
commit
```

默认值不显示在配置中；只有非默认值才进入 `display current-configuration`。配置值必须是 60 秒的整数倍。

### 配置静态 MAC 表项

已知终端的固定接入口时，可在对应桥域中配置静态表项。以下示例要求 Ethernet0 已属于 BD 11。

```text
mac-address static 02:11:22:33:44:55 Ethernet0 bridge-domain 11
commit
```

提交后检查该 MAC 的固定出口。搬迁终端时先更新或撤销该表项，再验证流量到达新位置。

## 验证配置

```vortexros-cli
display mac-address
display current-configuration | include aging-time
```

检查动态表项的 VLAN、MAC 和出接口。停止指定终端的流量后，可观察表项何时从列表中移除。
