---
nav_title: BFD 快速故障检测
nav_overview: 介绍
nav_feature: true
---


(section-operator-05-dynamic-routing-bfd-1)=
# BFD 快速故障检测

<span id="overview"></span>

BFD 快速检测两个转发端点之间的可达性。可独立建立会话，也可配合动态路由协议加速故障收敛。

<span id="principles"></span>

(section-operator-05-dynamic-routing-bfd-2)=
## 工作原理

BFD 独立探测相邻转发路径。协商检测间隔并进入 Up 后，连续缺少对端控制包达到检测条件会导致 Down。上层协议订阅 BFD 才会按该状态切换。核对 BFD 状态、上层路由和实际业务恢复。

可独立或由动态路由协议建立快速故障检测会话。间隔和检测倍数共同决定检测速度。

<span id="examples"></span>

(section-operator-05-dynamic-routing-bfd-3)=
## 配置与验证

(case-conditions-05-dynamic-routing-bfd)=
### 配置条件

确保两端已经具有可用的三层路径。按链路条件确定计时及检测次数。

BFD可建立独立会话，也可由OSPF、IS-IS、RIP和BGP邻居调用。协议会话默认发送间隔1000ms、接收间隔1000ms、检测次数3。

```{toctree}
:maxdepth: 1

bfd/cases/example-1
bfd/cases/example-2
bfd/cases/example-3
bfd/cases/example-4
```

(case-verification-05-dynamic-routing-bfd)=
### 通用验证

```vortexros-cli
display bfd configuration
display bfd session all
display bfd statistics
```

先确认会话 Up。受控断开链路后，检查会话 Down 和引用该会话的协议是否切换，恢复链路后复查。

<span id="observed"></span>

实测节选中的物理接口按文档端口编号记为 EthernetX。其他表项保留原始验证值。

(recorded-result-05-dynamic-routing-bfd)=
### 动态 BFD 检测故障的实测结果

在 OSPFv3 主路径使用动态单跳 BFD。会话建立后，超时的原因显示 `control-expired`。此时业务走备路径，恢复主链路后会话重新进入 up。实际协议事件节选如下。

```text
2026/11/26 06:15:33 BFD: [NQM5A-CJBHQ] Session-Change: [mhop:no peer:fe80::ff:fe02:1202 local:fe80::ff:fe01:1201 vrf:default ifname:Ethernet0] init -> up
2026/11/26 06:15:53 BFD: [NQM5A-CJBHQ] Session-Change: [mhop:no peer:fe80::ff:fe02:1202 local:fe80::ff:fe01:1201 vrf:default ifname:Ethernet0] down -> up
2026/11/26 06:15:45 BFD: [STTY2-28ZPH] Session-Change: [mhop:no peer:fe80::ff:fe02:1202 local:fe80::ff:fe01:1201 vrf:default ifname:Ethernet0] up -> down reason:control-expired
```

(section-operator-05-dynamic-routing-bfd-4)=
### 会话建立后的实际回显

三节点中 R1 的 IPv6 动态会话进入 Up。对照 Peer、Interface 和 State，可确认故障前接受探测的链路。

```text
<VortexROS> display bfd session all
BFD Session Brief Information
-------------------------------------------------------------------------------------------
Name     Peer                Local      Remote     VPN      Interface   Mode        State
dynamic  fe80::ff:fe02:1202  259268339  148741797  default  Ethernet0   Single-hop  Up
-------------------------------------------------------------------------------------------
Total session(s): 1
```

<span id="precautions"></span>

(section-operator-05-dynamic-routing-bfd-5)=
## 注意事项

启用接口级 BFD 前先启用全局 BFD。过短的检测间隔可能放大抖动，故障测试应核对邻居和路径恢复。

<p data-legacy-id="id1" class="manual-previous-section" data-section-moved><a href="#overview">介绍</a></p>
<p data-legacy-id="id2" class="manual-previous-section" data-section-moved><a href="#case-conditions-05-dynamic-routing-bfd">配置准备</a></p>
<p data-legacy-id="id3" class="manual-previous-section" data-section-moved><a href="#examples">配置案例</a></p>
<p data-legacy-id="id7" class="manual-previous-section" data-section-moved><a href="#case-verification-05-dynamic-routing-bfd">验证配置</a></p>
<p data-legacy-id="id4" class="manual-previous-section" data-section-moved><a href="cases/example-1/">独立BFD会话</a></p>
<p data-legacy-id="id5" class="manual-previous-section" data-section-moved><a href="cases/example-2/">路由协议调用BFD</a></p>
<p data-legacy-id="id6" class="manual-previous-section" data-section-moved><a href="cases/example-3/">直连双端独立 BFD 会话</a></p>
<p data-legacy-id="ospfv3-bfd" class="manual-previous-section" data-section-moved><a href="cases/example-4/">OSPFv3 联动 BFD</a></p>
