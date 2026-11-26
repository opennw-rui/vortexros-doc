---
nav_title: BGP 与 MP-BGP
nav_overview: 介绍
nav_feature: true
---


(section-operator-05-dynamic-routing-bgp-1)=
# BGP 与 MP-BGP

<span id="overview"></span>

BGP 用于 AS 间和 AS 内的路由交换。按地址族激活邻居，可处理 IPv4、IPv6 和 VPN 路由。

<span id="principles"></span>

(section-operator-05-dynamic-routing-bgp-2)=
## 工作原理

BGP 建立 TCP 会话后，按已协商的地址族交换路由。会话 Established 只表示对等连接就绪，导入导出策略、下一跳可达性和最优路径选择决定哪些前缀会进入转发表。分别核对邻居、已收到的前缀和转发。

BGP 按地址族建立路由交换，支持邻居组、策略和受支持的 VPN 地址族。

<span id="examples"></span>

(section-operator-05-dynamic-routing-bgp-3)=
## 配置与验证

(case-conditions-05-dynamic-routing-bgp)=
### 配置条件

确保邻居地址可达，规划两端 AS、Router ID 以及要交换的前缀。部署应用策略前检查现有会话。

全系统只允许一个主BGP AS。再次输入相同AS会进入现有视图；输入不同AS会报错且不会修改配置。AS 65535不可使用。

```{toctree}
:maxdepth: 1

bgp/cases/example-1
bgp/cases/example-2
bgp/cases/example-3
bgp/cases/example-4
```

(case-verification-05-dynamic-routing-bgp)=
### 通用验证

```vortexros-cli
display bgp peer
display ip routing-table protocol bgp
display ipv6 routing-table
```

确认需要的地址族邻居处于 Established，核对接收路由、下一跳及实际转发。

(section-operator-05-dynamic-routing-bgp-4)=
### 验证与撤销

```vortexros-cli
display bgp peer
display bgp routing-table
display bgp routing-table peer 10.0.0.2 received-routes
display bgp vpnv4 vpn-instance BLUE routing-table
display bgp tcp-protection verbose
```

默认TCP保护只接受已经配置的BGP邻居源地址。需要关闭时：

```text
bgp 64512
 undo default tcp-protected
```

精确删除邻居或单项参数：

```text
bgp 64512
 undo peer 10.0.0.2 route-policy RP-IN import
 undo peer 10.0.0.2 description
 undo peer 10.0.0.2
undo bgp 64512
commit
```

<span id="observed"></span>

(recorded-result-05-dynamic-routing-bgp)=
### 运行查询实测节选

IPv4 BGP 会话实测。先看 Established 和已收前缀数；前缀进入路由表后还需验证下一跳与业务报文。

```text
<VortexROS> display bgp peer
BGP local router ID : 2.2.2.2
 Local AS number : 65000
 Total number of peers : 2                 Peers in established state : 2

  Peer            V          AS  MsgRcvd  MsgSent  OutQ  Up/Down       State       PrefRcv
  10.201.12.1     4       65000        6       16     0  00:00:05      Established       1
  10.201.23.3     4       65000        7       12     0  00:00:03      Established       4
```

<span id="precautions"></span>

(section-operator-05-dynamic-routing-bgp-5)=
## 注意事项

会话已建立只表示 TCP/BGP 正常。还需检查指定地址族的前缀、策略效果和实际路径。共享密钥按设备保存。

(section-operator-05-dynamic-routing-bgp-6)=
### 验证与撤销

```vortexros-cli
display bgp peer
display bgp routing-table
display bgp routing-table peer 10.0.0.2 received-routes
display bgp vpnv4 vpn-instance BLUE routing-table
display bgp tcp-protection verbose
```

默认TCP保护只接受已经配置的BGP邻居源地址。需要关闭时：

```text
bgp 64512
 undo default tcp-protected
```

精确删除邻居或单项参数：

```text
bgp 64512
 undo peer 10.0.0.2 route-policy RP-IN import
 undo peer 10.0.0.2 description
 undo peer 10.0.0.2
undo bgp 64512
commit
```

<p data-legacy-id="id1" class="manual-previous-section" data-section-moved><a href="#overview">介绍</a></p>
<p data-legacy-id="id2" class="manual-previous-section" data-section-moved><a href="#case-conditions-05-dynamic-routing-bgp">配置准备</a></p>
<p data-legacy-id="id3" class="manual-previous-section" data-section-moved><a href="#examples">配置案例</a></p>
<p data-legacy-id="id5" class="manual-previous-section" data-section-moved><a href="#case-verification-05-dynamic-routing-bgp">验证配置</a></p>
<p data-legacy-id="id4" class="manual-previous-section" data-section-moved><a href="#precautions">验证与撤销</a></p>
<p data-legacy-id="ipv4" class="manual-previous-section" data-section-moved><a href="cases/example-1/">建立IPv4邻居</a></p>
<p data-legacy-id="tcp-md5" class="manual-previous-section" data-section-moved><a href="cases/example-2/">邻居组与TCP MD5认证</a></p>
<p data-legacy-id="vpnipv6" class="manual-previous-section" data-section-moved><a href="cases/example-3/">VPN与IPv6地址族</a></p>
<p data-legacy-id="ebgp" class="manual-previous-section" data-section-moved><a href="cases/example-4/">直连 eBGP 双向发布环回地址</a></p>
