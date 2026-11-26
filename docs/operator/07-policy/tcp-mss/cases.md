---
nav_title: 配置案例
nav_overview: 案例索引
---


# TCP MSS 调整 配置案例

(case-conditions-07-policy-tcp-mss)=
## 配置条件

仅在三层接口或受支持的隧道上配置。核对路径 MTU，以及 TCP 流量的实际入口和出口。

```{toctree}
:maxdepth: 1

cases/example-1
cases/example-2
```

(case-verification-07-policy-tcp-mss)=
## 通用验证

```vortexros-cli
display interface Tunnel 1
display current-configuration | include tcp mss
```

检查接口 MTU 和已提交的 MSS 规则。通过实际 TCP 连接确认 SYN 中的 MSS 符合预期。
