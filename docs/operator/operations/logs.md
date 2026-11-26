---
nav_title: 日志中心
nav_overview: 介绍
nav_feature: true
---


(section-operator-operations-logs-1)=
# 日志中心

<span id="overview"></span>

日志中心用于查看接口、Vlanif、Vbdif、动态路由邻居、BFD 和 VRRP 的状态变化，也可按服务查询设备日志。Console 默认接收实时日志，SSH 默认关闭。

<span id="principles"></span>

(section-operator-operations-logs-2)=
## 工作原理

可按服务和记录数查询历史。实时监视可按终端控制，也可由设备配置启停。

<span id="examples"></span>

(section-operator-operations-logs-3)=
## 配置与验证

(case-conditions-operations-logs)=
### 配置条件

先确定是临时调整当前终端，还是调整所有终端。查询历史记录可使用下面的 display 命令。

```{toctree}
:maxdepth: 1

logs/cases/example-1
logs/cases/example-2
```

(case-verification-operations-logs)=
### 通用验证

```vortexros-cli
display logbuffer
display logbuffer service frr last 30
display logbuffer last 20 since 15
display alarm active
```

核对事件涉及的接口或邻居、状态及本地时间。跨日期或跨启动周期时，在获准的系统维护环境查看带日期的 journal。

<span id="observed"></span>

(recorded-result-operations-logs)=
### 安装和启动日志的实测回显

Live 环境中的安装器是按终端实例启动的，`instance` 用于定位实际终端。下面为 r4 串口 Live 与已安装系统的两次查询。时间戳使用设备配置的时区。

```text
<VortexROS> display logbuffer service installer last 10
18:27:07.868+00:00 INFO installer SERVICE_MESSAGE instance="ttyS0" -- Starting vortexros-install@ttyS0.service - VortexROS Live installer...
18:27:07.941+00:00 INFO installer SERVICE_MESSAGE instance="ttyS0" -- Started vortexros-install@ttyS0.service - VortexROS Live installer.
```

```text
<VortexROS> display logbuffer service image
18:36:04.944+00:00 INFO image/confirm SERVICE_MESSAGE -- Confirmed image 0.1.0-dev-amd64-resource-recovery-r4
```

<span id="precautions"></span>

(section-operator-operations-logs-4)=
## 注意事项

终端时间随系统时区。查跨日或跨重启的事件时，按完整时间与启动记录关联。

<p data-legacy-id="id2" class="manual-previous-section" data-section-moved><a href="#overview">介绍</a></p>
<p data-legacy-id="id3" class="manual-previous-section" data-section-moved><a href="#case-conditions-operations-logs">配置准备</a></p>
<p data-legacy-id="id4" class="manual-previous-section" data-section-moved><a href="#examples">配置案例</a></p>
<p data-legacy-id="id6" class="manual-previous-section" data-section-moved><a href="#case-verification-operations-logs">验证配置</a></p>
<p data-legacy-id="id5" class="manual-previous-section" data-section-moved><a href="cases/example-2/">用接口变更核对日志与告警</a></p>
