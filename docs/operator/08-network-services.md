# DHCP 与网络管理服务

- [DHCPv4 服务器](08-network-services/dhcpv4-server.md)。为直连客户端分配 IPv4 地址、网关、DNS 及租期。可使用全局地址池，也可根据三层接口地址建立接口地址池。
- [DHCPv4 客户端](08-network-services/dhcpv4-client.md)。在上联动态取得 IPv4 地址、租约与路由，适用于由上游网络分配地址的接口。
- [DHCPv4 中继](08-network-services/dhcpv4-relay.md)。DHCPv4 中继将本地客户端的请求转发到其他子网的 DHCPv4 服务器，使多个接入网段可以共用服务。
- [DHCPv6 服务器](08-network-services/dhcpv6-server.md)。DHCPv6 服务器可向客户端分配 IPv6 地址，也可在支持的地址池中分配委派前缀。IPv6 默认路由另由 RA 或静态配置提供。
- [DHCPv6 客户端与前缀委派](08-network-services/dhcpv6-client.md)。在三层上联获取 IPv6 地址或受委派前缀。IPv6 的默认网关由路由通告或静态路由提供。
- [DHCPv6 中继](08-network-services/dhcpv6-relay.md)。在不同 IPv6 网段之间传递 DHCPv6 请求，使接入网段可使用远端服务器。
- [LLDP 邻居发现](08-network-services/lldp.md)。LLDP 发现直连链路另一端的设备与端口，适用于核对链路接线和邻接关系。
- [SNMP 监控](08-network-services/snmp.md)。SNMP 允许网管系统读取设备状态并接收通知。只读轮询支持 SNMPv2c，SNMPv3 支持 authPriv。

```{toctree}
:maxdepth: 1
:hidden:

08-network-services/dhcpv4-server
08-network-services/dhcpv4-client
08-network-services/dhcpv4-relay
08-network-services/dhcpv6-server
08-network-services/dhcpv6-client
08-network-services/dhcpv6-relay
08-network-services/lldp
08-network-services/snmp
```
