---
nav_title: 配置案例
---


# 系统与数据面组件 配置案例

## 操作流程

![物理网口 → Linux 或 DPDK 模式 → 业务与受管服务](cases.svg)

(case-conditions-installation-02-backends)=
## 配置条件

设备已完成安装、启动，并使用实际计划的接口模式。

## 配置步骤

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
## 验证方法

对照以下命令和预期结果核对设备状态。

```vortexros-cli
display dataplane interfaces topological
display health
display ip routing-table
```

各数据面接口应显示预期的活动模式，服务状态应反映当前运行情况。确认去往测试目的地址的路由和下一跳后，再从隔离对端验证转发。
