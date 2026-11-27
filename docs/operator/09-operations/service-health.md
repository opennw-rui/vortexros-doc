---
nav_title: 服务状态与监听端口
nav_overview: 介绍
nav_feature: true
---


(section-operator-09-operations-service-health-1)=
# 服务状态与监听端口

<span id="overview"></span>

设备提供服务、健康状态和监听端口查询，可用来区分连通性问题与本地服务未启动。

<span id="principles"></span>

(section-operator-09-operations-service-health-2)=
## 工作原理

可查询运行服务、监听地址、TCP/UDP 端口和告警。

<span id="examples"></span>

(section-operator-09-operations-service-health-3)=
## 配置与验证

(section-operator-09-operations-service-health-4)=
### 拓扑

![管理终端、R1 的设备互联](service-health/cases.svg)

(case-conditions-09-operations-service-health)=
### 配置条件

确定希望排查的服务和协议。远程排查前保留当前会话。

(section-operator-09-operations-service-health-5)=
### 配置步骤

以 SSH 不通为例，先确认管理接口与路由，再核对 TCP 监听和 SSH 登录记录。服务状态异常时同时查看告警。

```vortexros-cli
display ip interface brief
display process tcp listen
display ssh user login-info failed
```

(case-verification-09-operations-service-health)=
### 验证方法

对照以下命令和预期结果核对设备状态。

```vortexros-cli
display service verbose
display health
display process listen
display process udp listen
display alarm active
```

核对协议、监听地址、端口和主进程。恢复后从远端新建连接，确认业务可用。

<span id="observed"></span>

(section-operator-09-operations-service-health-6)=
### 控制层与数据面就绪的实测回显

本例正常启动后，配置代次一致，VPP API 已连接，依赖项就绪。

```text
<VortexROS> display health
Health state              : ready
Running/Actual generation : 1/1
Reconcile state           : in-sync
VPP API state             : connected
Interface dataplane owner : vpp
Takeover phase            : complete
Active alarms             : 0
Foundation recovery       : ready
Routing recovery          : ready
Services recovery         : ready
```

<span id="precautions"></span>

(section-operator-09-operations-service-health-7)=
## 注意事项

监听正常后仍需从管理终端验证真实连接。维护时先核对操作影响和当前会话。

<p data-legacy-id="id2" class="manual-previous-section" data-section-moved><a href="#overview">介绍</a></p>
<p data-legacy-id="id3" class="manual-previous-section" data-section-moved><a href="#case-conditions-09-operations-service-health">配置准备</a></p>
<p data-legacy-id="id4" class="manual-previous-section" data-section-moved><a href="#examples">配置案例</a></p>
<p data-legacy-id="id5" class="manual-previous-section" data-section-moved><a href="#case-verification-09-operations-service-health">验证配置</a></p>
