---
nav_title: 注意事项
---


# BGP 与 MP-BGP 注意事项

会话已建立只表示 TCP/BGP 正常。还需检查指定地址族的前缀、策略效果和实际路径。共享密钥按设备保存。

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
