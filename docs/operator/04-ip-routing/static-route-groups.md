# 静态路由组

## 功能介绍

用一个可维护的前缀清单管理具有相同下一跳和属性的多条静态路由。可录入手工成员，也可从文件或 URL 读取。

## 配置准备

提前准备源文件或 URL、下一跳和 VPN。大批量变更前准备可用的回退配置。

## 配置案例

静态路由组用于让大量前缀共用相同的下一跳、出接口、VPN、Preference和Tag。配置中只保留路由组及其绑定关系，不会把十万条成员展开成同样数量的普通静态路由命令。

```text
route-static group name CDN
 description CDN-PREFIXES
 route 198.18.0.0/24
 route 198.18.1.1
#
ip route-static group CDN 192.0.2.1 preference 60 tag 100
```

裸IPv4规范为`/32`，裸IPv6规范为`/128`，输入掩码后配置统一显示CIDR。手工成员自动去重。

### 文件成员与URL成员

路由组的外部列表统一存放在：

```text
/vortexros/route-static-groupd
```

管理员可先把每行一个CIDR的文件放到该目录，再在路由组视图中选择。`?`和Tab只列出目录顶层的普通文件，不接受子目录、符号链接或包含路径分隔符的名称：

```text
route-static group name CDN
 source file cdn-v4.txt
```

直接修改原文件不会立即改变已生效的路由。执行下面的命令才会重新读取、显示进度并增量更新路由：

```vortexros-cli
reset route-static group name CDN
```

URL与本地文件互斥。URL下载后的原始物化结果和元数据也由系统存放在同一目录的受管子目录中：

```text
route-static group name CDN
 source url https://lists.example.net/cdn-v4.txt vpn-instance BLUE
 auto-refresh enable
 auto-refresh interval 4320
```

URL默认必须使用HTTPS。只有明确接受明文传输的受控环境才可配置
`source url http://192.0.2.10/routes.txt insecure`；HTTPS来源不允许经重定向降级为HTTP。

两种来源的内容均为每行一个CIDR，空行和整行`#`注释跳过；任一非法行使新版本整体失效。手工与外部成员取并集。本地文件不支持`auto-refresh`；URL可按配置定时刷新。

首次配置URL后，执行全局 `commit` 会显示连接、下载、检查、应用和完成等进度；只有文件下载并检查成功后配置才会生效。后续普通commit不会重复下载：

```vortexros-cli
reset route-static group name CDN
display route-static group name CDN verbose
display ip routing-table group name CDN verbose
```

Ctrl+C只停止当前终端的进度显示，不取消设备正在执行的更新，也不关闭SSH。

## 验证配置

```vortexros-cli
display route-static group name CDN verbose
display ip routing-table group name CDN verbose
```

确认组内的前缀数量、数据来源和刷新状态。检查相关路由是否使用预期的下一跳，随后测试一个新增前缀和一个已撤销前缀。
