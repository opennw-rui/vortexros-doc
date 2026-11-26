# 路由策略、OSPF、BGP、IS-IS、RIP、BFD 与 VRRP

本章从设备使用者的角度说明如何建立邻居、发布路由、检查结果和撤销配置。示例中的接口、地址、AS号和计时值仅用于说明，部署时应替换为实际规划。

## IP前缀列表与路由策略

前缀列表负责匹配路由，路由策略决定允许、拒绝或修改匹配的路由。下面的策略只允许 `10.0.0.0/8` 中掩码长度为16至24的前缀，并把BGP本地优先级设为200：

```text
ip ip-prefix PL-IN index 10 permit 10.0.0.0 8 greater-equal 16 less-equal 24
route-policy RP-IN permit node 10
 if-match ip-prefix PL-IN
 apply local-preference 200
```

配置完成后，输入 `display ip ip-prefix ?`、`display route-policy ?` 或在协议中输入 `route-policy ?`，会同时显示参数说明和已经存在的对象名称。

命令关键字不区分大小写；用户定义的对象名按输入原样保存并区分大小写。例如`RP-IN`和`rp-in`是两个不同策略，引用时必须使用定义时的大小写。同一个route-policy节点只能有一个IPv4前缀列表条件和一个IPv6前缀列表条件；再次输入同地址族的`if-match`会替换原条件。需要匹配多个前缀时，应在同一个前缀列表中增加多条规则，或者使用不同的策略节点。

IPv6前缀列表和策略条件使用独立命令：

```text
ip ipv6-prefix V6-IN index 10 permit 2001:db8:: 32 greater-equal 48 less-equal 64
route-policy V6-POLICY permit node 10
 if-match ipv6 address prefix-list V6-IN
```

可使用`display ipv6 prefix V6-IN`验证IPv6列表。IPv4与IPv6列表可以同名，但引用命令明确区分地址族；旧入口`display ip ipv6-prefix`仍保留，便于已有运维脚本继续使用。

```vortexros-cli
display ip ip-prefix PL-IN
display route-policy RP-IN
display current-configuration | include PL-IN
```

删除前应先解除协议中的引用：

```text
undo route-policy RP-IN permit node 10
undo ip ip-prefix PL-IN
```

## OSPF

### 使用area下的network激活

```text
ospf 1 router-id 10.0.0.1
 opaque-capability enable
 area 0.0.0.0
  network 10.0.12.1 0.0.0.0 description P1-P2
```

`network`只能在area视图中输入。提交后，地址匹配的接口开始发送Hello报文；只有两端area、网络类型、认证和计时等条件兼容时才会建立邻居。

### 使用接口命令激活

```text
ospf 1 router-id 10.0.0.1
interface Vlanif 12
 ospf enable 1 area 0.0.0.0
 ospf network-type p2p
 ospf cost 10
 ospf dr-priority 100
```

同一进程只能选择 `network` 或接口 `ospf enable` 一种激活方式；混用会在命令进入待提交配置前报错。广播网络上的DR优先级范围为0至255，0表示不参与DR/BDR选举。

### Stub、NSSA与区域汇总

区域类型和汇总在area视图配置：

```text
ospf 1
 area 0.0.0.1
  nssa no-summary
  abr-summary 10.0.0.0 255.0.0.0 not-advertise
```

`stub`与`nssa`互斥；已经配置一种类型时，必须先执行对应的`undo`，不能用另一条命令隐式覆盖。`no-summary`阻止向该区域发布三类汇总路由，`not-advertise`阻止发布指定区域汇总。撤销命令为`undo stub`、`undo nssa`和`undo abr-summary ADDRESS MASK`。

### 验证与撤销

```vortexros-cli
display ospf 1 brief
display ospf 1 peer brief
display ospf 1 peer 10.0.0.2
display ospf 1 interface
display ospf 1 lsdb
display ospf 1 routing
```

`display ospf peer brief`按以下顺序显示，Interface位于Neighbor id左侧：

```text
Area Id    Pri  Up Time   Dead Time  Interface   Neighbor id  State
0.0.0.0      1  00:12:31  00:00:38   Vlanif12    10.0.0.2     Full
```

修改与删除示例：

```text
interface Vlanif 12
 undo ospf dr-priority
 undo ospf network-type
 undo ospf enable 1
undo ospf 1
commit
```

