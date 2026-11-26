---
nav_title: 配置案例
nav_overview: 案例索引
---


# 静态路由组 配置案例

(case-conditions-04-ip-routing-static-route-groups)=
## 配置条件

提前准备源文件或 URL、下一跳和 VPN。大批量变更前准备可用的回退配置。

```{toctree}
:maxdepth: 1

cases/example-1
cases/example-2
cases/example-3
```

(case-verification-04-ip-routing-static-route-groups)=
## 通用验证

```vortexros-cli
display route-static group name CDN verbose
display ip routing-table group name CDN verbose
```

确认组内的前缀数量、数据来源和刷新状态。检查相关路由是否使用预期的下一跳，随后测试一个新增前缀和一个已撤销前缀。
