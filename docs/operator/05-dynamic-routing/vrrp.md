# VRRP 与 VRRP6 网关冗余

## 功能介绍

VRRP 让多台设备共用虚拟网关，适用于接入网段的网关冗余。IPv4 默认 VRRPv2，IPv6 使用 VRRPv3。

## 配置准备

两台设备接在同一二层网段，使用不同真实地址、相同 VRID 和虚拟地址。启用跟踪前配置被跟踪接口。

## 配置案例

VRRP 让两台或多台设备共享一个网关地址。可在三层 Ethernet、Eth-Trunk、三层子接口、Vlanif 或 Vbdif 配置。IPv4 默认使用 VRRPv2。IPv6 固定使用 VRRPv3，需要配置本组的链路本地虚拟地址。

### IPv4完整示例

假设P1与P2都连接到VLAN 100，客户端使用 `10.100.0.254`作为默认网关。P1优先级120作为Master，P2保持默认优先级100作为Backup。

P1：

```text
interface Vlanif 100
 ip address 10.100.0.1 255.255.255.0
 vrrp vrid 10 virtual-ip 10.100.0.254
 vrrp vrid 10 priority 120
 vrrp vrid 10 timer advertise 1
 vrrp vrid 10 track interface Vlanif 200 reduced 30
```

P2：

```text
interface Vlanif 100
 ip address 10.100.0.2 255.255.255.0
 vrrp vrid 10 virtual-ip 10.100.0.254
 vrrp vrid 10 timer advertise 1
```

IPv4 用首条 `virtual-ip` 创建组。默认优先级为 100、通告间隔为 1 秒、抢占开启。在 P1 已配置的 Vlanif200 断开后，P1 的运行优先级降低 30。若低于 P2，P2 接管虚拟网关。

需要 IPv4 VRRPv3 时，在两端系统视图执行 `vrrp version v3` 并提交。用 `undo vrrp version` 恢复 IPv4 的 v2 默认值。此前保存的按组 v3 配置仍可回放。单播要求 v3，通过 `peer-ip` 配置同链路对端真实地址。IPv6 单播使用对端链路本地地址。删除某个地址族的最后一个对端后，该族恢复组播。

虚拟IP可以与接口自身地址相同。此时设备是该虚拟地址的地址拥有者，运行优先级自动为255；配置中仍保留用户输入的优先级，状态显示以运行优先级为准。

### IPv6示例

```text
interface Vlanif 100
 ipv6 address 2001:db8:100::1 64
 vrrp6 vrid 20 virtual-ip fe80::fe
 vrrp6 vrid 20 virtual-ip 2001:db8:100::fe
 vrrp6 vrid 20 priority 120
 vrrp6 vrid 20 timer advertise 1
```

两端使用相同的 VRID 和虚拟地址。IPv6 的全局虚拟地址可与链路本地虚拟地址同组使用。

### 查看状态和效果

```vortexros-cli
display vrrp brief
display vrrp interface Vlanif 100
display vrrp 10
display vrrp statistics
display vrrp6 brief
```

brief输出示例：

```text
VRID  State   Interface  Type  Virtual IP      Priority  RunPri  Adv
10    Master  Vlanif100  IPv4  10.100.0.254   120       120     1.00s
```

详细输出会显示状态、版本、地址族、虚拟IP、配置优先级、运行优先级、虚拟MAC、通告间隔和抢占状态。配置已经提交但VRRP组尚未创建时，State显示 `Pending (not created in dataplane)`，应检查接口模式、地址和服务健康状态。

业务验证应包括：客户端持续ping虚拟IP和外部地址；关闭Master的上联或被跟踪接口；确认Backup接管、ARP/ND更新且业务恢复；再恢复接口并观察抢占行为。

### 修改和删除

```text
interface Vlanif 100
 undo vrrp vrid 10 track interface Vlanif 200
 undo vrrp vrid 10 priority
 undo vrrp vrid 10 timer advertise
 undo vrrp vrid 10 virtual-ip 10.100.0.254
 undo vrrp vrid 10
```

`undo priority`恢复100，`undo timer advertise`恢复1秒，`undo preempt-mode`恢复抢占。`undo vrrp vrid 10`删除整个IPv4组；IPv6使用对应的 `undo vrrp6 vrid 20 ...`。

## 验证配置

```vortexros-cli
display vrrp brief
display vrrp interface Vlanif 100
display vrrp6 brief
```

确认主备用状态和运行优先级。持续从终端发送流量，断开主设备上联再恢复，检查网关迁移与转发恢复。
