---
nav_title: 802.1Q 与 QinQ 三层子接口
nav_overview: 介绍
nav_feature: true
---


(section-operator-03-interfaces-l2-subinterfaces-1)=
# 802.1Q 与 QinQ 三层子接口

<span id="overview"></span>

三层子接口按 802.1Q 标签区分共用物理链路的多个网段。QinQ 用外层和内层标签共同区分业务。

<span id="principles"></span>

(section-operator-03-interfaces-l2-subinterfaces-2)=
## 工作原理

多个带标签的业务可共用一条物理链路。收包时按封装标记选择子接口，之后按该子接口的二层桥域或三层配置处理。选错标签通常表现为父口已 up，但预期子接口没有收到业务。

子接口实例编号与标签独立。三层子接口终结标签，二层子接口按配置匹配帧并接入桥域。

<span id="examples"></span>

(section-operator-03-interfaces-l2-subinterfaces-3)=
## 配置与验证

(case-conditions-03-interfaces-l2-subinterfaces)=
### 配置条件

确保父接口按三层模式工作。对端须发送与相应子接口匹配的单标签或双标签。

```{toctree}
:maxdepth: 1

subinterfaces/cases/example-1
subinterfaces/cases/example-2
subinterfaces/cases/example-3
```

(case-verification-03-interfaces-l2-subinterfaces)=
### 通用验证

```vortexros-cli
display interface Ethernet 1.100
display interface Ethernet 1.200
display ip routing-table protocol direct
```

核对两个子接口的状态和直连路由。分别从两种标签的对端发包，确认流量经对应子接口进入。

<span id="observed"></span>

实测节选中的物理接口按文档端口编号记为 EthernetX。其他表项保留原始验证值。

(recorded-result-03-interfaces-l2-subinterfaces)=
### 运行查询实测节选

r4 同一物理链路上的三个子接口。前两项的协议已就绪，第三项 PHY 已 up 而 Proto 为 down。以下只保留表头和三个子接口。

```text
<VortexROS> display interface brief
Interface               PHY    Proto   InUti  OutUti  CRC    Type          MTU
Ethernet1.310           up     up       0.0%    0.0%   --    SubInterface  9000
Ethernet1.320           up     up       0.0%    0.0%   --    SubInterface  1500
Ethernet1.321           up     down     0.0%    0.0%   --    SubInterface  1500
```

<span id="precautions"></span>

(section-operator-03-interfaces-l2-subinterfaces-4)=
## 注意事项

核对两端标签和端口模式。多内层或 any 匹配时须显式配置需要的标签改写方式。

<p data-legacy-id="id1" class="manual-previous-section" data-section-moved><a href="#overview">介绍</a></p>
<p data-legacy-id="id2" class="manual-previous-section" data-section-moved><a href="#case-conditions-03-interfaces-l2-subinterfaces">配置准备</a></p>
<p data-legacy-id="id3" class="manual-previous-section" data-section-moved><a href="#examples">配置案例</a></p>
<p data-legacy-id="id4" class="manual-previous-section" data-section-moved><a href="#case-verification-03-interfaces-l2-subinterfaces">验证配置</a></p>
<p data-legacy-id="q" class="manual-previous-section" data-section-moved><a href="cases/example-2/">两端的 802.1Q 三层子接口</a></p>
<p data-legacy-id="qinq" class="manual-previous-section" data-section-moved><a href="cases/example-3/">灵活 QinQ 二层接入</a></p>
