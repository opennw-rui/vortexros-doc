---
nav_title: Bridge Domain 与高位桥域
nav_overview: 介绍
nav_feature: true
---


(section-operator-03-interfaces-l2-bridge-domain-1)=
# Bridge Domain 与高位桥域

<span id="overview"></span>

Bridge Domain 为独立的二层业务提供转发域。可连接本地接入口，也可与 VXLAN VNI 关联以延伸至远端。

<span id="principles"></span>

(section-operator-03-interfaces-l2-bridge-domain-2)=
## 工作原理

桥域按业务隔离 MAC 学习、查表和泛洪范围。接入口或子接口负责把报文归入桥域，VXLAN 用 VNI 标识跨设备的同一服务。相同客户 VID 或 MAC 出现在不同桥域时分别学习和转发。普通交换 VLAN 按自己的 VID 处理。

BD 提供独立的二层转发域，可关联 VLAN、VNI 与 Vbdif。高位 BD 编号与普通 VLAN ID 独立。

<span id="examples"></span>

(section-operator-03-interfaces-l2-bridge-domain-3)=
## 配置与验证

(case-conditions-03-interfaces-l2-bridge-domain)=
### 配置条件

普通 VLAN 的可用 VID 为 1–4094。高位 BD 可使用 4096–4294967294，适用于显式引用桥域的业务。普通 STP、RSTP 和 MSTP 的适用范围不变。

```{toctree}
:maxdepth: 1

bridge-domain/cases/example-1
bridge-domain/cases/example-2
```

(case-verification-03-interfaces-l2-bridge-domain)=
### 通用验证

```vortexros-cli
display bridge-domain 11
display bridge-domain 65536
display mac-address
display vxlan tunnel
```

确认本地接口、VNI 与远端 VTEP 归属。高位域之间可以重复使用客户 VID 或 MAC，分别验证域内连通、域间隔离，并确认迁移后的旧远端条目已撤销。

[Vbdif 网关](vbdif.md) · [VXLAN EVPN](../06-tunnels/vxlan-evpn.md)

<span id="observed"></span>

(recorded-result-03-interfaces-l2-bridge-domain)=
### 运行查询实测节选

r4 桥域 101 绑定服务 VNI。下例检查桥域状态和其实际绑定值。

```text
<VortexROS> display bridge-domain 101
Forwarding      : on    Unknown unicast flood : off    Learning      : on
ARP termination : off   ARP unicast forward   : off    MAC aging (s) : 0

VNI: 101
BVI: Vbdif101

BDID        State       Flood       Description
-------------------------------------------------------------------------------
101         up          enable      --
-------------------------------------------------------------------------------

Ports  State  SHG
-------------------------------------------------------------------------------
--     --     --
```

(section-operator-03-interfaces-l2-bridge-domain-4)=
### 高位桥域的实测结果

三台 VTEP 验证了两个高位桥域使用同一组播组时互相隔离。每个桥域按本域订阅和来源选择出口，未订阅流量不会送往该出口。双栈 MAC/IP 可学习、迁移和独立撤销。已知地址的 ARP/ND 可由本地应答，未知请求继续转发。

<span id="precautions"></span>

(section-operator-03-interfaces-l2-bridge-domain-5)=
## 注意事项

普通 VLAN VID 1–4094。跨设备延伸业务时核对 VNI 和 RT。移除 BD 前先解除接入口、Vbdif、VLAN 和 VNI 引用。

<p data-legacy-id="id1" class="manual-previous-section" data-section-moved><a href="#overview">介绍</a></p>
<p data-legacy-id="id2" class="manual-previous-section" data-section-moved><a href="#case-conditions-03-interfaces-l2-bridge-domain">配置准备</a></p>
<p data-legacy-id="id3" class="manual-previous-section" data-section-moved><a href="#examples">配置案例</a></p>
<p data-legacy-id="id4" class="manual-previous-section" data-section-moved><a href="#case-verification-03-interfaces-l2-bridge-domain">验证配置</a></p>
<p data-legacy-id="bd-evpn" class="manual-previous-section" data-section-moved><a href="cases/example-2/">高位 BD 动态 EVPN 配置</a></p>
