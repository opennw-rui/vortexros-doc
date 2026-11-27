---
nav_title: IPv6 路径 MTU
nav_overview: 介绍
nav_feature: true
---


(section-operator-04-ip-routing-ipv6-path-mtu-1)=
# IPv6 路径 MTU

<span id="overview"></span>

IPv6 路径 MTU 表示到目的地址的路径可传输的最大 IP 报文长度。小报文可达、大报文失败时，可结合此查询排查路径限制。

<span id="principles"></span>

(section-operator-04-ip-routing-ipv6-path-mtu-2)=
## 工作原理

IPv6 转发节点遇到报文大于出口 MTU 时通过 Packet Too Big 通知发送端。线路可以转发小包、却对大流量出现异常。用已知长度的探测分别检查小包和实际业务所需的包长。

按默认表或 VPN 查询已学习的目的 IPv6 路径 MTU。

<span id="examples"></span>

(section-operator-04-ip-routing-ipv6-path-mtu-3)=
## 配置与验证

(section-operator-04-ip-routing-ipv6-path-mtu-4)=
### 拓扑

![R1、R2、目的主机 的设备互联](ipv6-path-mtu/cases.svg)

(case-conditions-04-ip-routing-ipv6-path-mtu)=
### 配置条件

确定目的地址和所属 VPN。路径 MTU 表来自运行中学习到的信息。先经过实际业务路径发送 IPv6 流量，再查看相关项。

(section-operator-04-ip-routing-ipv6-path-mtu-5)=
### 配置步骤

```vortexros-cli
display ipv6 pathmtu
display ipv6 pathmtu vpn-instance BLUE
display ipv6 routing-table vpn-instance BLUE
```

第一条查看默认实例，后两条查看 BLUE 中的路径信息和路由。将 BLUE 换成实际实例名。

(case-verification-04-ip-routing-ipv6-path-mtu)=
### 验证方法

对照以下命令和预期结果核对设备状态。

```vortexros-cli
display ipv6 pathmtu vpn-instance BLUE
display ipv6 routing-table vpn-instance BLUE
```

对照目标地址和 MTU，核对出接口及隧道封装。存在活动路径 MTU 项时，其目的应与测试流量一致。没有学习到条目时，可从两端测试不同长度的 IPv6 报文，并检查网络是否传递 ICMPv6 Packet Too Big 消息。

<span id="observed"></span>

(lab-result-operator-04-ip-routing-ipv6-path-mtu)=
### 路径 MTU 缓存为空时的回显

在 r4 的测试实例中，查询时尚无会话触发路径 MTU 缓存，设备仅显示列名。应在实际收到 IPv6 Packet Too Big 并形成有效条目后，再按目的地址和 VPN 实例核对 Path MTU。

```text
<VortexROS> display ipv6 pathmtu
IPv6 Address  Path MTU  VPN-Instance  Table ID
```

<span id="precautions"></span>

(section-operator-04-ip-routing-ipv6-path-mtu-6)=
## 注意事项

结果来自运行流量。核对隧道封装，并验证路径允许 ICMPv6 Packet Too Big 返回。

<p data-legacy-id="id1" class="manual-previous-section" data-section-moved><a href="#overview">介绍</a></p>
<p data-legacy-id="id2" class="manual-previous-section" data-section-moved><a href="#case-conditions-04-ip-routing-ipv6-path-mtu">查询准备</a></p>
<p data-legacy-id="id3" class="manual-previous-section" data-section-moved><a href="#examples">配置案例</a></p>
<p data-legacy-id="id4" class="manual-previous-section" data-section-moved><a href="#case-verification-04-ip-routing-ipv6-path-mtu">验证结果</a></p>
