---
nav_title: 配置案例
nav_overview: 案例索引
---


# VRRP 与 VRRP6 网关冗余 配置案例

(case-conditions-05-dynamic-routing-vrrp)=
## 配置条件

两台设备接在同一二层网段，使用不同真实地址、相同 VRID 和虚拟地址。启用跟踪前配置被跟踪接口。

VRRP 让两台或多台设备共享一个网关地址。可在三层 Ethernet、Eth-Trunk、三层子接口、Vlanif 或 Vbdif 配置。IPv4 默认使用 VRRPv2。IPv6 固定使用 VRRPv3，需要配置本组的链路本地虚拟地址。

```{toctree}
:maxdepth: 1

cases/example-1
cases/example-2
cases/dual-stack-vrrp-unicast
```

(case-verification-05-dynamic-routing-vrrp)=
## 通用验证

```vortexros-cli
display vrrp brief
display vrrp interface Vlanif 100
display vrrp6 brief
```

确认主备用状态和运行优先级。持续从终端发送流量，断开主设备上联再恢复，检查网关迁移与转发恢复。

## 查看状态和效果

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
