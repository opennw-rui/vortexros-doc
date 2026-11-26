---
nav_title: 功能特性
---


# IPIP Tunnel 功能特性

隧道模式由内层、外层地址族决定，两端必须一致。

| 模式 | 内层 | 外层 |
| --- | --- | --- |
| `ipv4-ipv4` | IPv4 | IPv4 |
| `ipv6-ipv4` | IPv6 | IPv4 |
| `ipv4-ipv6` | IPv4 | IPv6 |
| `ipv6-ipv6` | IPv6 | IPv6 |

与 [GRE Tunnel](../gre.md) 一样，外层端点不完整时显示 `^down`。PHY up 要求隧道已启用且本端有可用的底层转发路径。Protocol up 还要求内层地址有效。
