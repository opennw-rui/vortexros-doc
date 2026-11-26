---
nav_title: 本机 DNS 解析
nav_overview: 介绍
nav_feature: true
---


(section-operator-02-system-services-dns-1)=
# 本机 DNS 解析

<span id="overview"></span>

动态 DNS 解析让设备通过主机名访问管理或网络服务。设备自身的 DNS 请求走默认路由表。

<span id="principles"></span>

(section-operator-02-system-services-dns-2)=
## 工作原理

本机解析服务负责把主机名交给所配置的 DNS 服务器查询。能 ping 到服务器只证明 IP 可达。用实际域名查询确认应答，同时核对超时与无记录的区别。

支持配置本机的 IPv4、IPv6 DNS 服务器和搜索域，DNS 查询从默认路由表发送。

<span id="examples"></span>

(section-operator-02-system-services-dns-3)=
## 配置与验证

(case-conditions-02-system-services-dns)=
### 配置条件

确认 DNS 服务器在默认路由表中可达。192.0.2.53 是示例地址。

```{toctree}
:maxdepth: 1

dns/cases/example-1
dns/cases/example-2
```

(case-verification-02-system-services-dns)=
### 通用验证

```vortexros-cli
display dns server
```

确认服务器列表显示配置地址，再用实际可解析的主机名测试。

<span id="observed"></span>

(recorded-result-02-system-services-dns)=
(result-operator-02-system-services-dns)=
### 默认表 DNS 的实测结果

两台设备分别通过 IPv4 DNS 服务器解析带搜索域的短名称，并通过 IPv6 DNS 服务器查询完整域名。保存配置并重启后复查，关闭 DNS 配置后验证变更生效。

(r4-result-operator-02-system-services-dns)=
### 尚未启用 DNS 的实测回显

r4 空盘启动时，解析状态为 disabled，服务器列表为空。完成启用及地址配置后，再核对状态、地址列表和实测域名解析。

```text
<VortexROS> display dns server
DNS resolution : disabled
No.   IP address
```

<span id="precautions"></span>

(section-operator-02-system-services-dns-4)=
## 注意事项

配置 DHCP 地址池的 DNS 选项只影响客户端。本机解析失败时，先验证默认路由表能到达 DNS 服务器。

<p data-legacy-id="id1" class="manual-previous-section" data-section-moved><a href="#overview">介绍</a></p>
<p data-legacy-id="id2" class="manual-previous-section" data-section-moved><a href="#case-conditions-02-system-services-dns">配置准备</a></p>
<p data-legacy-id="id3" class="manual-previous-section" data-section-moved><a href="#examples">配置案例</a></p>
<p data-legacy-id="id5" class="manual-previous-section" data-section-moved><a href="#case-verification-02-system-services-dns">验证配置</a></p>
<p data-legacy-id="id4" class="manual-previous-section" data-section-moved><a href="cases/example-2/">使用管理域名及搜索后缀</a></p>
