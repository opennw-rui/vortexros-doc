# 接口与二层交换

- [物理接口与硬件卸载](03-interfaces-l2/physical-interfaces.md)。物理接口可以作为三层端口或二层交换端口。接口配置包括描述、MTU、地址和受支持的硬件卸载功能。
- [Eth-Trunk 链路聚合](03-interfaces-l2/eth-trunk.md)。将多条 Ethernet 链路合为一条逻辑接口，可增加可用带宽并承受单链路故障。可按对端选择手工聚合或 LACP。
- [802.1Q 与 QinQ 三层子接口](03-interfaces-l2/subinterfaces.md)。三层子接口按 802.1Q 标签区分共用物理链路的多个网段。QinQ 用外层和内层标签共同区分业务。
- [VLAN 二层交换](03-interfaces-l2/vlan.md)。VLAN 把同一台设备上的二层交换范围分开。Access 端口连接无标签终端，Trunk 端口在链路上传递指定 VLAN。
- [Vlanif 三层网关](03-interfaces-l2/vlanif.md)。Vlanif 为一个 VLAN 提供三层接口，可作为终端默认网关并在网段之间路由。
- [MAC 地址表](03-interfaces-l2/mac-table.md)。通过 MAC 地址表确认设备把流量转发到哪个端口，也可调整动态表项的老化时间。
- [Bridge Domain 与高位桥域](03-interfaces-l2/bridge-domain.md)。Bridge Domain 为独立的二层业务提供转发域。可连接本地接入口，也可与 VXLAN VNI 关联以延伸至远端。
- [Vbdif 三层网关](03-interfaces-l2/vbdif.md)。Vbdif 是 Bridge Domain 的网关接口。它让桥域中的终端通过网关地址访问其他网段。
- [ARP 与代理 ARP](03-interfaces-l2/arp.md)。ARP 用于查询同链路 IPv4 下一跳的 MAC 地址。代理 ARP 由设备代指定目标响应，用于终端无法直接解析目标但设备有正确转发路径的场景。
- [IPv6 邻居发现与静态邻居](03-interfaces-l2/ipv6-neighbor-discovery.md)。IPv6 邻居发现用于解析相邻节点的链路层地址。可为已知对端设置静态映射，或按需要调整数据面邻居表容量和老化时间。

```{toctree}
:maxdepth: 1
:hidden:

03-interfaces-l2/physical-interfaces
03-interfaces-l2/eth-trunk
03-interfaces-l2/subinterfaces
03-interfaces-l2/vlan
03-interfaces-l2/vlanif
03-interfaces-l2/mac-table
03-interfaces-l2/bridge-domain
03-interfaces-l2/vbdif
03-interfaces-l2/arp
03-interfaces-l2/ipv6-neighbor-discovery
```
