---
nav_title: 配置案例
nav_overview: 案例索引
---


# 本机 DNS 解析 配置案例

(case-conditions-02-system-services-dns)=
## 配置条件

确认 DNS 服务器在默认路由表中可达。192.0.2.53 是示例地址。

```{toctree}
:maxdepth: 1

cases/example-1
cases/example-2
```

(case-verification-02-system-services-dns)=
## 通用验证

```vortexros-cli
display dns server
```

确认服务器列表显示配置地址，再用实际可解析的主机名测试。
