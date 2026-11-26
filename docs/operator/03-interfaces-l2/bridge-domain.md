# Bridge Domain 与高位桥域

## 功能介绍

Bridge Domain 为独立的二层业务提供转发域。可连接本地接入口，也可与 VXLAN VNI 关联以延伸至远端。

## 配置准备

普通 VLAN 的可用 VID 为 1–4094。高位 BD 可使用 4096–4294967294，适用于显式引用桥域的业务。普通 STP、RSTP 和 MSTP 的适用范围不变。

## 配置案例

```text
bridge-domain 11
 l2 binding vlan 100
 vxlan vni 1011
interface Vbdif 11
 ip address 10.11.0.1 255.255.255.0
```

验证BD、VNI、MAC学习和L3网关：

```vortexros-cli
display bridge-domain 11
display mac-address
display interface Vbdif 11
```

删除前先解除Vbdif、VNI和VLAN绑定，避免业务仍在引用BD。

### 高位 BD 动态 EVPN 配置

```text
system-view
evpn-overlay enable
bridge-domain 65536
vxlan vni 65010
evpn
route-distinguisher 65000:1101
vpn-target 65000:65010 import-extcommunity
vpn-target 65000:65010 export-extcommunity
quit
quit
interface Ethernet0
bridge-domain 65536
quit
interface Nve1
vni 65010 head-end peer-list protocol bgp
quit
commit
```

部署高位 EVPN 时，用 `display bridge-domain` 和 `display mac-address` 核对域归属和 MAC 学习，再检查 VNI、远端 VTEP 和 EVPN 路由。迁移网关或成员后，确认旧位置的远端 MAC/IP 已撤销并在新位置重新学习。可以在不同域使用同一客户 VID 或 MAC，验证时应检查域间隔离和域内连通。

撤销该 VNI 的动态通告时，在对应 NVE 视图执行 `undo vni 65010 head-end peer-list protocol bgp` 并提交。随后核对受影响域的远端状态和其余域的转发。

## 验证配置

```vortexros-cli
display bridge-domain 11
display bridge-domain 65536
display mac-address
display vxlan tunnel
```

确认本地接口、VNI 与远端 VTEP 归属。高位域之间可以重复使用客户 VID 或 MAC，分别验证域内连通、域间隔离，并确认迁移后的旧远端条目已撤销。

[Vbdif 网关](vbdif.md) · [VXLAN EVPN](../06-tunnels/vxlan-evpn.md)
