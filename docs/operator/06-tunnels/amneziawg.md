# AmneziaWG 隧道

## 功能介绍

AmneziaWG 为站点间提供加密隧道及可配置的握手与报文格式。可以与 WireGuard 并行配置。

## 配置准备

两端使用一致的协议参数，交换公钥，确认 VPN 路由和 UDP 端口可达。使用独立设备密钥。

## 配置案例

AmneziaWG使用独立的数据面插件、接口和peer对象，不替换WireGuard；两类隧道可以同时配置。Profile除peer外，还保存握手前垃圾包、报文前置填充、消息头范围、内容填充、随机尾部和定时参数。两端必须使用一致的协议参数。

下面示例启用3个随机垃圾包、不同消息头范围和固定前置填充。启用header protection时，四类报文的前置填充都必须不少于12字节。

```text
amneziawg profile AWG-PROFILE
 junk size 16 48
 junk count 3
 padding init 24
 padding response 28
 padding cookie 20
 padding transport 16
 header init 100 110
 header response 200 210
 header cookie 300 310
 header transport 400 410
 padding content 4 16
 timing rekey-timeout 4 6
 header-protection BASE64-32-BYTE-KEY
 random-trailers enable
 junk-packet 1 expression "<b 0x160301><c><t><r 32><rc 16><rd 8>"
 #
 peer SITE-B
  publickey BASE64-PUBLIC-KEY
  allowd-ip 10.30.0.0 16
  destination 198.51.100.2 port 51820
  keepalive 25
#
interface Tunnel 20
 tunnel-protocol amneziawg
 privatekey auto
 source vpn-instance default
 amneziawg-profile AWG-PROFILE
 mtu 1500
 ip address 10.255.20.1 255.255.255.252
commit
```

`junk-packet SLOT BASE64`用于配置1至5号静态原始报文槽位；`junk-packet SLOT expression "EXPRESSION"`用于动态生成握手前报文。表达式支持：`<b 0x...>`固定字节、`<c>`每次握手随机起始且逐槽递增的32位网络序计数、`<t>`当前Unix秒、`<r N>`随机字节、`<rc N>`随机英文字母和`<rd N>`随机数字。表达式最多4096字节，展开后的单个报文最多4096字节，动态标签最多128个Jc/Jmin/Jmax产生的随机垃圾包与这些槽位相互独立。

Allowed IP、underlay VPN、动态客户端源端口、固定服务端监听端口和漫游endpoint的语义与WireGuard相同。Tunnel直连前缀会按Allowed IP最长前缀映射到peer，非直连业务网段仍由路由配置决定。修改协议参数时，已存在的peer会被最小化重建；修改单个peer只影响该peer。

验证命令：

```vortexros-cli
display amneziawg profile AWG-PROFILE
display amneziawg peer AWG-PROFILE SITE-B
display amneziawg interface Tunnel 20
display interface Tunnel 20
ping 10.255.20.2
```

删除时先解除Tunnel引用，再删除profile：

```text
interface Tunnel 20
 undo amneziawg-profile
quit
undo amneziawg profile AWG-PROFILE
commit
```

### 主动连接端与漫游应答端

两台设备以 192.0.2.0/24 互联，R2 的外层地址为 192.0.2.2，底层也可改为经路由器可达。R1 主动发送，R2 固定监听 UDP 3443，从经过认证的流量学习 R1 端点。隧道地址分别为 10.44.0.1/30 和 .2/30。

两端先创建 Tunnel20，指定 `tunnel-protocol amneziawg`，执行 `privatekey auto` 并提交一次。用 `display current-configuration` 查看本机公钥，只交换公钥。把以下公钥占位符换成对端公钥，录入其余配置并提交。

**R1**

```text
amneziawg profile AWG
 junk size 16 48
 junk count 3
 peer R2
  publickey R2-PUBLIC-KEY
  allowd-ip 10.44.0.2 32
  destination 192.0.2.2 port 3443
  keepalive 15
#
interface Tunnel 20
 tunnel-protocol amneziawg
 source vpn-instance default
 amneziawg-profile AWG
 ip address 10.44.0.1 255.255.255.252
```

**R2**

```text
amneziawg profile AWG
 junk size 16 48
 junk count 3
 peer R1
  publickey R1-PUBLIC-KEY
  allowd-ip 10.44.0.1 32
#
interface Tunnel 20
 tunnel-protocol amneziawg
 source vpn-instance default
 source-port 3443
 amneziawg-profile AWG
 ip address 10.44.0.2 255.255.255.252
```

```vortexros-cli
display amneziawg interface
display interface Tunnel 20
display ip routing-table
```

R1 发起到 10.44.0.2 的 ping 后，两端应能看到握手时间更新与收发计数增长。再从 R2 测试回程。外层通过静态路由到达 R2 时，撤销并恢复该路由，确认外层可达后隧道重新握手。 AmneziaWG 的垃圾包和其他握手参数应在两端使用一致的值。

## 验证配置

```vortexros-cli
display amneziawg interface Tunnel 20
display amneziawg peer AWG-PROFILE SITE-B
display interface Tunnel 20
```

检查对端握手后收发计数是否增加，从两端测试隧道地址和业务前缀。维护后要复查底层出口及隧道状态。
