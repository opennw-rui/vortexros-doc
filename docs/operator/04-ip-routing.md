# IPv4/IPv6、VPN、静态路由与路由组

## VPN-instance

VortexROS 为VPN实例分配1024～2048范围内的后端表号，可同时创建1025个
VPN实例。日常配置不会显示容量警告；只有实际超过该数量时，`commit`才会
拒绝配置并显示已配置数量和可用范围。

```text
ip vpn-instance BLUE
 ipv4-family
  route-distinguisher 65000:100
  vpn-target 65000:100 both
 ipv6-family
```

接口、路由和动态路由协议可以引用VPN实例。仍有配置引用时不能删除VPN。RD/RT只需在VPN实例下配置，在BGP VPN地址族中无需重复输入。

## 普通静态路由

```text
ip route-static 203.0.113.0 255.255.255.0 192.0.2.1 preference 60 tag 100 description TO-WAN
ip route-static vpn-instance BLUE 10.0.0.0 8 vpn-instance default 192.0.2.1 Tunnel 1
ipv6 route-static 2001:db8:100:: 64 2001:db8::1
```

多条静态路由在配置中连续显示，不用无意义的`#`逐条分隔。跨VPN下一跳要同时显示目标VPN和下一跳VPN。

```vortexros-cli
display ip routing-table protocol static
display ip routing-table vpn-instance BLUE
display ipv6 routing-table protocol static
display ip fib
display ip fib vpn-instance BLUE
display ipv6 fib
display ipv6 fib vpn-instance BLUE
```

`display ip routing-table`和`display ipv6 routing-table`读取路由控制面的优选结果，并可通过`verbose`或`inactive`查看详细候选。`display ip fib`和`display ipv6 fib`直接读取VPP Binary API返回的实际转发项，不会用控制面路由冒充已生效FIB。两条FIB命令不带参数时查看default表，指定`vpn-instance`时按大小写敏感的VPP表名查看对应VPN；标题显示表名及表ID，`Lookup-Table`显示VPP路径实际使用的递归查表ID，包括default表的`0`。IPv6 FIB采用与IPv6路由表一致的逐路径块状布局；每个块只显示VPP能够证明的目的地址、前缀长度、下一跳、Preference、权重、路径类型、出接口、路径标志和递归查表ID。ECMP的每条有效路径各显示一个块。

## IPv6运行状态命令

在`display ipv6 ?`下会列出当前具有实际数据源的命令。未实现的数据采集能力不会显示成可用命令：

```text
fib                  Display IPv6 FIB information
interface            Display IPv6 interface information
nd                   Display IPv6 neighbor discovery information
neighbors            Display IPv6 neighbor information
pathmtu              Display IPv6 path MTU information
pool                 Display IPv6 pool information
prefix               Display IPv6 prefix-list information
routing-table        Display IPv6 routing table
urpf                 Display IPv6 URPF information
```

`display ipv6 nd`读取VPP的IPv6邻居容量、老化时间与回收策略。容量和回收策略可分别通过`ipv6 nd max-number`与`ipv6 nd recycle`配置；两项`undo`恢复配套VPP 26.06的产品默认值（50000条、关闭回收）。`display ipv6 pathmtu`读取VPP实际路径MTU数据库，可按VPN实例过滤；数据量较大时CLI按VPP游标连续读取全部分页，不会把正常的继续信号显示成错误。`display ipv6 pool`和`display ipv6 prefix`分别显示已提交的DHCPv6地址池和IPv6前缀列表；原有的DHCPv6客户端、中继以及IPv6路由组命令保持不变。

IPv6邻居表直接读取VPP实际ND条目，可按接口、VPN实例或动态/静态类型过滤：

```vortexros-cli
display ipv6 neighbors
display ipv6 neighbors Vlanif 10
display ipv6 neighbors interface Ethernet 1
display ipv6 neighbors vpn-instance BLUE
display ipv6 neighbors dynamic
display ipv6 neighbors static
```

静态邻居使用`ipv6 neighbor IPV6 MAC interface IF`配置并随Candidate、commit和save持久化；删除时使用对应的完整`undo ipv6 neighbor ...`命令。`undo`中的接口、IPv6地址和MAC必须与Candidate中的条目完全匹配，避免输错MAC时误删另一条配置。承载接口被删除并重建后，即使静态邻居配置本身未变化，控制面也会重新下发该条目。commit会以VPP静态邻居表为权威读回，不能把动态学习条目误认为已配置静态条目。

每个邻居使用独立的信息块，`IPv6 Address`独占一行；其余字段固定按`Link-layer/State`、`Interface/Age`、`VLAN/CEVLAN`、`VPN name/Is Router`两列显示，`Secure FLAG`单列显示。动态和静态类型只在汇总中计数，不增加无后端字段的明细行。VLAN信息只来自已提交模型，不根据接口名称猜测：Vlanif使用其VLAN，子接口使用外层/内层VLAN，Vbdif只有在业务桥域明确绑定VLAN时才显示该VLAN；桥域ID不会冒充VLAN ID。当前VPP Binary API不提供完整ND状态、Router标志和SEND安全状态，这些字段显示`-`，不会伪造为REACH、Router或安全邻居。命令也不会根据接口地址伪造本机邻居项。

## 静态路由组

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

首次`commit`会解析、规范化并生成不可变运行快照。之后直接修改原文件不会绕过配置事务改变现网；执行下面的命令才会重新读取、显示进度并增量更新路由：

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

## 路由组增量修改

- 一个成员变化只影响“该前缀×引用该组的绑定”；
- 一个绑定变化只处理该组成员；
- 普通静态路由和多个路由组产生完全相同的路径和属性时，设备只保留一条有效路由；
- 路径相同但Preference、Tag等不同会报告冲突；
- 增加或删除单个成员时，只更新该成员所影响的路由，不重新加载整个路由组。

## uRPF与路由表

接口可以启用严格或宽松的反向路径检查：

```text
interface Vlanif 100
 ip urpf strict
 ipv6 urpf strict
```

- `strict`：源地址的最佳返回路径必须从收到报文的接口到达；
- `loose`：源地址只需在路由表中可达；
- `disable`或对应的`undo ip urpf`、`undo ipv6 urpf`：关闭该地址族检查。

IPv4和IPv6 uRPF是两个独立配置对象，修改或撤销其中一个不会覆盖另一个。使用 `display urpf` 查看全部地址族，使用`display ipv6 urpf`只查看IPv6接口模式；通过`display ip routing-table ... verbose`或`display ipv6 routing-table ... verbose`检查作为判断依据的路由。

## 功能验证表

| 场景 | 配置 | 数据面效果 | 验证 |
|---|---|---|---|
| 直连下一跳 | 普通静态路由 | 安装到目标VRF | ping和routing-table |
| 递归下一跳 | 先建递归可达路由 | 解析成功后安装 | verbose中的NextHop/Interface |
| ECMP | 同前缀不同下一跳 | 多路径进入RIB/FIB | route verbose和流量 |
| 跨VPN | 目标VPN+下一跳VPN | 在目标表安装、去指定表解析下一跳 | 两个VPN路由表 |
| 默认路由 | `/0` | 无更长匹配时使用 | 特定目的ping/tracert |
| 精确undo | 完整路径参数 | 只删除一个所有者/路径 | 其他所有者仍保留 |

最后用 `display current-configuration` 核对路由组定义和 `ip route-static group` 绑定。IPv6 绑定使用 `ipv6 route-static group`。
