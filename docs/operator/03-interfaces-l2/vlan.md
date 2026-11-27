---
nav_title: VLAN 二层交换
nav_overview: 介绍
nav_feature: true
---


(section-operator-03-interfaces-l2-vlan-1)=
# VLAN 二层交换

<span id="overview"></span>

VLAN 把同一台设备上的二层交换范围分开。Access 端口连接无标签终端，Trunk 端口在链路上传递指定 VLAN。

<span id="principles"></span>

(section-operator-03-interfaces-l2-vlan-2)=
## 工作原理

未打标签帧在入端按端口默认 VLAN 归类，带标签帧按标签和允许列表归类。转发只在命中的 VLAN 内查表和泛洪，出端再按端口配置决定保留或去除标签。

| 端口模式 | 适用场景 | 配置重点 |
| --- | --- | --- |
| Access | 接入发送无标签帧的终端。 | `port default vlan` 指定接入的 VLAN。 |
| Trunk | 交换机之间或与能够收发标签的设备互联。 | `port trunk allow-pass vlan` 控制放行列表。另核对两端对无标签帧的 PVID 约定。 |
| Hybrid | 同一个端口需要对部分 VLAN 保留标签、对另一部分去标签。 | 分别配置 PVID、Tagged 和 Untagged。 |

启用交换后默认 VLAN 1 存在。Trunk 默认放行 VLAN 1，可按业务要求显式撤销。低位普通 VLAN 的配置范围为 1–4094。

<span id="examples"></span>

(section-operator-03-interfaces-l2-vlan-3)=
## 配置与验证

(section-operator-03-interfaces-l2-vlan-4)=
### 拓扑

![两台交换机通过 Trunk 互联，各接一台无标签终端](vlan/cases.svg)

(case-conditions-03-interfaces-l2-vlan)=
### 配置条件

SW1 和 SW2 的 Ethernet1 互联，各自的 Ethernet2 接入一个无标签终端。终端 A 用 `192.0.2.11/24`，终端 B 用 `192.0.2.12/24`。两端都属于 VLAN 100。VLAN 200 在两台设备之间预留。

(section-operator-03-interfaces-l2-vlan-5)=
### 配置步骤

在 SW1 和 SW2 分别从用户视图输入同一组命令。

```vortexros-cli
system-view
enable switch
vlan batch 100 200
interface Ethernet 1
 portswitch
 port link-type trunk
 port trunk allow-pass vlan 100 200
 quit
interface Ethernet 2
 portswitch
 port link-type access
 port default vlan 100
 quit
commit
return
```

(case-verification-03-interfaces-l2-vlan)=
### 验证方法

```vortexros-cli
display vlan 100
display vlan 200
display mac-address vlan 100
```

`display vlan` 同时显示 VLAN 状态、MAC 学习状态、描述和端口成员。`U/D` 表示端口 up/down，`TG/UT` 表示出端带标签/不带标签。两条链路均 up 时，本案例的预期回显中应包含以下两行。

```text
-----------------------------------------------------------------
U: Up;         D: Down;         TG: Tagged;         UT: Untagged;
-----------------------------------------------------------------

VID  Type    Status  MAC-LRN  Description    Ports
-----------------------------------------------------------------
100  common  enable  enable   VLAN 100       TG:Ethernet1(U)  UT:Ethernet2(U)
200  common  enable  enable   VLAN 200       TG:Ethernet1(U)
-----------------------------------------------------------------
```

先让终端 A、B 互相 Ping，再在两台设备查询 VLAN 100 的 MAC 表。预期设备从本端 Ethernet2 学到本地终端，从 Ethernet1 学到对端终端。跨 VLAN 通信需经三层网关。

<span id="observed"></span>

实测节选中的物理接口按文档端口编号记为 EthernetX。其他表项保留原始验证值。

(section-operator-03-interfaces-l2-vlan-6)=
### 运行查询实测节选

r4 接入口划入 VLAN 200 后，查询显示该 VLAN 的状态及出端标签方式。

```text
<VortexROS> display vlan 200
--------------------------------------------------------------------------------------
U: Up;         D: Down;         TG: Tagged;         UT: Untagged;
--------------------------------------------------------------------------------------

VID    Type      Status    MAC-LRN    Description      Ports
--------------------------------------------------------------------------------------
200    common    enable    enable     VLAN 200         UT:Ethernet2(U)  Ethernet3(U)
--------------------------------------------------------------------------------------
```

### 其他配置案例

```{toctree}
:maxdepth: 1

vlan/cases/hybrid
vlan/cases/full-trunk
```

<span id="precautions"></span>

(section-operator-03-interfaces-l2-vlan-7)=
## 注意事项

检查 Trunk 两端的允许列表和本端 PVID。退出示例前，先在两端恢复原 Access 成员和 Trunk 放行列表，再移除已无其他引用的 VLAN。若要按外层服务标签承载客户 VLAN，参见 [QinQ 二层接入](qinq.md)。

<p data-legacy-id="id1" class="manual-previous-section" data-section-moved><a href="#overview">介绍</a></p>
<p data-legacy-id="id2" class="manual-previous-section" data-section-moved><a href="#case-conditions-03-interfaces-l2-vlan">配置准备</a></p>
<p data-legacy-id="id3" class="manual-previous-section" data-section-moved><a href="#examples">配置案例</a></p>
<p data-legacy-id="id4" class="manual-previous-section" data-section-moved><a href="#case-verification-03-interfaces-l2-vlan">验证配置</a></p>
