# VortexROS 用户手册

本手册面向 VortexROS `v0.1.0-dev` 的设备管理员。按任务查找配置步骤及验证方法。

## 开始使用

- [从 Live ISO 安装](installation/03-install-vortexros.md)
- [首次启动与管理接入](installation/06-first-start.md)
- [提交与保存配置](operator/01-cli/configuration.md)

## 按功能查找

- [命令行与配置管理](operator/01-cli.md)
- [系统设置与远程管理](operator/02-system-services.md)
- [接口](operator/interfaces.md)
- [二层交换](operator/layer2-switching.md)
- [IP 接入](operator/ip-access.md)
- [静态路由](operator/static-routing.md)
- [动态路由](operator/05-dynamic-routing.md)
- [高可用与故障检测](operator/high-availability.md)
- [隧道与 Overlay 网络](operator/06-tunnels.md)，含 [EVPN](operator/06-tunnels/evpn.md)
- [访问控制列表](operator/topics/traffic-access.md)
- [QoS](operator/topics/traffic-qos.md)
- [NAT](operator/nat.md)
- [网络服务与管理协议](operator/08-network-services.md)
- [运行监控与故障处理](operator/09-operations.md)
- [MPLS](operator/10-mpls-l3vpn.md)
- [应用部署与网络](operator/11-applications.md)

## 日常维护

- [升级与回退](installation/07-upgrade-uninstall.md)
- [日志中心](operator/operations/logs.md)
- [脱敏支持包与加密备份](operator/09-operations/backup-support.md)
- [全命令参考](operator/reference/commands.md)

```{toctree}
:maxdepth: 3
:hidden:

installation/index
operator/01-cli
operator/02-system-services
operator/interfaces
operator/layer2-switching
operator/ip-access
operator/static-routing
operator/05-dynamic-routing
operator/high-availability
operator/06-tunnels
operator/topics/traffic-access
operator/topics/traffic-qos
operator/nat
operator/08-network-services
operator/09-operations
operator/10-mpls-l3vpn
operator/11-applications
operator/reference/commands
operator/index
```
