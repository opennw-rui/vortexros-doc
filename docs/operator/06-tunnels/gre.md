---
nav_title: GRE Tunnel
nav_overview: 介绍
nav_feature: true
---


(section-operator-06-tunnels-gre-1)=
# GRE Tunnel

<span id="overview"></span>

GRE 用于在可达的三层网络上承载另一条三层逻辑链路。隧道本身不提供加密。

<span id="principles"></span>

(section-operator-06-tunnels-gre-2)=
## 工作原理

用 `display interface Tunnel 1` 或 `display interface brief` 查看状态。PHY 反映隧道自身和底层路径是否就绪，Protocol 还取决于隧道接口的三层地址。

| 状态 | 判定条件 |
| --- | --- |
| PHY up | GRE 协议和两端外层地址已配置，运行中的隧道已启用，源地址属于所选底层路由表，目的地址在同一表中有可用转发路径。 |
| Protocol up | PHY 已 up，且 Tunnel 接口具备有效的内层 IP 地址。没有内层地址时，PHY 可以是 up，Protocol 显示 down。 |
| `^down` | 协议或外层端点配置不完整，隧道等待创建。 |
| `down` | 配置已完整，但运行接口、源地址或底层路径尚未就绪。 |
| `*down` | 已通过 `shutdown` 管理关闭。 |

GRE 的 up 反映本端条件。两端配置是否一致、业务是否可用，以隧道内的双向流量为准。

<span id="examples"></span>

(section-operator-06-tunnels-gre-3)=
## 配置与验证

(case-conditions-06-tunnels-gre)=
### 配置条件

准备两台三层设备。各端的本机外层地址必须存在，且能在选定底层路由表中到达对端地址。规划独立的隧道内层网段。

```{toctree}
:maxdepth: 1

gre/cases/default-routing-table
gre/cases/vpn-underlay
```

(case-verification-06-tunnels-gre)=

<span id="observed"></span>

(recorded-result-06-tunnels-gre)=
### 运行查询实测节选

r4 三节点的实际 GRE 回显节选。此拓扑使用 Tunnel0 与 192.0.2.0/30，标记出的上下状态、内层地址和外层端点可与本页各案例对照。

```text
<VortexROS> display interface Tunnel 0
Tunnel0 current state : UP
Line protocol current state : UP
Internet Address is 192.0.2.1/30
Physical is GRE tunnel
Tunnel protocol: gre
Source: 10.201.12.1
Destination: 10.201.23.3
```

同一测试的直连路由确认内层网段关联到 Tunnel0。

```text
<VortexROS> display ip routing-table protocol direct
Routing Table : default
Destination/Mask   Proto   Pre  Cost    Flags  NextHop          Interface       VPN-Instance
    192.0.2.0/30   Direct  0    0         D    -                Tunnel0         default
```

<span id="precautions"></span>

(section-operator-06-tunnels-gre-4)=
## 注意事项

- 源地址和目的地址须使用同一底层路由表。底层 VPN 与 Tunnel 接口承载内层业务所用的 VPN 可分别选择。
- 两端的 GRE key 应一致。对称修改或撤销 key 后，用内层双向流量验证。
- 外层 IPv4 MTU 为 1500、使用 GRE key 且无其他额外封装时，内层 MTU 可设为 1472。实际路径 MTU 更小时应相应调小。
- 删除前先移除指向 Tunnel1 的静态路由和协议、策略引用。在系统视图执行 `undo interface Tunnel 1` 并提交，再检查接口及相关直连路由。

<p data-legacy-id="id1" class="manual-previous-section" data-section-moved><a href="#overview">介绍</a></p>
<p data-legacy-id="id2" class="manual-previous-section" data-section-moved><a href="#principles">功能特性</a></p>
<p data-legacy-id="id4" class="manual-previous-section" data-section-moved><a href="#precautions">注意事项</a></p>
<p data-legacy-id="id3" class="manual-previous-section" data-section-moved><a href="#examples">配置案例</a></p>
<p data-legacy-id="gre" class="manual-previous-section" data-section-moved><a href="cases/default-routing-table/">默认路由表中的双端 GRE</a></p>
<p data-legacy-id="vpn" class="manual-previous-section" data-section-moved><a href="cases/vpn-underlay/">使用 VPN 实例作为底层</a></p>
