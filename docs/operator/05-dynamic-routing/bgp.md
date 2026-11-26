# BGP 与 MP-BGP

## 功能介绍

BGP 用于 AS 间和 AS 内的路由交换。按地址族激活邻居，可处理 IPv4、IPv6 和 VPN 路由。

## 配置准备

确保邻居地址可达，规划两端 AS、Router ID 以及要交换的前缀。部署应用策略前检查现有会话。

## 配置案例

全系统只允许一个主BGP AS。再次输入相同AS会进入现有视图；输入不同AS会报错且不会修改配置。AS 65535不可使用。

### 建立IPv4邻居

```text
bgp 64512
 router-id 10.0.0.1
 peer 10.0.0.2 as-number 64513
 peer 10.0.0.2 description EBGP-P2
 peer 10.0.0.2 connect-interface LoopBack 0
 peer 10.0.0.2 route-policy RP-IN import
 ipv4-family unicast
  network 10.10.0.0 255.255.0.0
```

提交后，设备使用指定源接口连接邻居，对收到的路由应用 `RP-IN`，并在本地路由表存在相同前缀时发布network。输入 `lo0` 等合法缩写时，配置会显示为设备中的规范接口名。

### 邻居组与TCP MD5认证

具有相同属性的邻居可以加入同一个邻居组。内部组继承本地AS；外部组必须先指定对端AS，再加入成员：

```text
bgp 64512
 group IBGP-RR internal
 peer IBGP-RR password simple Lab-Password-01
 peer IBGP-RR connect-interface LoopBack 0
 peer 10.0.0.2 group IBGP-RR
 peer 10.0.0.3 group IBGP-RR
 group TRANSIT external
 peer TRANSIT as-number 64513
 peer TRANSIT password simple Transit-Password-01
 peer 192.0.2.2 group TRANSIT
 ipv4-family unicast
  peer IBGP-RR reflect-client
  peer TRANSIT route-policy RP-IN import
```

命令关键字不区分大小写，邻居组名称按输入原样保存并区分大小写；`TRANSIT`与`transit`是两个不同对象。成员继承组的AS、认证、源接口及地址族策略。邻居可以用`peer ADDRESS password simple PASSWORD`设置自己的认证密码，以覆盖组密码。已经加入邻居组的成员不能再单独配置AS；需要改变归属时，应先执行`undo peer ADDRESS`，再重新创建。

BFD 计时器按字段继承。成员单独配置的计时字段覆盖组值，其余字段继续继承。`peer ADDRESS bfd disable` 停用该成员继承的 BFD，`undo peer ADDRESS bfd disable` 恢复继承。

BGP 使用 TCP MD5，两端应配置同一共享密钥。交互配置使用 `password simple`，保存的 CFG 使用设备密钥加密。跨设备迁移时在目标设备重新录入共享密钥。密码长度为 1–80 个非空格可打印字符。

邻居组不能在仍有成员引用时删除。可按以下顺序撤销：

```text
bgp 64512
 undo peer 192.0.2.2
 undo peer TRANSIT password
 undo group TRANSIT
commit
```

`display bgp group` 用于查看邻居组状态，`display current-configuration configuration bgp` 用于核对设备配置。普通 BGP 会话状态不显示密码。

### VPN与IPv6地址族

```text
bgp 64512
 ipv4-family vpn-instance BLUE
  import-route direct
 ipv6-family vpn-instance BLUE
  import-route direct
```

VPN地址族使用VPN实例下配置的RD和RT。进入VPN地址族后，设备会加入该地址族需要的默认配置。`undo default ipv4-unicast`用于取消自动启用新IPv4邻居；此后需要在IPv4 unicast地址族中显式启用邻居。

在对应的 unicast 地址族下修改邻居。IPv6 邻居或 network 的策略应使用 `ip ipv6-prefix` 和 `if-match ipv6 address prefix-list`。IPv6 地址族中的 `import-route ospf` 导入 OSPFv3 路由。

地址族中可以生成聚合路由：

```text
bgp 64512
 ipv4-family unicast
  aggregate 10.0.0.0 255.0.0.0 detail-suppressed
 ipv6-family unicast
  aggregate 2001:db8:: 32 as-set detail-suppressed
```

`detail-suppressed` 只发布聚合路由。`as-set` 保留组成路由的 AS 信息。两项均未配置时，聚合路由与组成路由同时发布。

### 验证与撤销

```vortexros-cli
display bgp peer
display bgp routing-table
display bgp routing-table peer 10.0.0.2 received-routes
display bgp vpnv4 vpn-instance BLUE routing-table
display bgp tcp-protection verbose
```

默认TCP保护只接受已经配置的BGP邻居源地址。需要关闭时：

```text
bgp 64512
 undo default tcp-protected
```

精确删除邻居或单项参数：

```text
bgp 64512
 undo peer 10.0.0.2 route-policy RP-IN import
 undo peer 10.0.0.2 description
 undo peer 10.0.0.2
undo bgp 64512
commit
```

### 直连 eBGP 双向发布环回地址

R1 AS 64512 和 R2 AS 64513 通过 Ethernet0 的 192.0.2.0/24 直连。各自只发布本机 LoopBack0 的 /32。

两台设备分别在系统视图录入各自的配置片段，退出功能视图后提交。

**R1**

```vortexros-config
interface Ethernet 0
 ip address 192.0.2.1 255.255.255.0
#
interface LoopBack 0
 ip address 198.51.100.1 255.255.255.255
#
bgp 64512
 router-id 198.51.100.1
 peer 192.0.2.2 as-number 64513
 ipv4-family unicast
  peer 192.0.2.2 enable
  network 198.51.100.1 255.255.255.255
#
return
```

**R2**

```vortexros-config
interface Ethernet 0
 ip address 192.0.2.2 255.255.255.0
#
interface LoopBack 0
 ip address 198.51.100.2 255.255.255.255
#
bgp 64513
 router-id 198.51.100.2
 peer 192.0.2.1 as-number 64512
 ipv4-family unicast
  peer 192.0.2.1 enable
  network 198.51.100.2 255.255.255.255
#
return
```

分别查看状态。

```vortexros-cli
display bgp peer
display bgp routing-table
display ip routing-table protocol bgp
```

两端邻居均为 Established。R1 的远端 198.51.100.2/32 下一跳应为 192.0.2.2，AS 路径应含 64513。R2 可观察反向结果。各自从环回发起对端测试。

## 验证配置

```vortexros-cli
display bgp peer
display ip routing-table protocol bgp
display ipv6 routing-table
```

确认需要的地址族邻居处于 Established，核对接收路由、下一跳及实际转发。
