---
nav_title: 配置案例
nav_overview: 案例索引
---


# WireGuard 隧道 配置案例

(case-conditions-06-tunnels-wireguard)=
## 配置条件

交换公钥，规划内层地址、外层路由及监听 UDP 端口。准备每端独立生成的私钥。

交换两端公钥，规划底层 VPN、业务前缀及 UDP 端口。配置备份可能含有密钥，按凭据保护。

```{toctree}
:maxdepth: 1

cases/example-1
cases/example-2
```

(case-verification-06-tunnels-wireguard)=
## 通用验证

```vortexros-cli
display wireguard interface
display interface Tunnel 10
display ip routing-table
```

确认对端握手、收发计数和业务路径。分别验证隧道地址与远端业务网段。
