# 配置指南

从业务大类进入功能页。EVPN、MPLS L3VPN 和 DHCP 等专题按用途继续细分。功能页集中提供工作原理、配置步骤、验证命令与注意事项。

- [命令行与配置管理](01-cli.md)
- [系统设置与远程管理](02-system-services.md)
- [接口](interfaces.md)
- [二层交换](layer2-switching.md)
- [IP 接入](ip-access.md)
- [静态路由](static-routing.md)
- [动态路由](05-dynamic-routing.md)
- [高可用与故障检测](high-availability.md)
- [隧道与 Overlay 网络](06-tunnels.md)，含 [EVPN](06-tunnels/evpn.md)
- [访问控制列表](topics/traffic-access.md)
- [QoS](topics/traffic-qos.md)
- [NAT](nat.md)
- [网络服务与管理协议](08-network-services.md)
- [运行监控与故障处理](09-operations.md)
- [MPLS](10-mpls-l3vpn.md)
- [应用部署与网络](11-applications.md)
- [全命令参考](reference/commands.md)

## 使用约定

- 配置片段使用缩进表示视图。交互输入时，先用 quit 返回上一级视图，再进入下一个同级视图。
- 执行 commit 后配置才生效。利用相应的 display 命令和实际业务验证，再执行 save。
- 示例地址、设备名、接口名与凭据占位符需要按实际网络替换。
