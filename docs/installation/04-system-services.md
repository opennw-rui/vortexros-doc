---
nav_title: 系统服务与状态
nav_overview: 介绍
nav_feature: true
---


# 系统服务与状态

<span id="overview"></span>

启动完成后，通过设备 CLI 核对服务、日志和监听端口。

<span id="principles"></span>

## 工作原理

CLI 提供服务、健康状态与日志查询，可查看网络端口、时钟和管理状态。

<span id="examples"></span>

## 配置与验证

### 操作流程

![已启动设备 → CLI 查询服务 → 管理端点验证](04-system-services/cases.svg)

(case-conditions-installation-04-system-services)=
### 配置条件

系统已启动，使用具备相应查询权限的 CLI 账户。

### 配置步骤

启动完成后，通过设备 CLI 核对服务、日志和监听端口。

```text
<VortexROS> display service
<VortexROS> display health
<VortexROS> display logbuffer
<VortexROS> display process listen
```

OpenSSH 负责受管登录，设备本地 AAA 决定访问权限。FRR 和数据面服务由系统按启动依赖编排。NTP 使用配置中的时间源，日志中心可显示接口和协议状态变化。

配置修改经 Candidate 提交并保存。使用整机镜像入口维护受管系统软件。时区、DNS、NTP、SSH 和日志的配置见[系统与访问管理](../operator/02-system-services.md)。

(case-verification-installation-04-system-services)=
### 验证方法

对照以下命令和预期结果核对设备状态。

```vortexros-cli
display service
display health
display process listen
```

所需服务应在运行。检查实际监听地址和端口，再从另一台管理设备发起相应连接。

<span id="observed"></span>

(result-installation-04-system-services)=
### TCP 监听查询的实测回显

r5 的 TCP 监听检查中，sshd 在 [::]:22 监听，路由服务的控制端口可见于本地环回地址。实测节选如下。

```text
<VortexROS> display process tcp listen
Proto  State   Recv-Q  Send-Q  Local Address   Peer Address  Process
tcp    LISTEN  0       3       127.0.0.1:2608  0.0.0.0:*     isisd(372)
tcp    LISTEN  0       128     [::]:22         [::]:*        sshd(536)
```

<span id="precautions"></span>

## 注意事项

先确认运行版本和服务依赖。升级按整机签名流程操作。