撤销接口激活只影响该接口；删除进程会撤销该进程的全部邻居和路由。

## OSPFv3

OSPFv3用于IPv6动态路由。先创建进程和区域，再在三层接口下绑定进程：

```text
ospfv3 1 router-id 10.0.0.1
 maximum load-balancing 6
 bandwidth-reference 100000
 import-route static
 area 0.0.0.0
interface Vlanif 12
 ospfv3 1 area 0.0.0.0
```

接口必须属于与进程相同的VPN实例。进程1对应default；其他进程必须在创建时指定非default VPN，例如`ospfv3 2 router-id 10.0.0.2 vpn-instance BLUE`。同一个VPN只能对应一个后端OSPFv3实例，同一个接口不能同时加入两个OSPFv3进程。

Stub、NSSA和IPv6区域汇总在area视图配置：

```text
ospfv3 1
 area 0.0.0.1
  nssa no-summary
  abr-summary 2001:db8:: 32 not-advertise
```

`stub`与`nssa`互斥。`default-route-advertise`仅在本机已有IPv6默认路由时发布，`default-route-advertise always`则不依赖本机默认路由。`silent-interface INTERFACE`保留该接口的网络发布但停止建立邻居。

```vortexros-cli
display ospfv3 1 brief
display ospfv3 1 peer brief
display ospfv3 1 interface
display ospfv3 1 lsdb
display ospfv3 1 routing
```

`peer brief`中的邻居状态来自FRR OSPFv3运行态，`routing`中的路由数量只统计协议为`ospf6`的IPv6路由。配置已提交但尚未形成邻接时不会伪造Full状态；验收时应同时确认邻居Full、IPv6路由存在和业务地址可达。

撤销示例：

```text
interface Vlanif 12
 undo ospfv3 1 area 0.0.0.0
ospfv3 1
 area 0.0.0.1
  undo abr-summary 2001:db8:: 32
  undo nssa
undo ospfv3 1
commit
```

## BGP

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

BFD按字段继承。组上启用BFD并配置计时器后，成员默认继承；成员只配置一个计时字段时，仅该字段覆盖组值，其余字段继续继承。`peer ADDRESS bfd disable`用于明确关闭该成员从组继承的BFD，`undo peer ADDRESS bfd disable`恢复继承；`undo peer ADDRESS bfd enable`同样删除成员级开关。存在显式关闭的成员时，系统会把组的有效BFD配置逐一投影到其余成员，避免后端重新继承组BFD而使关闭失效。运行态、BFD会话归属和FRR profile使用同一套有效值。

密码认证使用BGP TCP MD5。当前只提供`simple`形式，密码以明文进入配置并按明文下发到FRR，`display current-configuration`也会显示原值；应限制配置文件、命令输出和运维会话的访问权限。密码长度为1至80个不含空格的可打印字符，不支持`cipher`输入形式。

邻居组不能在仍有成员引用时删除。可按以下顺序撤销：

```text
bgp 64512
 undo peer 192.0.2.2
 undo peer TRANSIT password
 undo group TRANSIT
commit
```

`display bgp group`用于查看后端邻居组状态；`display current-configuration configuration bgp`用于核对设备配置。密码只应通过配置查看，不会作为普通BGP会话状态字段输出。

### VPN与IPv6地址族

```text
bgp 64512
 ipv4-family vpn-instance BLUE
  import-route direct
 ipv6-family vpn-instance BLUE
  import-route direct
```

VPN地址族使用VPN实例下配置的RD和RT。进入VPN地址族后，设备会加入该地址族需要的默认配置。`undo default ipv4-unicast`用于取消自动启用新IPv4邻居；此后需要在IPv4 unicast地址族中显式启用邻居。

IPv4与IPv6邻居只能在对应的unicast地址族视图下修改。引用了IPv4 `ip ip-prefix`的route-policy不能挂载到IPv6邻居或IPv6 network；IPv6地址族应使用`ip ipv6-prefix`和`if-match ipv6 address prefix-list`。IPv6地址族中的`import-route ospf`由系统映射到后端OSPFv3路由类型。

地址族中可以生成聚合路由：

```text
bgp 64512
 ipv4-family unicast
  aggregate 10.0.0.0 255.0.0.0 detail-suppressed
 ipv6-family unicast
  aggregate 2001:db8:: 32 as-set detail-suppressed
```

