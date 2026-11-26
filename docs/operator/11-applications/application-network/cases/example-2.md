---
nav_title: 应用出口放行、发布与撤销
---


# 应用出口放行、发布与撤销

## 拓扑

![应用与独立数据卷 → 应用双栈桥 → 管理上联与外部服务](example-2.svg)

## 配置条件

准备独立应用卷、支持应用桥的签名应用，以及在默认路由表可达的上联。先创建桥，再安装和启动使用该桥的应用。

应用 probe 使用 192.0.2.10，设备 Ethernet2 为外部上联。198.51.100.2 同时提供 DNS 和 HTTPS。外部访问者从允许的 198.51.100.0/25 测试 198.51.100.1:8443，再从未授权的来源做对照。

## 配置步骤

先以不含 publish 的策略文件创建桥，再安装并启动 probe。待应用有固定地址后应用完整策略。

```sh
sudo vortexros-image app bridge-create 192.0.2.0/24 2001:db8:400::/64 1420 /path/initial-policy.json
sudo vortexros-image app bridge-policy /path/policy.json
sudo vortexros-image app bridge-status
```

正常时应用仅匹配所配 DNS 和 HTTPS 出口，外部端口只接受显式来源。若启用 advertise，在设备用 `display ip routing-table` 和 `display ipv6 routing-table` 查厂内应用前缀，只有配置发布的路由邻居才应收到通告。清空策略后，重复测试并确认许可流量、端口发布和通告撤销。

## 验证方法

对照以下命令和预期结果核对设备状态。

```vortexros-cli
display ip routing-table
display ipv6 routing-table
```

用 app bridge-status 核对应用桥策略，分别从允许和拒绝的来源测试。开启通告后核对两个前缀，撤销后复查。
