# WireGuard 隧道

## 功能介绍

WireGuard 用于在站点或终端之间建立加密三层连接。可按对端指定公钥、网络前缀和远端地址。

## 功能特性

隧道用本机私钥标识自己，按对端公钥分别建立会话。目的地址属于多个允许前缀时，使用最长的匹配前缀选择 peer。显式配置外层源地址时，该地址须属于指定的底层路由表。

PHY up 要求 profile 和密钥就绪且隧道已启用，Protocol up 还需要有效的内层地址。检查单个 peer 是否已经握手时，查看其握手时间及收发计数。

## 配置案例

交换两端公钥，规划底层 VPN、业务前缀及 UDP 端口。配置备份可能含有密钥，按凭据保护。

### 使用固定对端和业务前缀

Profile只保存peer集合；Tunnel保存private key、underlay、监听端口和profile引用。

```text
wireguard profile WG-PROFILE
 peer SITE-B
  publickey BASE64-PUBLIC-KEY
  allowd-ip 10.20.0.0 16
  destination 198.51.100.2 port 51820
  keepalive 25
#
interface Tunnel 10
 tunnel-protocol wireguard
 privatekey auto
 source vpn-instance default
 wireguard-profile WG-PROFILE
 mtu 1500
 ip address 10.255.0.1 255.255.255.252
```

`source vpn-instance NAME [IP]`选择underlay VPN；最后的源IP可以省略，省略时VPP按peer endpoint在该VPN中的路由自动选源。客户端省略`source-port`，每次创建接口时使用随机临时源端口。只有作为监听端的服务端才配置固定`source-port`。

Allowed IP限制该peer允许收发的地址范围。Tunnel自身配置的直连前缀如果被某个Allowed IP覆盖，数据面会自动把这个直连前缀映射到最长前缀匹配的peer，因此纯L3 Tunnel上的`/24`等直连网段不需要ARP，也不需要为对端再补`/32`静态路由。Allowed IP不会为Tunnel之外的任意业务网段自动创建系统路由；这些网段仍需静态或动态路由。

Tunnel显式source与所有已配置的peer destination必须使用同一外层地址族。IPv6 overlay可以与IPv4或IPv6 underlay组合，需为peer显式配置IPv6 `allowd-ip`；未配置任何`allowd-ip`时默认仅为`0.0.0.0/0`。不同peer可以配置嵌套的Allowed IP，数据面按最长前缀选择peer；完全相同的前缀不能由两个peer同时拥有。

服务端peer可以不配置`destination`，首个通过认证的报文会学习并更新该peer的漫游endpoint；这种模式必须在Tunnel上配置固定监听端口：

```text
wireguard profile WG-SERVER
 peer ROAMING-CLIENT
  publickey BASE64-PUBLIC-KEY
  allowd-ip 10.40.0.0 24
#
interface Tunnel 11
 tunnel-protocol wireguard
 privatekey auto
 source vpn-instance default
 source-port 51820
 wireguard-profile WG-SERVER
 ip address 10.40.0.1 255.255.255.0
```

- 新增或删除peer只影响该peer；
- 修改密钥、目的地址或监听参数时，相关Tunnel可能短暂重新建立；
- profile仍被Tunnel引用时不能删除；
- 修改underlay source或VPN后，应重新检查到peer公网地址的路由。

```text
interface Tunnel 10
 undo wireguard-profile
 undo source
quit
undo wireguard profile WG-PROFILE
commit
```

```vortexros-cli
display wireguard interface
display interface Tunnel 10
display ip routing-table
ping -vpn-instance BLUE 10.255.0.2
```

除接口状态外，还应从对端确认握手、收发计数和业务路由。只有Tunnel地址可达而业务前缀没有路由时，WireGuard不会自动补充路由。

### 主动连接端与漫游应答端

两台设备以 192.0.2.0/24 互联，R2 的外层地址为 192.0.2.2，底层也可改为经路由器可达。R1 主动发送，R2 固定监听 UDP 51820，从经过认证的流量学习 R1 端点。隧道地址分别为 10.44.0.1/30 和 .2/30。

两端先创建 Tunnel10，指定 `tunnel-protocol wireguard`，执行 `privatekey auto` 并提交一次。用 `display current-configuration` 查看本机公钥，只交换公钥。把以下公钥占位符换成对端公钥，录入其余配置并提交。

**R1**

```text
wireguard profile WG
 peer R2
  publickey R2-PUBLIC-KEY
  allowd-ip 10.44.0.2 32
  destination 192.0.2.2 port 51820
  keepalive 15
#
interface Tunnel 10
 tunnel-protocol wireguard
 source vpn-instance default
 wireguard-profile WG
 ip address 10.44.0.1 255.255.255.252
```

**R2**

```text
wireguard profile WG
 peer R1
  publickey R1-PUBLIC-KEY
  allowd-ip 10.44.0.1 32
#
interface Tunnel 10
 tunnel-protocol wireguard
 source vpn-instance default
 source-port 51820
 wireguard-profile WG
 ip address 10.44.0.2 255.255.255.252
```

```vortexros-cli
display wireguard interface
display interface Tunnel 10
display ip routing-table
```

R1 发起到 10.44.0.2 的 ping 后，两端应能看到握手时间更新与收发计数增长。再从 R2 测试回程。外层通过静态路由到达 R2 时，撤销并恢复该路由，确认外层可达后隧道重新握手。

## 验证配置

```vortexros-cli
display wireguard interface
display interface Tunnel 10
display ip routing-table
```

确认对端握手、收发计数和业务路径。分别验证隧道地址与远端业务网段。