`detail-suppressed`只发布聚合路由；`as-set`保留组成路由的AS信息。显式使用`as-set`时，系统会同步调整该BGP实例的后端AS_SET接收模式，使配置不会被FRR静默忽略。两项均未配置时，聚合路由与组成路由同时发布。

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

## IS-IS

进程号在设备内全局唯一。一个进程只能绑定一个VPN，一个VPN最多配置一个IS-IS进程；接口所属VPN必须与进程VPN一致。

```text
isis 10 vpn-instance BLUE
 network-entity 49.0001.0100.0000.0001.00
 is-level level-2
 cost-style wide
 log-adjacency-changes
interface Vlanif 100
 isis enable 10
 isis ipv6-enable 10
 isis circuit-type p2p
 isis circuit-level level-2
 isis cost 20
```

提交后，IPv4和IPv6在同一进程中运行。接口VPN不一致、同一接口引用另一个进程或同一VPN已存在其他进程时，命令会被拒绝。

`import-route`用于导入IPv4路由，`ipv6 import-route`用于导入IPv6路由：

```text
isis 10
 import-route static
 ipv6 import-route static
 ipv6 import-route ospfv3
```

系统根据进程的IS-IS level生成FRR要求的`level-1`或`level-2`重分发命令；默认level-1-2会同时下发两级，避免后端接受命令时因缺少level而拒绝配置。

```vortexros-cli
display isis 10 brief
display isis 10 peer
display isis 10 interface
display isis 10 lsdb
display isis 10 route
```

撤销示例：

```text
interface Vlanif 100
 undo isis ipv6-enable 10
 undo isis enable
undo isis 10
commit
```

如果需要把进程迁移到另一个VPN，应先删除进程，再使用新VPN重新创建。

## RIP与RIPng

### RIP IPv4

```text
rip 1
 version 2
 network 10.0.0.0
 default-metric 2
 maximum load-balancing 4
 timers rip 30 180 120
 silent-interface LoopBack 0
```

`network`使用IPv4主类网络地址。提交后匹配接口参加RIP，silent-interface仍发布该接口网络，但不从该接口发送更新。

### RIPng IPv6

```text
ripng 2 vpn-instance BLUE
 network 2001:db8:100::/64
 import-route static
 default-route originate
```

RIPng视图中的`import-route ospf`表示导入OSPFv3路由，系统会映射到后端的IPv6协议名称。

```vortexros-cli
display rip 1 interface
display rip 1 database
display rip 1 route
display ripng 2 interface
display ripng 2 route
```

精确撤销：

```text
rip 1
 undo network 10.0.0.0
 undo timers rip
undo rip 1
undo ripng 2 vpn-instance BLUE
commit
```

## BFD

BFD可建立独立会话，也可由OSPF、IS-IS、RIP和BGP邻居调用。协议会话默认发送间隔1000ms、接收间隔1000ms、检测次数3。

### 独立BFD会话

```text
bfd
bfd TO-P2 bind peer-ip 10.0.12.2 source-ip 10.0.12.1 interface Vlanif 12
 min-tx-interval 300
 min-rx-interval 300
 detect-multiplier 3
 log-session-changes
```

多跳会话需要显式指定 `source-ip`，VPN场景可追加 `vpn-instance BLUE`。

### 路由协议调用BFD

```text
interface Vlanif 12
 ospf bfd enable
 ospf bfd min-tx-interval 300 min-rx-interval 300 detect-multiplier 3
```

```text
bgp 64512
 peer 10.0.0.2 bfd enable
 peer 10.0.0.2 bfd min-tx-interval 300 min-rx-interval 300 detect-multiplier 3
```

IS-IS和RIP使用同样的接口形式，将命令前缀替换为 `isis bfd` 或 `rip bfd`。

```vortexros-cli
display bfd configuration
display bfd session all
display bfd statistics
```

恢复默认计时或删除会话：

```text
bfd TO-P2 bind peer-ip 10.0.12.2 source-ip 10.0.12.1 interface Vlanif 12
 undo min-tx-interval
 undo min-rx-interval
 undo detect-multiplier
undo bfd TO-P2
commit
```

## VRRP与VRRP6

VRRP 让两台或多台设备共享一个网关地址。可在三层 Ethernet、Eth-Trunk、三层子接口、Vlanif 或 Vbdif 配置。IPv4 默认使用 VRRPv2。IPv6 固定使用 VRRPv3，需要配置本组的链路本地虚拟地址。

