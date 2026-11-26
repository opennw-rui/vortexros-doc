---
nav_title: 系统与数据面组件
nav_overview: 介绍
nav_feature: true
---


# 系统与数据面组件

<span id="overview"></span>

开发镜像自带 Linux、FRR、VPP、Kea、Chrony 和 OpenSSH。FRR 承载动态路由协议，Linux 管理系统的标准网络视图。启用 DPDK 接管时，VPP 负责已接管接口的转发。

<span id="principles"></span>

## 工作原理

Linux、DPDK 和所管理的系统服务可通过设备状态命令查询。

<span id="examples"></span>

## 配置与验证

### 操作流程

![物理网口 → Linux 或 DPDK 模式 → 业务与受管服务](02-backends/cases.svg)

(case-conditions-installation-02-backends)=
### 配置条件

设备已完成安装、启动，并使用实际计划的接口模式。

### 配置步骤

开发镜像自带 Linux、FRR、VPP、Kea、Chrony 和 OpenSSH。FRR 承载动态路由协议，Linux 管理系统的标准网络视图。启用 DPDK 接管时，VPP 负责已接管接口的转发。

| 组件 | 常用检查 |
| --- | --- |
| 整机软件与内核 | `display version`、`display startup` |
| Linux 或 DPDK 端口归属 | `display dataplane interfaces topological` |
| 控制面和后端服务 | `display service`、`display health` |
| 路由和转发 | `display ip routing-table`、`display ipv6 routing-table` |
| 管理和时钟 | `display users`、`display ntp-service status` |

操作系统、配套服务与受管配置由签名整机镜像统一更新。开发版的具体内核和软件版本以设备和对应制品的记录为准。

(case-verification-installation-02-backends)=
### 验证方法

对照以下命令和预期结果核对设备状态。

```vortexros-cli
display dataplane interfaces topological
display health
display ip routing-table
```

各数据面接口应显示预期的活动模式，服务状态应反映当前运行情况。确认去往测试目的地址的路由和下一跳后，再从隔离对端验证转发。

<span id="observed"></span>

(closeout-result-installation-02-backends)=
### Linux 数据面的实测回显

r4 在未启用 DPDK 的虚拟机中，接口由 Linux 持有。数据面归属以 Interface dataplane owner 字段为准。DPDK 装机的对应读回见 {ref}`安装结果 <case-verification-installation-03-install-vortexros>`。

```text
<VortexROS> display health
Health state              : ready
Interface dataplane owner : linux
Takeover phase            : ready
Active alarms             : 0
```

<span id="precautions"></span>

## 注意事项

选择适合硬件的接口模式。功能状态与流量路径以实际运行查询及对端验证为准。
