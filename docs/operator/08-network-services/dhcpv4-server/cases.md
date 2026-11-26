---
nav_title: 配置案例
nav_overview: 案例索引
---


# DHCPv4 服务器 配置案例

(case-conditions-08-network-services-dhcpv4-server)=
## 配置条件

准备三层接口及可用地址范围。一个地址池只绑定同一 VPN 内的一个服务接口。交换端口所在的网段应使用对应 Vlanif 提供 DHCP。

```{toctree}
:maxdepth: 1

cases/example-1
cases/example-2
```

(case-verification-08-network-services-dhcpv4-server)=
## 通用验证

```vortexros-cli
display dhcp service verbose
display ip pool
display ip pool used
```

核对服务 Ready 和地址池配置，让终端重新请求租约，检查分配地址、网关与有效期。DHCP 中的 DNS 选项用于客户端。
