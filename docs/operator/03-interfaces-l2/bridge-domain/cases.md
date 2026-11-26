---
nav_title: 配置案例
nav_overview: 案例索引
---


# Bridge Domain 与高位桥域 配置案例

(case-conditions-03-interfaces-l2-bridge-domain)=
## 配置条件

普通 VLAN 的可用 VID 为 1–4094。高位 BD 可使用 4096–4294967294，适用于显式引用桥域的业务。普通 STP、RSTP 和 MSTP 的适用范围不变。

```{toctree}
:maxdepth: 1

cases/example-1
cases/example-2
```

(case-verification-03-interfaces-l2-bridge-domain)=
## 通用验证

```vortexros-cli
display bridge-domain 11
display bridge-domain 65536
display mac-address
display vxlan tunnel
```

确认本地接口、VNI 与远端 VTEP 归属。高位域之间可以重复使用客户 VID 或 MAC，分别验证域内连通、域间隔离，并确认迁移后的旧远端条目已撤销。

[Vbdif 网关](../vbdif.md) · [VXLAN EVPN](../../06-tunnels/vxlan-evpn.md)
