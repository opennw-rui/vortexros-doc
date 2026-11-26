---
nav_title: IPv4 与 IPv6 静态路由
nav_overview: 介绍
nav_feature: true
---


(section-operator-04-ip-routing-static-routes-1)=
# IPv4 与 IPv6 静态路由

<span id="overview"></span>

静态路由把指定目的前缀交给固定的下一跳或出接口，适用于默认出口、固定对端或备用路径。

<span id="principles"></span>

(section-operator-04-ip-routing-static-routes-2)=
## 工作原理

配置的目的前缀和下一跳必须能在对应路由表解析。存在重叠前缀时，转发优先使用最长匹配。对同一目的前缀选择候选路由时才比较 preference 等属性。核对表中的前缀、出接口和下一跳，并从两个方向验证。可对照[华为 IP 路由选路原理](https://info.support.huawei.com/info-finder/encyclopedia/en/detail?action=queryEntityDetail&keyword=IP+routing)。

可为目的前缀指定固定下一跳或出接口，支持 IPv4、IPv6 与 VPN。路由表和转发表可分别查询。

<span id="examples"></span>

(section-operator-04-ip-routing-static-routes-3)=
## 配置与验证

(case-conditions-04-ip-routing-static-routes)=
### 配置条件

确认下一跳在正确的路由表内可达。使用跨 VPN 下一跳时先创建相应 VPN。

```{toctree}
:maxdepth: 1

static-routes/cases/example-1
static-routes/cases/example-2
```

(case-verification-04-ip-routing-static-routes)=
### 通用验证

```vortexros-cli
display ip routing-table protocol static
display ip routing-table vpn-instance BLUE
display ipv6 routing-table protocol static
display ip fib
display ipv6 fib
```

检查优选路由的目的前缀、下一跳和出接口。DPDK 数据面还可查看 FIB。存在多条等价路径时，核对每条有效路径并验证实际转发。

<span id="observed"></span>

(recorded-result-04-ip-routing-static-routes)=
### 运行查询实测节选

r4 三节点路由拓扑中的实际 IPv4 回显。目的前缀在默认表为 Active，Flags 含 `D`，出接口、下一跳与配置一致。

```text
<VortexROS> display ip routing-table protocol static
Route Flags: R - relay, D - download to fib, T - nexthop VPN instance, B - black hole route
-----------------------------------------------------------------------------------------------
Routing Table : default
         Destinations : 1        Routes : 1        Configured Routes : 1

Static routing table status : <Active>
         Destinations : 1        Routes : 1

Destination/Mask   Proto   Pre  Cost    Flags  NextHop          Interface       VPN-Instance

  10.201.23.0/24   Static  60   0         D    10.201.12.2      host-p1e12      default
```

<span id="precautions"></span>

(section-operator-04-ip-routing-static-routes-4)=
## 注意事项

提交前核对下一跳在正确实例内可达。在冗余路径中要同时测试去程和回程。

<p data-legacy-id="id1" class="manual-previous-section" data-section-moved><a href="#overview">介绍</a></p>
<p data-legacy-id="id2" class="manual-previous-section" data-section-moved><a href="#case-conditions-04-ip-routing-static-routes">配置准备</a></p>
<p data-legacy-id="id3" class="manual-previous-section" data-section-moved><a href="#examples">配置案例</a></p>
<p data-legacy-id="id5" class="manual-previous-section" data-section-moved><a href="#case-verification-04-ip-routing-static-routes">验证配置</a></p>
<p data-legacy-id="id4" class="manual-previous-section" data-section-moved><a href="cases/example-2/">双栈主机路由与回程</a></p>
