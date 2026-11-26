---
nav_title: VRRP 与 VRRP6 网关冗余
nav_overview: 介绍
nav_feature: true
---


(section-operator-05-dynamic-routing-vrrp-1)=
# VRRP 与 VRRP6 网关冗余

<span id="overview"></span>

VRRP 让多台设备共用虚拟网关，适用于接入网段的网关冗余。IPv4 默认 VRRPv2，IPv6 使用 VRRPv3。

<span id="principles"></span>

(section-operator-05-dynamic-routing-vrrp-2)=
## 工作原理

组内只有 Master 对外承担虚拟网关。Backup 监听通告，主设备失效后参与选举。检查组角色、虚拟地址和通告方式，并从客户端经虚拟网关发流量确认切换。协议版本、地址族和单播参数应在两端匹配。

IPv4 默认 VRRPv2，IPv6 使用 VRRPv3。v3 可配置单播。优先级、抢占和接口跟踪决定切换。

<span id="examples"></span>

(section-operator-05-dynamic-routing-vrrp-3)=
## 配置与验证

(case-conditions-05-dynamic-routing-vrrp)=
### 配置条件

两台设备接在同一二层网段，使用不同真实地址、相同 VRID 和虚拟地址。启用跟踪前配置被跟踪接口。

VRRP 让两台或多台设备共享一个网关地址。可在三层 Ethernet、Eth-Trunk、三层子接口、Vlanif 或 Vbdif 配置。IPv4 默认使用 VRRPv2。IPv6 固定使用 VRRPv3，需要配置本组的链路本地虚拟地址。

```{toctree}
:maxdepth: 1

vrrp/cases/example-1
vrrp/cases/example-2
vrrp/cases/dual-stack-vrrp-unicast
```

(case-verification-05-dynamic-routing-vrrp)=
### 通用验证

```vortexros-cli
display vrrp brief
display vrrp interface Vlanif 100
display vrrp6 brief
```

确认主备用状态和运行优先级。持续从终端发送流量，断开主设备上联再恢复，检查网关迁移与转发恢复。

(section-operator-05-dynamic-routing-vrrp-4)=
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

<span id="observed"></span>

(recorded-result-05-dynamic-routing-vrrp)=
### 双栈主备切换的实测结果

Vlanif200 的双栈单播验收覆盖初次选举、故障切换和恢复，稳定后的每阶段双栈探测均收到 3/3 回包。撤销单播配置并提交后，线侧再次出现 IPv4 和 IPv6 的组播 VRRP 通告。下面是对照正常回稳的实际抓包节选。

```text
07:46:48.080701 IP 198.51.100.1 > 224.0.0.18: VRRPv3, Advertisement, vrid 10, prio 120, intvl 100cs, length 12
07:46:49.107364 IP6 fe80::537e:a562:429d:ee73 > ff02::12: VRRPv3, Advertisement, vrid 10, prio 120, intvl 100cs, length 40
```

(section-operator-05-dynamic-routing-vrrp-5)=
### 双栈单播对端实测回显

两台设备在 Vlanif200 上使用同一 VRID。以下分别节选主设备的 IPv4 和 IPv6 对端字段。IPv6 使用对端链路本地地址。

```text
<VortexROS> display vrrp interface Vlanif200 10 verbose
    Unicast peers  : 198.51.100.2
```

```text
<VortexROS> display vrrp6 interface Vlanif200 10 verbose
    Unicast peers  : fe80::ff:fe00:220
```

<span id="precautions"></span>

(section-operator-05-dynamic-routing-vrrp-6)=
## 注意事项

两端需使用相同 VRID、版本和虚拟地址，真实地址应互不冲突。单播 IPv6 peer 配真实链路本地地址。切换测试应从终端观察实际转发。

(section-operator-05-dynamic-routing-vrrp-7)=
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

<p data-legacy-id="id1" class="manual-previous-section" data-section-moved><a href="#overview">介绍</a></p>
<p data-legacy-id="id2" class="manual-previous-section" data-section-moved><a href="#case-conditions-05-dynamic-routing-vrrp">配置准备</a></p>
<p data-legacy-id="id3" class="manual-previous-section" data-section-moved><a href="#examples">配置案例</a></p>
<p data-legacy-id="id6" class="manual-previous-section" data-section-moved><a href="#case-verification-05-dynamic-routing-vrrp">验证配置</a></p>
<p data-legacy-id="id4" class="manual-previous-section" data-section-moved><a href="#case-verification-05-dynamic-routing-vrrp">查看状态和效果</a></p>
<p data-legacy-id="id5" class="manual-previous-section" data-section-moved><a href="#precautions">修改和删除</a></p>
<p data-legacy-id="ipv4" class="manual-previous-section" data-section-moved><a href="cases/example-1/">IPv4完整示例</a></p>
<p data-legacy-id="ipv6" class="manual-previous-section" data-section-moved><a href="cases/example-2/">IPv6示例</a></p>
<p data-legacy-id="vrrpv3" class="manual-previous-section" data-section-moved><a href="cases/dual-stack-vrrp-unicast/">双栈 VRRPv3 单播网关</a></p>
