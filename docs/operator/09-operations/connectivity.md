---
nav_title: Ping、Tracert 与 MTR 连通性诊断
nav_overview: 介绍
nav_feature: true
---


(section-operator-09-operations-connectivity-1)=
# Ping、Tracert 与 MTR 连通性诊断

<span id="overview"></span>

Ping 检查端到端可达性，Tracert 查看逐跳路径，MTR 持续观察丢包与延迟。可从指定 VPN 进行诊断。

<span id="principles"></span>

(section-operator-09-operations-connectivity-2)=
## 工作原理

| 工具 | 作用 | 何时使用 |
| --- | --- | --- |
| Ping | 发送 ICMP Echo，请求目标返回应答。 | 先确认特定源、目的或 VPN 能否双向通信。 |
| Tracert | 逐步提高 TTL 或 Hop Limit，收集沿途响应。 | 查看流量可能经过哪几跳，缩小路径排查范围。 |
| MTR | 重复探测各跳，累计应答、延迟和丢包。 | 短时间内连续观察间歇抖动，尤其是目的端状态。 |

指定 VPN 后，探测使用该实例的路由表。探测经过防火墙或被限速时，可能看到中间跳无应答而目的端仍然可达。若连通性变化与 ICMP 通告有关，参见 [ICMP 发送控制](../04-ip-routing/icmp-send.md)。

<span id="examples"></span>

(section-operator-09-operations-connectivity-3)=
## 配置与验证

(section-operator-09-operations-connectivity-4)=
### 拓扑

![R1、R2、目标端 的设备互联](connectivity/cases.svg)

(case-conditions-09-operations-connectivity)=
### 配置条件

准备目标地址，先确认应该使用默认路由表还是业务 VPN。

(section-operator-09-operations-connectivity-5)=
### 配置步骤

```vortexros-cli
ping 192.0.2.1
ping -vpn-instance BLUE 10.0.0.1
tracert 198.51.100.1
mtr -vpn-instance BLUE 10.0.0.1
```

按 Ctrl+C 结束当前诊断命令，保留登录会话。

(case-verification-09-operations-connectivity)=
### 验证方法

对照以下命令和预期结果核对设备状态。

```vortexros-cli
display ip routing-table vpn-instance BLUE
display ip interface brief
```

确认目标已匹配所需路由及出接口。比较实际 Ping 和路径结果；防火墙阻止 ICMP 时，再验证业务所用的协议。

<span id="observed"></span>

(closeout-result-operator-09-operations-connectivity)=
### 先核对设备状态再做连通性诊断

三节点验证在阻断一条聚合成员链路后仍从另一端收到 ICMP 回应。检查聚合状态和独立的去程回程可达性后再定位经过的链路。同一拓扑的实际 LACP 回显见 [Eth-Trunk](../03-interfaces-l2/eth-trunk.md)。

<span id="precautions"></span>

(section-operator-09-operations-connectivity-6)=
## 注意事项

ICMP 结果受路径中设备的限速与准入影响。用业务协议复核，避免只凭中间跳的丢包判断端到端失败。

<p data-legacy-id="id1" class="manual-previous-section" data-section-moved><a href="#overview">介绍</a></p>
<p data-legacy-id="id2" class="manual-previous-section" data-section-moved><a href="#case-conditions-09-operations-connectivity">配置准备</a></p>
<p data-legacy-id="id3" class="manual-previous-section" data-section-moved><a href="#examples">配置案例</a></p>
<p data-legacy-id="id4" class="manual-previous-section" data-section-moved><a href="#case-verification-09-operations-connectivity">验证配置</a></p>
