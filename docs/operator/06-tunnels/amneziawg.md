---
nav_title: AmneziaWG 隧道
nav_overview: 介绍
nav_feature: true
---


(section-operator-06-tunnels-amneziawg-1)=
# AmneziaWG 隧道

<span id="overview"></span>

AmneziaWG 为站点间提供加密隧道及可配置的握手与报文格式。可以与 WireGuard 并行配置。

<span id="principles"></span>

(section-operator-06-tunnels-amneziawg-2)=
## 工作原理

本地配置的混淆参数与所用对端必须兼容。外层 UDP 可达性、对端握手和内层路由各有独立状态。升级或冷启动后先核对外层回程，再确认握手和内层数据。

每个 peer 独立握手。PHY up 要求 profile、密钥和外层源地址条件满足且隧道运行，Protocol up 还需要合法的内层地址。单个 peer 的握手状态通过 peer 查询核对。

<span id="examples"></span>

(section-operator-06-tunnels-amneziawg-3)=
## 配置与验证

(case-conditions-06-tunnels-amneziawg)=
### 配置条件

为两端准备独立密钥、可达的外层路径及相同的协议参数。外层 UDP 监听端口应符合部署规划。

两端使用一致的协议参数，交换公钥，确认 VPN 路由和 UDP 端口可达。使用独立设备密钥。

```{toctree}
:maxdepth: 1

amneziawg/cases/example-1
amneziawg/cases/example-2
```

(case-verification-06-tunnels-amneziawg)=
### 通用验证

```vortexros-cli
display amneziawg interface Tunnel 20
display amneziawg peer AWG-PROFILE SITE-B
display interface Tunnel 20
```

检查对端握手后收发计数是否增加，从两端测试隧道地址和业务前缀。维护后要复查底层出口及隧道状态。

<span id="observed"></span>

(recorded-result-06-tunnels-amneziawg)=
### 重启、底层恢复和 MTU 的实测结果

默认和命名底层 VPN 实例各建立一条隧道，内层流量在 PERF 实例中转发。两条隧道在数据面重启前后双向探测均收到 3/3 回应。适配 1320 字节 MTU 的禁止分片探测通过，再大 1 字节返回 Message too long。保存配置后，升级试启动、再次冷启动及恢复底层默认路由均验证了恢复。

<span id="precautions"></span>

(section-operator-06-tunnels-amneziawg-4)=
## 注意事项

两端须匹配握手参数和填充配置。更换公钥、协议参数或外层路由后，用新握手和双向业务确认。配置备份按凭据保管。

<p data-legacy-id="id1" class="manual-previous-section" data-section-moved><a href="#overview">介绍</a></p>
<p data-legacy-id="id2" class="manual-previous-section" data-section-moved><a href="#principles">功能特性</a></p>
<p data-legacy-id="id3" class="manual-previous-section" data-section-moved><a href="#examples">配置案例</a></p>
<p data-legacy-id="id6" class="manual-previous-section" data-section-moved><a href="#case-verification-06-tunnels-amneziawg">验证配置</a></p>
<p data-legacy-id="id4" class="manual-previous-section" data-section-moved><a href="cases/example-1/">使用指定握手参数的对端</a></p>
<p data-legacy-id="id5" class="manual-previous-section" data-section-moved><a href="cases/example-2/">主动连接端与漫游应答端</a></p>
