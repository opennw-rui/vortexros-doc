---
nav_title: IPv6 路由通告与 SLAAC
nav_overview: 介绍
nav_feature: true
---


(section-operator-04-ip-routing-ipv6-router-advertisement-1)=
# IPv6 路由通告与 SLAAC

<span id="overview"></span>

主机可从 RA 学习 IPv6 前缀和默认路由。VortexROS 可在上联接收 RA，也可在下游三层接口发布 RA。

<span id="principles"></span>

(section-operator-04-ip-routing-ipv6-router-advertisement-2)=
## 工作原理

主机可从路由器通告获取默认路由和前缀。前缀用于 SLAAC 时，主机还要在链路上完成重复地址检测。拿到地址与得到默认路由是两个独立结果，验证时分别读取。

可在指定上联接收 RA 并获取 SLAAC 地址或默认路由，也可向下游通告前缀。

<span id="examples"></span>

(section-operator-04-ip-routing-ipv6-router-advertisement-3)=
## 配置与验证

(case-conditions-04-ip-routing-ipv6-router-advertisement)=
### 配置条件

确认上游在指定链路提供路由通告。独立使用 DHCPv6 时，仍需为默认路由准备 RA 或静态路由。

```{toctree}
:maxdepth: 1

ipv6-router-advertisement/cases/example-1
ipv6-router-advertisement/cases/example-2
```

(case-verification-04-ip-routing-ipv6-router-advertisement)=
### 通用验证

```vortexros-cli
display ipv6 interface brief
display ipv6 neighbors
display ipv6 routing-table
```

确认地址与通告前缀匹配，默认路由指向上游路由器的链路本地地址。撤销后检查对应自动学习的地址和路由已消失。

如果设备在发出 RA，从下游主机检查自动生成的 IPv6 地址和默认路由，并测试网关连通。

<span id="observed"></span>

实测节选中的物理接口按文档端口编号记为 EthernetX。其他表项保留原始验证值。

(recorded-result-04-ip-routing-ipv6-router-advertisement)=
(r4-ra-slaac-result)=
### RA、SLAAC 和缺省路由的实测回显

r4 三节点中，第一台从专用三层链路发布 `2001:db8:20::/64`。第二台在对端口自动获得同一前缀的地址，缺省路由从该口指向上游的 IPv6 链路本地地址。直接探测上游地址收到 3/3 回应。撤销自动配置后，自动地址和所学缺省路由均消失。以下保留实际回显中的相关行。

```text
<VortexROS> display ipv6 interface brief
Interface               IPv6 Address/Mask                      Physical  Protocol  VPN-Instance
Ethernet4               2001:db8:20:0:fe:b5ff:fe44:9b03/64     up        up        default
```

```text
<VortexROS> display ipv6 routing-table
Routing Table : default
Destination  : ::                                      PrefixLength : 0
NextHop      : fe80::fe:2cff:fe2d:b091                 Preference   : 0
Cost         : 1024                                    Protocol     : Kernel
RelayNextHop : fe80::fe:2cff:fe2d:b091                 Flags        : D
Interface    : Ethernet4                               VPN-Instance : default
```

<span id="precautions"></span>

(section-operator-04-ip-routing-ipv6-router-advertisement-4)=
## 注意事项

DHCPv6 的地址或前缀委派独立于 RA 默认路由。测试多类自动地址时，逐项核对来源及撤销效果。

<p data-legacy-id="id1" class="manual-previous-section" data-section-moved><a href="#overview">介绍</a></p>
<p data-legacy-id="id2" class="manual-previous-section" data-section-moved><a href="#case-conditions-04-ip-routing-ipv6-router-advertisement">配置准备</a></p>
<p data-legacy-id="id3" class="manual-previous-section" data-section-moved><a href="#examples">配置案例</a></p>
<p data-legacy-id="id4" class="manual-previous-section" data-section-moved><a href="#case-verification-04-ip-routing-ipv6-router-advertisement">验证配置</a></p>
<p data-legacy-id="ipv6" class="manual-previous-section" data-section-moved><a href="cases/example-2/">向下游发布 IPv6 前缀</a></p>
