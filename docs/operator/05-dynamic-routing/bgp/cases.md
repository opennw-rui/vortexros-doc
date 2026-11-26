---
nav_title: 配置案例
nav_overview: 案例索引
---


# BGP 与 MP-BGP 配置案例

(case-conditions-05-dynamic-routing-bgp)=
## 配置条件

确保邻居地址可达，规划两端 AS、Router ID 以及要交换的前缀。部署应用策略前检查现有会话。

全系统只允许一个主BGP AS。再次输入相同AS会进入现有视图；输入不同AS会报错且不会修改配置。AS 65535不可使用。

```{toctree}
:maxdepth: 1

cases/example-1
cases/example-2
cases/example-3
cases/example-4
```

(case-verification-05-dynamic-routing-bgp)=
## 通用验证

```vortexros-cli
display bgp peer
display ip routing-table protocol bgp
display ipv6 routing-table
```

确认需要的地址族邻居处于 Established，核对接收路由、下一跳及实际转发。

## 验证与撤销

```vortexros-cli
display bgp peer
display bgp routing-table
display bgp routing-table peer 10.0.0.2 received-routes
display bgp vpnv4 vpn-instance BLUE routing-table
display bgp tcp-protection verbose
```

默认TCP保护只接受已经配置的BGP邻居源地址。需要关闭时：

```text
bgp 64512
 undo default tcp-protected
```

精确删除邻居或单项参数：

```text
bgp 64512
 undo peer 10.0.0.2 route-policy RP-IN import
 undo peer 10.0.0.2 description
 undo peer 10.0.0.2
undo bgp 64512
commit
```
