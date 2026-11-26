---
nav_title: 配置案例
nav_overview: 案例索引
---


# 静态 VXLAN 配置案例

(case-conditions-06-tunnels-vxlan-static)=
## 配置条件

两端 VTEP 的底层地址彼此可达，启用相应的桥域和数据面。选择相同 VNI，并规划每端本地接入口。

为两台设备规划可达的 VTEP 地址，预建相同的 VNI 与本地桥域。

```{toctree}
:maxdepth: 1

cases/example-1
cases/two-vteps
```

(case-verification-06-tunnels-vxlan-static)=
## 通用验证

```vortexros-cli
display vxlan tunnel
display vxlan statistics source 192.0.2.1 peer 192.0.2.2 vni 1011
display bridge-domain 11
```

确认 VNI 与 VTEP 一致，从两端桥域内的终端测试互通，并检查 VXLAN 收发计数。
