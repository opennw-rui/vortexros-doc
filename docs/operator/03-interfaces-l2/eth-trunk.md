---
nav_title: Eth-Trunk 链路聚合
nav_overview: 介绍
nav_feature: true
---


(section-operator-03-interfaces-l2-eth-trunk-1)=
# Eth-Trunk 链路聚合

<span id="overview"></span>

将多条 Ethernet 链路合为一条逻辑接口，可增加可用带宽并承受单链路故障。可按对端选择手工聚合或 LACP。

<span id="principles"></span>

(section-operator-03-interfaces-l2-eth-trunk-2)=
## 工作原理

手工聚合依赖两端一致的成员和模式。LACP 通过周期性交互判断哪些成员可参与收发。聚合成员变化后先看可用成员，再用跨对端流量验证聚合仍可转发。单条流量的速率还受它所选成员链路限制。

支持手工聚合和 LACP。成员集中归属于聚合口，接口简表将成员显示在 Eth-Trunk 项下。

<span id="examples"></span>

(section-operator-03-interfaces-l2-eth-trunk-3)=
## 配置与验证

(case-conditions-03-interfaces-l2-eth-trunk)=
### 配置条件

示例使用 Ethernet1 和 Ethernet2。先移除成员上独立的二三层业务配置，并确保对端采用相同模式及 MTU。

```{toctree}
:maxdepth: 1

eth-trunk/cases/example-1
eth-trunk/cases/example-2
```

(case-verification-03-interfaces-l2-eth-trunk)=
### 通用验证

```vortexros-cli
display eth-trunk 10
display interface brief
```

确认成员状态符合预期。检查 Eth-Trunk10 及其成员，再断开一根链路验证剩余成员是否仍能转发。

<span id="observed"></span>

(recorded-result-03-interfaces-l2-eth-trunk)=
(r4-result-operator-03-interfaces-l2-eth-trunk)=
### 成员加入、迁移和退出时的实测回显

三个配置步骤在 r4 逐次核对，成员加入 Eth-Trunk10 后缩进显示在该组下面。迁至 Eth-Trunk11 后只在新组下出现，撤销时恢复为独立行。下面的对照只检查本机显示和成员关系，未在对端完成 LACP，聚合口读回 down。

```text
<VortexROS> display interface brief
Interface               PHY    Proto   InUti  OutUti  CRC    Type          MTU
Eth-Trunk10             down   down     0.0%    0.0%   --    bond          1500
  host-p1a12            up     up       0.0%    0.0%   --    AF-Packet     1500
  host-p1b12            up     up       0.0%    0.0%   --    AF-Packet     1500
```

(lab-result-operator-03-interfaces-l2-eth-trunk)=
### 双端聚合进入转发状态后的实测回显

两台设备都启用静态 LACP，聚合端口实际 Up，两条成员处于 Selected。实测断开一条成员后仍能转发，恢复链路后两条成员重新入组。以下为首端节选。

```text
<P1> display eth-trunk 10
Eth-Trunk10's state information is:
Local:
LAG ID: 10                  WorkingMode: STATIC
System Priority: 65535      System ID: 02fe-c51c-ad7d
Operate status: up          Number Of Up Port In Trunk: 2
--------------------------------------------------------------------------------
ActorPortName          Status   PortPri PortNo PortKey PortState Weight
host-p1a12             Selected 255     1      31      00111111  1
host-p1b12             Selected 255     2      31      00111111  1
```

<span id="precautions"></span>

(section-operator-03-interfaces-l2-eth-trunk-4)=
## 注意事项

两端采用匹配的聚合模式和 MTU。成员退出聚合后才可以单独配置二层或三层属性。

<p data-legacy-id="id1" class="manual-previous-section" data-section-moved><a href="#overview">介绍</a></p>
<p data-legacy-id="id2" class="manual-previous-section" data-section-moved><a href="#case-conditions-03-interfaces-l2-eth-trunk">配置准备</a></p>
<p data-legacy-id="id3" class="manual-previous-section" data-section-moved><a href="#examples">配置案例</a></p>
<p data-legacy-id="id4" class="manual-previous-section" data-section-moved><a href="#case-verification-03-interfaces-l2-eth-trunk">验证配置</a></p>
<p data-legacy-id="lacp" class="manual-previous-section" data-section-moved><a href="cases/example-2/">两台设备双链路 LACP</a></p>
