# 静态 VXLAN 与 NVE

## 功能介绍

VXLAN 在 IP 网络上延伸二层业务。静态模式从 NVE 手动指定远端 VTEP，适用于远端固定的部署。

## 配置准备

为两台设备规划可达的 VTEP 地址，预建相同的 VNI 与本地桥域。示例源地址 192.0.2.1，远端 192.0.2.2。

## 配置案例

```text
interface Nve 1
 source 192.0.2.1
 vni 1011 head-end peer-list 192.0.2.2
```

使用 [Bridge Domain](../03-interfaces-l2/bridge-domain.md) 绑定本地业务。验证时可执行：

```vortexros-cli
display vxlan tunnel
display vxlan statistics source 192.0.2.1 peer 192.0.2.2 vni 1011
display bridge-domain 11
display mac-address
```

删除远端或整个NVE配置：

```text
interface Nve 1
 undo vni 1011 head-end peer-list 192.0.2.2
quit
undo interface Nve 1
commit
```

## 验证配置

```vortexros-cli
display vxlan tunnel
display vxlan statistics source 192.0.2.1 peer 192.0.2.2 vni 1011
display bridge-domain 11
```

确认 VNI 与 VTEP 一致，从两端桥域内的终端测试互通，并检查 VXLAN 收发计数。
