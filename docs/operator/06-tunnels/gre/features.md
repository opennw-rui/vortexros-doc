---
nav_title: 功能特性
---


# GRE Tunnel 功能特性

用 `display interface Tunnel 1` 或 `display interface brief` 查看状态。PHY 反映隧道自身和底层路径是否就绪，Protocol 还取决于隧道接口的三层地址。

| 状态 | 判定条件 |
| --- | --- |
| PHY up | GRE 协议和两端外层地址已配置，运行中的隧道已启用，源地址属于所选底层路由表，目的地址在同一表中有可用转发路径。 |
| Protocol up | PHY 已 up，且 Tunnel 接口具备有效的内层 IP 地址。没有内层地址时，PHY 可以是 up，Protocol 显示 down。 |
| `^down` | 协议或外层端点配置不完整，隧道等待创建。 |
| `down` | 配置已完整，但运行接口、源地址或底层路径尚未就绪。 |
| `*down` | 已通过 `shutdown` 管理关闭。 |

GRE 的 up 反映本端条件。两端配置是否一致、业务是否可用，以隧道内的双向流量为准。
