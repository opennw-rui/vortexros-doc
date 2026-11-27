---
nav_title: ARP 与代理 ARP
nav_overview: 介绍
nav_feature: true
---


(section-operator-03-interfaces-l2-arp-1)=
# ARP 与代理 ARP

<span id="overview"></span>

ARP 用于查询同链路 IPv4 下一跳的 MAC 地址。代理 ARP 由设备代指定目标响应，用于终端无法直接解析目标但设备有正确转发路径的场景。

<span id="principles"></span>

(section-operator-03-interfaces-l2-arp-2)=
## 工作原理

设备对选定的 IPv4 下一跳解析 MAC，再在正确接口向该 MAC 发送。相同 IP 在不同 VPN 或桥域中可以有不同的邻居关系。排查时先定位路由和出接口，再查 ARP 所属域。

支持查询动态邻居、配置桥域静态映射，以及在具备 MAC 的三层接口上为指定地址范围提供代理 ARP。

<span id="examples"></span>

(section-operator-03-interfaces-l2-arp-3)=
## 配置与验证

(case-conditions-03-interfaces-l2-arp)=
### 配置条件

选定具备 MAC、可以发送 ARP 的三层接口。先核对路由和实际可达性。

```{toctree}
:maxdepth: 1

arp/cases/example-1
arp/cases/example-2
```

(case-verification-03-interfaces-l2-arp)=
### 通用验证

```vortexros-cli
display arp
display arp proxy
display arp interface Vlanif 100
```

核对表项状态、出口和代理地址范围。在同链路终端请求其中一个目标，检查收到的响应及目标连通性。老化时间设置适用于 DPDK 数据面的邻居表。

<span id="observed"></span>

实测节选中的物理接口按文档端口编号记为 EthernetX。其他表项保留原始验证值。

(recorded-result-03-interfaces-l2-arp)=
### 三层邻居和桥域条目的实测回显

在同一台设备上分别查询三层动态 ARP 和桥域静态 ARP。核对 `TYPE/VLAN` 中的 `D/-` 与 `S/200`。

```text
<VortexROS> display arp 10.201.12.2
ARP Entry Types: D - Dynamic, S - Static, I - Interface, RD - Redirect
AGE: Time since last update VLAN: VLAN or Bridge Domain

IP ADDRESS      MAC ADDRESS    AGE(M)   TYPE/VLAN    INTERFACE        VPN-INSTANCE
----------------------------------------------------------------------------------------
10.201.12.2     0200-0002-1202          D/-          Ethernet0        default
----------------------------------------------------------------------------------------
Total:1         Dynamic:1        Static:0     Interface:0
Redirect:0
```

```text
<VortexROS> display arp 198.51.100.231
ARP Entry Types: D - Dynamic, S - Static, I - Interface, RD - Redirect
AGE: Time since last update VLAN: VLAN or Bridge Domain

IP ADDRESS      MAC ADDRESS    AGE(M)   TYPE/VLAN    INTERFACE        VPN-INSTANCE
----------------------------------------------------------------------------------------
198.51.100.231  0200-0011-0402          S/200        Vlanif200        ALL
----------------------------------------------------------------------------------------
Total:1         Dynamic:0        Static:1     Interface:0
Redirect:0
```

<span id="precautions"></span>

(section-operator-03-interfaces-l2-arp-4)=
## 注意事项

静态映射以实际端点 MAC 为准。部署代理 ARP 前检查目的与回程路由，避免替无实际转发路径的目标应答。

<p data-legacy-id="id1" class="manual-previous-section" data-section-moved><a href="#overview">介绍</a></p>
<p data-legacy-id="id2" class="manual-previous-section" data-section-moved><a href="#case-conditions-03-interfaces-l2-arp">配置准备</a></p>
<p data-legacy-id="id3" class="manual-previous-section" data-section-moved><a href="#examples">配置案例</a></p>
<p data-legacy-id="id4" class="manual-previous-section" data-section-moved><a href="#case-verification-03-interfaces-l2-arp">验证配置</a></p>
<p data-legacy-id="arp" class="manual-previous-section" data-section-moved><a href="cases/example-2/">桥域静态 ARP 与超时撤销</a></p>
