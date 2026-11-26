---
nav_title: 创建手工路由组
---


# 创建手工路由组

## 拓扑

![手工或外部前缀清单 → 本机路由组 → 配置的下一跳](example-1.svg)

## 配置条件

提前准备源文件或 URL、下一跳和 VPN。大批量变更前准备可用的回退配置。

静态路由组用于让大量前缀共用相同的下一跳、出接口、VPN、Preference和Tag。配置中只保留路由组及其绑定关系，不会把十万条成员展开成同样数量的普通静态路由命令。

## 配置步骤

```text
route-static group name CDN
 description CDN-PREFIXES
 route 198.18.0.0/24
 route 198.18.1.1
#
ip route-static group CDN 192.0.2.1 preference 60 tag 100
```

裸IPv4规范为`/32`，裸IPv6规范为`/128`，输入掩码后配置统一显示CIDR。手工成员自动去重。

## 验证方法

对照以下命令和预期结果核对设备状态。

```vortexros-cli
display route-static group name CDN verbose
display ip routing-table group name CDN verbose
```

组中应显示录入前缀，实际路由使用配置的下一跳及优先级。