### IPv4完整示例

假设P1与P2都连接到VLAN 100，客户端使用 `10.100.0.254`作为默认网关。P1优先级120作为Master，P2保持默认优先级100作为Backup。

P1：

```text
interface Vlanif 100
 ip address 10.100.0.1 255.255.255.0
 vrrp vrid 10 virtual-ip 10.100.0.254
 vrrp vrid 10 priority 120
 vrrp vrid 10 timer advertise 1
 vrrp vrid 10 track interface Vlanif 200 reduced 30
```

P2：

```text
interface Vlanif 100
 ip address 10.100.0.2 255.255.255.0
 vrrp vrid 10 virtual-ip 10.100.0.254
 vrrp vrid 10 timer advertise 1
```

IPv4 用首条 `virtual-ip` 创建组。默认优先级为 100、通告间隔为 1 秒、抢占开启。在 P1 已配置的 Vlanif200 断开后，P1 的运行优先级降低 30。若低于 P2，P2 接管虚拟网关。

需要 IPv4 VRRPv3 时，在两端系统视图执行 `vrrp version v3` 并提交。用 `undo vrrp version` 恢复 IPv4 的 v2 默认值。此前保存的按组 v3 配置仍可回放。单播要求 v3，通过 `peer-ip` 配置同链路对端真实地址。IPv6 单播使用对端链路本地地址。删除某个地址族的最后一个对端后，该族恢复组播。

虚拟IP可以与接口自身地址相同。此时设备是该虚拟地址的地址拥有者，运行优先级自动为255；配置中仍保留用户输入的优先级，状态显示以运行优先级为准。

### IPv6示例

```text
interface Vlanif 100
 ipv6 address 2001:db8:100::1 64
 vrrp6 vrid 20 virtual-ip fe80::fe
 vrrp6 vrid 20 virtual-ip 2001:db8:100::fe
 vrrp6 vrid 20 priority 120
 vrrp6 vrid 20 timer advertise 1
```

两端使用相同的 VRID 和虚拟地址。IPv6 的全局虚拟地址可与链路本地虚拟地址同组使用。

### 查看状态和效果

```vortexros-cli
display vrrp brief
display vrrp interface Vlanif 100
display vrrp 10
display vrrp statistics
display vrrp6 brief
```

brief输出示例：

```text
VRID  State   Interface  Type  Virtual IP      Priority  RunPri  Adv
10    Master  Vlanif100  IPv4  10.100.0.254   120       120     1.00s
```

详细输出会显示状态、版本、地址族、虚拟IP、配置优先级、运行优先级、虚拟MAC、通告间隔和抢占状态。配置已经提交但VRRP组尚未创建时，State显示 `Pending (not created in dataplane)`，应检查接口模式、地址和服务健康状态。

数据面遵循VRRPv3规范：IPv4通告校验和只覆盖VRRP消息，IPv6通告使用IPv6伪首部；Master收到优先级低于或等于本机的通告时会立即发送一次自身通告，并继续保持Master状态。此行为可缩短错误Master出现后的收敛时间，不需要额外CLI配置。

业务验证应包括：客户端持续ping虚拟IP和外部地址；关闭Master的上联或被跟踪接口；确认Backup接管、ARP/ND更新且业务恢复；再恢复接口并观察抢占行为。

### 修改和删除

```text
interface Vlanif 100
 undo vrrp vrid 10 track interface Vlanif 200
 undo vrrp vrid 10 priority
 undo vrrp vrid 10 timer advertise
 undo vrrp vrid 10 virtual-ip 10.100.0.254
 undo vrrp vrid 10
```

`undo priority`恢复100，`undo timer advertise`恢复1秒，`undo preempt-mode`恢复抢占。`undo vrrp vrid 10`删除整个IPv4组；IPv6使用对应的 `undo vrrp6 vrid 20 ...`。

## 配置完成后的通用检查

每次变更后至少执行：

```vortexros-cli
display this
commit
display current-configuration
display ip routing-table
display alarm active
```

随后使用本节对应的邻居、路由、BFD或VRRP命令检查运行状态。确认业务正常后再执行 `save`。删除配置时先解除引用或接口绑定，再删除协议进程和策略对象。
