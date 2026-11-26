---
nav_title: 配置案例
nav_overview: 案例索引
---


# AmneziaWG 隧道 配置案例

(case-conditions-06-tunnels-amneziawg)=
## 配置条件

为两端准备独立密钥、可达的外层路径及相同的协议参数。外层 UDP 监听端口应符合部署规划。

两端使用一致的协议参数，交换公钥，确认 VPN 路由和 UDP 端口可达。使用独立设备密钥。

```{toctree}
:maxdepth: 1

cases/example-1
cases/example-2
```

(case-verification-06-tunnels-amneziawg)=
## 通用验证

```vortexros-cli
display amneziawg interface Tunnel 20
display amneziawg peer AWG-PROFILE SITE-B
display interface Tunnel 20
```

检查对端握手后收发计数是否增加，从两端测试隧道地址和业务前缀。维护后要复查底层出口及隧道状态。
