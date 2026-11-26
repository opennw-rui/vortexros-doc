---
nav_title: 静态 VXLAN
nav_overview: 介绍
nav_feature: true
---


(section-operator-06-tunnels-vxlan-static-1)=
# 静态 VXLAN

<span id="overview"></span>

VXLAN 在 IP 网络上延伸二层业务。静态模式从 NVE 手动指定远端 VTEP，适用于远端固定的部署。

<span id="principles"></span>

(section-operator-06-tunnels-vxlan-static-2)=
## 工作原理

静态 VXLAN 依赖显式 VTEP 对端列表和一致的 VNI。报文在入端桥域进入隧道，到达对端后按相同 VNI 映射至对应桥域。检查 NVE 源、VNI 与对端可达性，再验证远端 MAC 学习和实际帧。

NVE 指定本端 VTEP 地址，并为每个 VNI 配置远端 VTEP 列表。发送广播、未知单播或组播时，本端向该 VNI 中的静态对端复制报文。用 `display vxlan tunnel` 查看实际隧道，用 `display vxlan statistics` 查看对应 VNI 和对端的收发量。

<span id="examples"></span>

(section-operator-06-tunnels-vxlan-static-3)=
## 配置与验证

(case-conditions-06-tunnels-vxlan-static)=
### 配置条件

两端 VTEP 的底层地址彼此可达，启用相应的桥域和数据面。选择相同 VNI，并规划每端本地接入口。

为两台设备规划可达的 VTEP 地址，预建相同的 VNI 与本地桥域。

```{toctree}
:maxdepth: 1

vxlan-static/cases/example-1
vxlan-static/cases/two-vteps
```

(case-verification-06-tunnels-vxlan-static)=
### 通用验证

```vortexros-cli
display vxlan tunnel
display vxlan statistics source 192.0.2.1 peer 192.0.2.2 vni 1011
display bridge-domain 11
```

确认 VNI 与 VTEP 一致，从两端桥域内的终端测试互通，并检查 VXLAN 收发计数。

<span id="observed"></span>

(recorded-result-06-tunnels-vxlan-static)=
### 运行查询实测节选

r4 静态 VXLAN 的实际查询。检查本地源 VTEP 和对端 VTEP，再从业务网段验证实际报文。

```text
<VortexROS> display vxlan tunnel
Tunnel ID   Source                                    Destination                               State     Type
----------------------------------------------------------------------------------------------------------------
23          10.201.12.1                               10.201.23.3                               up        static
----------------------------------------------------------------------------------------------------------------
 Number of vxlan tunnel :
 Total: 1    Static: 1    L2 dynamic: 0    L3 dynamic: 0    Unmanaged: 0
```

<span id="precautions"></span>

(section-operator-06-tunnels-vxlan-static-4)=
## 注意事项

静态对端列表应双向配置。先保证底层可达和 MTU 足够，再检查同 VNI 的桥域成员。删除整个 NVE 前确认没有其他 VNI 依赖它。

<p data-legacy-id="id1" class="manual-previous-section" data-section-moved><a href="#overview">介绍</a></p>
<p data-legacy-id="id2" class="manual-previous-section" data-section-moved><a href="#principles">功能特性</a></p>
<p data-legacy-id="id3" class="manual-previous-section" data-section-moved><a href="#examples">配置案例</a></p>
<p data-legacy-id="id5" class="manual-previous-section" data-section-moved><a href="#case-verification-06-tunnels-vxlan-static">验证配置</a></p>
<p data-legacy-id="id4" class="manual-previous-section" data-section-moved><a href="cases/example-1/">为已有桥域添加一个静态对端</a></p>
<p data-legacy-id="vtep" class="manual-previous-section" data-section-moved><a href="cases/two-vteps/">两个 VTEP 的静态二层互通</a></p>
