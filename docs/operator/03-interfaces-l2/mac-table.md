---
nav_title: MAC 地址表
nav_overview: 介绍
nav_feature: true
---


(section-operator-03-interfaces-l2-mac-table-1)=
# MAC 地址表

<span id="overview"></span>

通过 MAC 地址表确认设备把流量转发到哪个端口，也可调整动态表项的老化时间。

<span id="principles"></span>

(section-operator-03-interfaces-l2-mac-table-2)=
## 工作原理

交换设备根据入帧源 MAC 在该 VLAN 或桥域学习端口。后续用目的 MAC 查表决定出口。老化、迁移和显式删除会改变动态项。静态项由配置维护，查询应同时核对域和学习位置。

按桥域转发的 MAC 表可显示动态学习与静态条目。可全局调整动态 MAC 老化时间。

<span id="examples"></span>

(section-operator-03-interfaces-l2-mac-table-3)=
## 配置与验证

(case-conditions-03-interfaces-l2-mac-table)=
### 配置条件

在已经可以收发流量的 VLAN 上观察动态学习。全局老化时间调整会影响已有 VLAN。

```{toctree}
:maxdepth: 1

mac-table/cases/example-1
mac-table/cases/example-2
```

(case-verification-03-interfaces-l2-mac-table)=
### 通用验证

```vortexros-cli
display mac-address
display current-configuration | include aging-time
```

检查动态表项的 VLAN、MAC 和出接口。停止指定终端的流量后，可观察表项何时从列表中移除。

<span id="observed"></span>

实测节选中的物理接口按文档端口编号记为 EthernetX。其他表项保留原始验证值。

(recorded-result-03-interfaces-l2-mac-table)=
### 精确查询的实测回显

测试设备在 VLAN 200 配置静态 MAC 后执行精确查询。命中时只有一项，查询未配置的地址时总数为 0。

```text
<VortexROS> display mac-address 0200-0011-0402
-------------------------------------------------------------------------------
MAC Address       VLAN/VSI/BD                    Learned-From        Type
-------------------------------------------------------------------------------
0200-0011-0402    200/-/-                        Ethernet3           static
-------------------------------------------------------------------------------
Total items displayed = 1
```

<span id="precautions"></span>

(section-operator-03-interfaces-l2-mac-table-4)=
## 注意事项

静态 MAC 的出接口必须实际属于相应桥域。迁移固定终端时需同步更新静态表项。

<p data-legacy-id="id1" class="manual-previous-section" data-section-moved><a href="#overview">介绍</a></p>
<p data-legacy-id="id2" class="manual-previous-section" data-section-moved><a href="#case-conditions-03-interfaces-l2-mac-table">配置准备</a></p>
<p data-legacy-id="id3" class="manual-previous-section" data-section-moved><a href="#examples">配置案例</a></p>
<p data-legacy-id="id5" class="manual-previous-section" data-section-moved><a href="#case-verification-03-interfaces-l2-mac-table">验证配置</a></p>
<p data-legacy-id="id4" class="manual-previous-section" data-section-moved><a href="cases/example-2/">配置静态 MAC 表项</a></p>
