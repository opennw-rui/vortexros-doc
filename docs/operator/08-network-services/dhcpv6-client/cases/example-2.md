---
nav_title: 联动服务器的前缀委派
---


# 联动服务器的前缀委派

## 拓扑

![DHCPv6 客户端，2001:db8:20::2 → Ethernet0 直连，2001:db8:20::/64 → 服务器，2001:db8:20::1](example-2.svg)

## 配置条件

确认上游支持有状态地址分配或前缀委派。如果还需要默认路由，请准备 RA。

服务器与客户端 Ethernet0 直连，传输网段使用 2001:db8:20::/64。服务器把 2001:db8:100::/56 划分成 /64 委派给客户端。两台设备分别录入并提交。

## 配置步骤

**本端设备**

```vortexros-config
enable dhcp server
#
dhcpv6 pool PD
 prefix-delegation 2001:db8:100::/56 64 life-time 3600 1800
#
interface Ethernet 0
 ipv6 enable
 ipv6 address 2001:db8:20::1 64
 dhcpv6 server PD
#
return
```

**对端设备**

```vortexros-config
interface Ethernet 0
 ipv6 enable
 ipv6 address 2001:db8:20::2 64
 dhcpv6 client pd CPE-PREFIX
#
return
```

## 验证方法

对照以下命令和预期结果核对设备状态。

```vortexros-cli
display dhcpv6 pool name PD used
display dhcpv6 client prefix name CPE-PREFIX
```

第一条在服务器查询，第二条在客户端查询。服务器应有 IA_PD 记录，客户端所获前缀与服务器相同，长度为 /64。撤销客户端的 PD 后复查该接口不再使用委派前缀。
