---
nav_title: 配置案例
nav_overview: 案例索引
---


# RIPng（IPv6） 配置案例

(case-conditions-05-dynamic-routing-ripng)=
## 配置条件

准备已配置 IPv6 的链路。如果使用 BLUE，先创建并配置相应的 IPv6 VPN 实例。

```{toctree}
:maxdepth: 1

cases/example-1
cases/example-2
```

(case-verification-05-dynamic-routing-ripng)=
## 通用验证

```vortexros-cli
display ripng 2 route
display ipv6 routing-table vpn-instance BLUE
```

确认学到的前缀出现在对应 VPN 和接口。撤销进程后，相关学到的路由应退出路由表。
