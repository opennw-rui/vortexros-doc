---
nav_title: 配置案例
nav_overview: 案例索引
---


# MPLS 核心转发 配置案例

(case-conditions-10-mpls-l3vpn-mpls)=
## 配置条件

为每台设备准备唯一 LSR ID，通过 IGP 交换其地址，并在核心接口准备对端连通。

```{toctree}
:maxdepth: 1

cases/example-1
cases/example-2
```

(case-verification-10-mpls-l3vpn-mpls)=
## 通用验证

```vortexros-cli
display mpls interface
display mpls lsp
display mpls forwarding-table
```

确认核心接口启用，建立标签路径后核对标签、下一跳和出接口。

[LDP 标签分发](../ldp.md)
