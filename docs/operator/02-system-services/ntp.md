---
nav_title: NTP 时间同步
nav_overview: 介绍
nav_feature: true
---


(section-operator-02-system-services-ntp-1)=
# NTP 时间同步

<span id="overview"></span>

NTP 使设备向指定时间源同步时钟。可使用 IPv4、IPv6 及独立的管理 VPN。

<span id="principles"></span>

(section-operator-02-system-services-ntp-2)=
## 工作原理

NTP 通过多个时间戳估算本机与服务端之间的偏移和延迟，再选择可用来源处理系统时间。同一个地址位于不同 VPN 时，应按指定 VPN 独立核对可达性。配置了来源还需确认它已被选中。

支持 IPv4 和 IPv6 单播客户端及按 VPN 选择时间源。同一个源地址可在多个 VPN 中分别配置。

<span id="examples"></span>

(section-operator-02-system-services-ntp-3)=
## 配置与验证

(case-conditions-02-system-services-ntp)=
### 配置条件

确认时间源可达。使用 vpn-instance 前先创建相应的 VPN 并准备到服务器的路由。

```{toctree}
:maxdepth: 1

ntp/cases/example-1
ntp/cases/example-2
```

(case-verification-02-system-services-ntp)=
### 通用验证

```vortexros-cli
display ntp-service status
display ntp-service sessions
```

等待设备选源，核对同步状态、服务器地址、所属 VPN 和可达性。

<span id="observed"></span>

(recorded-result-02-system-services-ntp)=
### 时钟源会话的实测回显

测试设备从默认路由表联系时间源 198.18.81.2。`*` 表示当前选用的时间源，`Reach` 用于观察最近的可达情况。

```text
<VortexROS> display ntp-service sessions
Clock source  VPN-Instance  State  Stratum  Poll  Reach
198.18.81.2   default       *      2        6     17
```

(query-result-02-system-services-ntp)=
### 命令回显实测节选

r5 在默认路由表和两个命名 VPN 实例测试 NTP。下列两个实例中的 192.0.2.1 地址相同，必须同时核对 VPN-Instance。星号标出当前选用的时间源。

```text
<VortexROS> display ntp-service sessions
Clock source    VPN-Instance  State  Stratum  Poll  Reach
198.51.100.1    default       -      2        6     17
192.0.2.1       qa-blue       *      2        6     17
192.0.2.1       qa-red        -      2        6     7
2001:db8:12::1  qa-blue       -      2        6     7
```

<span id="precautions"></span>

(section-operator-02-system-services-ntp-4)=
## 注意事项

确认 UDP 123 的回程经过相同 VPN。禁用同步保留已配置时间源，撤销单个源需匹配其地址和 VPN。

<p data-legacy-id="id1" class="manual-previous-section" data-section-moved><a href="#overview">介绍</a></p>
<p data-legacy-id="id2" class="manual-previous-section" data-section-moved><a href="#case-conditions-02-system-services-ntp">配置准备</a></p>
<p data-legacy-id="id3" class="manual-previous-section" data-section-moved><a href="#examples">配置案例</a></p>
<p data-legacy-id="id4" class="manual-previous-section" data-section-moved><a href="#case-verification-02-system-services-ntp">验证配置</a></p>
<p data-legacy-id="vpn" class="manual-previous-section" data-section-moved><a href="cases/example-2/">在不同 VPN 使用相同时间源地址</a></p>
