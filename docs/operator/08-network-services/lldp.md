---
nav_title: LLDP 邻居发现
nav_overview: 介绍
nav_feature: true
---


(section-operator-08-network-services-lldp-1)=
# LLDP 邻居发现

<span id="overview"></span>

LLDP 发现直连链路另一端的设备与端口，适用于核对链路接线和邻接关系。

<span id="principles"></span>

(section-operator-08-network-services-lldp-2)=
## 工作原理

LLDP 周期发送本地设备及端口信息，接收设备在对应接口维护邻居。它适合在没有 IP 地址时核对直接接线，不能替代跨网段的连通性检查。

LLDP 发现直连设备与端口，可查询本端和邻居信息。

<span id="examples"></span>

(section-operator-08-network-services-lldp-3)=
## 配置与验证

(case-conditions-08-network-services-lldp)=
### 配置条件

在需观察的链路两端启用 LLDP，并确认物理链路已连接。

```{toctree}
:maxdepth: 1

lldp/cases/example-1
lldp/cases/example-2
```

(case-verification-08-network-services-lldp)=
### 通用验证

```vortexros-cli
display lldp neighbor brief
display lldp neighbor interface Ethernet0
```

检查本地 Ethernet0 对应的远端设备和端口，等待下一个通告周期后复查变更。

<span id="observed"></span>

实测节选中的物理接口按文档端口编号记为 EthernetX。其他表项保留原始验证值。

(recorded-result-08-network-services-lldp)=
(lab-result-operator-08-network-services-lldp)=
### 两台设备交换邻居信息的实测回显

三节点测试中，两台设备经两条独立链路发送 LLDP。P1 实测回显节选如下。通过 Local Intf 和 Neighbor Intf 核对每条链路的实际接线。

```text
<P1> display lldp neighbor brief
Local Intf  Neighbor Dev    Neighbor Intf  Exptime (sec)
-------------------------------------------------------------------------------
Ethernet4   02fe-7b01-5196  Ethernet4      115
Ethernet5   02fe-e803-861b  Ethernet5      115
```

<span id="precautions"></span>

(section-operator-08-network-services-lldp-4)=
## 注意事项

邻居显示依赖链路和对端 LLDP。改线后等待重新通告或旧条目到期。

<p data-legacy-id="id1" class="manual-previous-section" data-section-moved><a href="#overview">介绍</a></p>
<p data-legacy-id="id2" class="manual-previous-section" data-section-moved><a href="#case-conditions-08-network-services-lldp">配置准备</a></p>
<p data-legacy-id="id3" class="manual-previous-section" data-section-moved><a href="#examples">配置案例</a></p>
<p data-legacy-id="id5" class="manual-previous-section" data-section-moved><a href="#case-verification-08-network-services-lldp">验证配置</a></p>
<p data-legacy-id="id4" class="manual-previous-section" data-section-moved><a href="cases/example-2/">两端对照管理口接线</a></p>
