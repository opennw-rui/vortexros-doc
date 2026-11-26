---
nav_title: WireGuard 隧道
nav_overview: 介绍
nav_feature: true
---


(section-operator-06-tunnels-wireguard-1)=
# WireGuard 隧道

<span id="overview"></span>

WireGuard 用于在站点或终端之间建立加密三层连接。可按对端指定公钥、网络前缀和远端地址。

<span id="principles"></span>

(section-operator-06-tunnels-wireguard-2)=
## 工作原理

公钥标识对端，Allowed IPs 约束哪些内层地址允许与该对端关联。外层端点和底层路由负责送达加密 UDP。最近握手、有效内层地址和实际转发需要分别确认。

隧道用本机私钥标识自己，按对端公钥分别建立会话。目的地址属于多个允许前缀时，使用最长的匹配前缀选择 peer。显式配置外层源地址时，该地址须属于指定的底层路由表。

PHY up 要求 profile 和密钥就绪且隧道已启用，Protocol up 还需要有效的内层地址。检查单个 peer 是否已经握手时，查看其握手时间及收发计数。

<span id="examples"></span>

(section-operator-06-tunnels-wireguard-3)=
## 配置与验证

(case-conditions-06-tunnels-wireguard)=
### 配置条件

交换公钥，规划内层地址、外层路由及监听 UDP 端口。准备每端独立生成的私钥。

交换两端公钥，规划底层 VPN、业务前缀及 UDP 端口。配置备份可能含有密钥，按凭据保护。

```{toctree}
:maxdepth: 1

wireguard/cases/example-1
wireguard/cases/example-2
```

(case-verification-06-tunnels-wireguard)=
### 通用验证

```vortexros-cli
display wireguard interface
display interface Tunnel 10
display ip routing-table
```

确认对端握手、收发计数和业务路径。分别验证隧道地址与远端业务网段。

<span id="observed"></span>

(recorded-result-06-tunnels-wireguard)=
### 底层选路和 MTU 的实测结果

分别使用默认和命名底层 VPN 实例 UPLINK，隧道内层业务使用独立的 PERF 实例。两条 WireGuard 隧道在数据面重启前后双向探测均收到 3/3 回应。使用 1320 字节的隧道 MTU，恰好满足 MTU 的禁止分片探测通过，再大 1 字节时返回 Message too long。

<span id="precautions"></span>

(section-operator-06-tunnels-wireguard-4)=
## 注意事项

仅交换公钥。若响应侧没有固定的 peer 目的地址，应配置固定监听端口。自动源的路径变化后复查握手时间。

<p data-legacy-id="id1" class="manual-previous-section" data-section-moved><a href="#overview">介绍</a></p>
<p data-legacy-id="id2" class="manual-previous-section" data-section-moved><a href="#principles">功能特性</a></p>
<p data-legacy-id="id3" class="manual-previous-section" data-section-moved><a href="#examples">配置案例</a></p>
<p data-legacy-id="id6" class="manual-previous-section" data-section-moved><a href="#case-verification-06-tunnels-wireguard">验证配置</a></p>
<p data-legacy-id="id4" class="manual-previous-section" data-section-moved><a href="cases/example-1/">使用固定对端和业务前缀</a></p>
<p data-legacy-id="id5" class="manual-previous-section" data-section-moved><a href="cases/example-2/">主动连接端与漫游应答端</a></p>
