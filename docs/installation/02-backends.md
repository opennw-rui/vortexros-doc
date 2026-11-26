# 系统与数据面组件

开发镜像自带 Linux、FRR、VPP、Kea、Chrony 和 OpenSSH。FRR 承载动态路由协议，Linux 管理系统的标准网络视图。启用 DPDK 接管时，VPP 负责已接管接口的转发。

| 组件 | 常用检查 |
| --- | --- |
| 整机软件与内核 | `display version`、`display startup` |
| Linux 或 DPDK 端口归属 | `display dataplane interfaces topological` |
| 控制面和后端服务 | `display service`、`display health` |
| 路由和转发 | `display ip routing-table`、`display ipv6 routing-table` |
| 管理和时钟 | `display users`、`display ntp-service status` |

操作系统、配套服务与受管配置由签名整机镜像统一更新。开发版的具体内核和软件版本以设备和对应制品的记录为准。
