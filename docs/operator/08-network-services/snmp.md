---
nav_title: SNMP 监控
nav_overview: 介绍
nav_feature: true
---


(section-operator-08-network-services-snmp-1)=
# SNMP 监控

<span id="overview"></span>

SNMP 允许网管系统读取设备状态并接收通知。只读轮询支持 SNMPv2c，SNMPv3 支持 authPriv。

<span id="principles"></span>

(section-operator-08-network-services-snmp-2)=
## 工作原理

查询返回设备当前的管理对象，通知用于主动上报事件。固定源接口与 VPN 会影响接收请求和发送通知的路径。检查访问方式、采集端实际应答及接口计数。

SNMP 可用只读轮询查询设备信息，并支持通知。v3 支持 authPriv 和按管理实例绑定源接口。

<span id="examples"></span>

(section-operator-08-network-services-snmp-3)=
## 配置与验证

(case-conditions-08-network-services-snmp)=
### 配置条件

准备管理站和设备管理接口。下例使用 v2c 联调，请将 COMMUNITY 替换为设备专用的团体名。

```{toctree}
:maxdepth: 1

snmp/cases/example-1
snmp/cases/example-2
```

(case-verification-08-network-services-snmp)=
### 通用验证

```vortexros-cli
display snmp-agent sys-info
display snmp-agent community
display process udp listen
```

预期 UDP 161 监听在所配置的管理地址或接口。再从实际管理站发起只读查询，确认返回设备的 `sysName.0`。使用管理 VPN 时，从该 VPN 内的管理站验证请求和应答。配置通知时同时在接收端确认收到了对应事件。

<span id="observed"></span>

(recorded-result-08-network-services-snmp)=
### 实际 GET 查询和 AgentX 连接

在另一个接入网段使用 SNMPv2c 查询 sysName，实际返回如下。发送查询时使用自己配置的只读 community。连接记录可用 `display logbuffer service snmp` 查看。

```text
.1.3.6.1.2.1.1.5.0 = STRING: "VortexROS"
```

```text
<VortexROS> display logbuffer service snmp
02:08:45.772+08:00 INFO snmp/agentx SERVICE_MESSAGE -- NET-SNMP version 5.9.4.pre2 AgentX subagent connected
```

<span id="precautions"></span>

(section-operator-08-network-services-snmp-4)=
## 注意事项

将监听限制在所需管理接口，保护团体名及 v3 口令。应从真实网管终端核对请求和响应。

<p data-legacy-id="id1" class="manual-previous-section" data-section-moved><a href="#overview">介绍</a></p>
<p data-legacy-id="id2" class="manual-previous-section" data-section-moved><a href="#case-conditions-08-network-services-snmp">配置准备</a></p>
<p data-legacy-id="id3" class="manual-previous-section" data-section-moved><a href="#examples">配置案例</a></p>
<p data-legacy-id="id4" class="manual-previous-section" data-section-moved><a href="#case-verification-08-network-services-snmp">验证配置</a></p>
<p data-legacy-id="vpn-snmpv3" class="manual-previous-section" data-section-moved><a href="cases/example-2/">管理 VPN 内的 SNMPv3 轮询</a></p>
