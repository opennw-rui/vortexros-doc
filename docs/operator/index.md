# 配置指南

按业务需要选择功能。每页包含适用场景、配置准备、配置案例和验证步骤。

- [命令行与配置管理](01-cli.md)
- [系统设置与远程管理](02-system-services.md)
- [接口与二层交换](03-interfaces-l2.md)
- [IP 接入与静态路由](04-ip-routing.md)
- [动态路由与高可用](05-dynamic-routing.md)
- [隧道与覆盖网络](06-tunnels.md)
- [访问控制、QoS 与 NAT](07-policy.md)
- [DHCP 与网络管理服务](08-network-services.md)
- [运行监控与故障处理](09-operations.md)
- [MPLS 与 L3VPN](10-mpls-l3vpn.md)
- [应用部署与网络](11-applications.md)
- [全命令参考](reference/commands.md)

## 使用约定

- 配置片段使用缩进表示视图。交互输入时，先用 quit 返回上一级视图，再进入下一个同级视图。
- 执行 commit 后配置才生效。利用相应的 display 命令和实际业务验证，再执行 save。
- 示例地址、设备名、接口名与凭据占位符需要按实际网络替换。
