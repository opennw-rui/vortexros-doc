---
nav_title: 动态 VXLAN 与二层学习
nav_overview: 介绍
nav_feature: true
---


(section-operator-06-tunnels-vxlan-evpn-1)=
# BGP EVPN 与动态 VXLAN

<span id="overview"></span>

EVPN 通过 BGP 发布二层业务的远端信息，适用于无需逐个填写 VTEP 地址的 VXLAN 网络。

<span id="principles"></span>

(section-operator-06-tunnels-vxlan-evpn-2)=
## 工作原理

动态 VXLAN 使用 EVPN 的 Type-3 路由发现同一 VNI 的远端 VTEP，用 Type-2 路由通告端点 MAC 及可用的 IP。看到会话 Established 后，还要检查 VNI、MAC 路由与实际远端转发。

EVPN Type-3 让同一 VNI 的 VTEP 发现彼此。Type-2 通告客户 MAC，携带 IP 时还可用于 ARP/ND 抑制。高位 BD 使用独立域编号，可和普通 VLAN 并行运行。

<span id="examples"></span>

(section-operator-06-tunnels-vxlan-evpn-3)=
## 配置与验证

(case-conditions-06-tunnels-vxlan-evpn)=
### 配置条件

先配置两端底层接口、BGP EVPN 邻居和 VTEP 源。两个站点的 VNI 与 RT 相同，RD 分别配置。

```{toctree}
:maxdepth: 1

vxlan-evpn/cases/example-1
vxlan-evpn/cases/example-2
vxlan-evpn/cases/example-3
```

(case-verification-06-tunnels-vxlan-evpn)=
### 通用验证

```vortexros-cli
display bgp evpn peer
display bgp evpn all routing-table mac-route
display bridge-domain 65536
display vxlan tunnel
display mac-address bridge-domain 65536
```

先确认 BGP 邻居已建立，再检查远端 VTEP 和 MAC。移动终端后，确认旧位置的表项撤销且新位置学习正常。

<span id="observed"></span>

实测节选中的物理接口按文档端口编号记为 EthernetX。其他表项保留原始验证值。

(recorded-result-06-tunnels-vxlan-evpn)=
### 运行查询实测节选

r4 动态 VXLAN 的实际地址族会话。会话已建立并收到前缀，还应继续核对 EVPN 路由和对应 VNI。

```text
<VortexROS> display bgp evpn peer
BGP local router ID : 10.255.0.1
 Local AS number : 65000
 Total number of peers : 1                 Peers in established state : 1

  Peer            V          AS  MsgRcvd  MsgSent  OutQ  Up/Down       State       PrefRcv
  10.255.0.3      4       65000        6        8     0  00:00:04      Established       2
```

同一拓扑的 Type-3 实测回显节选。应能看到远端 VTEP 作为下一跳。

```text
<VortexROS> display bgp evpn all routing-table inclusive-route
 Route Distinguisher: 65000:301
       Network                                                        NextHop
 *>i   0:32:10.255.0.3                                                10.255.0.3

 Route Distinguisher: 65000:302
       Network                                                        NextHop
 *>i   0:32:10.255.0.3                                                10.255.0.3

 Total Number of Inclusive Routes: 4
```

(section-operator-06-tunnels-vxlan-evpn-4)=
### 动态 VXLAN 隧道和实际 MAC 学习

r4 的同一拓扑中，从 10.255.0.1 到 10.255.0.3 的两条二层动态隧道均为 up。下方 MAC 表记录了 Ethernet6 在 BD 101 和 BD 102 中的本地学习结果。

```text
<VortexROS> display vxlan tunnel
Tunnel ID   Source                                    Destination                               State     Type
--------------------------------------------------------------------------------------------------------------------
20          10.255.0.1                                10.255.0.3                                up        L2 dynamic
21          10.255.0.1                                10.255.0.3                                up        L2 dynamic
--------------------------------------------------------------------------------------------------------------------
 Number of vxlan tunnel :
 Total: 2    Static: 0    L2 dynamic: 2    L3 dynamic: 0    Unmanaged: 0
```

```text
<VortexROS> display mac-address
-------------------------------------------------------------------------------
MAC Address       VLAN/VSI/BD                    Learned-From        Type
-------------------------------------------------------------------------------
ae5a-2c16-9902    -/-/101                        Ethernet6           dynamic
0200-0000-0102    -/-/102                        Ethernet6           dynamic
-------------------------------------------------------------------------------
Total items displayed = 2
```

`VLAN/VSI/BD` 中的 `-/-/101` 表示业务桥域 101。对单归属站点，`Learned-From` 对本地动态 MAC 显示接入口，对 EVPN 学到的远端动态 MAC 显示远端 VTEP 地址。可在[双 VTEP 案例](vxlan-evpn/cases/example-2.md)对照同一个桥域中的两种表项。

<span id="precautions"></span>

(section-operator-06-tunnels-vxlan-evpn-5)=
## 注意事项

RD 按设备区分，同一 VNI 的 RT 必须匹配。高位 BD 与普通 VLAN 独立，测试 MAC 迁移和重复地址时按实际 BD 查询。

<p data-legacy-id="id1" class="manual-previous-section" data-section-moved><a href="#overview">介绍</a></p>
<p data-legacy-id="id2" class="manual-previous-section" data-section-moved><a href="#principles">功能特性</a></p>
<p data-legacy-id="id3" class="manual-previous-section" data-section-moved><a href="#examples">配置案例</a></p>
<p data-legacy-id="id4" class="manual-previous-section" data-section-moved><a href="#case-verification-06-tunnels-vxlan-evpn">验证配置</a></p>
<p data-legacy-id="vtep-bd" class="manual-previous-section" data-section-moved><a href="cases/example-2/">两个 VTEP 的高位 BD 与动态学习</a></p>
<p data-legacy-id="mac-ip" class="manual-previous-section" data-section-moved><a href="cases/example-3/">高位域隔离、组播订阅与 MAC/IP 迁移</a></p>
