---
nav_title: MQC 分类、流量策略与重定向
nav_overview: 介绍
nav_feature: true
---


(section-operator-07-policy-mqc-1)=
# MQC 分类、流量策略与重定向

<span id="overview"></span>

MQC 将匹配、动作和应用位置分开。可按业务流分类，对匹配报文限速、重标记或重定向。

<span id="principles"></span>

(section-operator-07-policy-mqc-2)=
## 工作原理

分类器识别报文，流行为声明命中时的动作，策略负责关联二者和绑定方向。分类命中与出口可达性是两个条件。跨 VPN 重定向需在目标表中找到可用路径。

通过分类器匹配流量、行为定义动作，再将策略绑定到指定方向。支持标记、限速和 VPN 重定向。

<span id="examples"></span>

(section-operator-07-policy-mqc-3)=
## 配置与验证

(case-conditions-07-policy-mqc)=
### 配置条件

先建立案例使用的 ACL WEB-IN 和 VPN BLUE，检查目标 VPN 有正确路由。

```{toctree}
:maxdepth: 1

mqc/cases/example-1
mqc/cases/example-2
mqc/cases/example-3
```

(case-verification-07-policy-mqc)=
### 通用验证

```vortexros-cli
display traffic classifier user-defined WEB-CLASS
display traffic behavior user-defined WEB-BEHAVIOR
display traffic policy user-defined WEB-POLICY
```

检查分类条件、动作及绑定。让命中和未命中的业务分别通过设备，检查出口和限速效果。

<span id="observed"></span>

实测节选中的物理接口按文档端口编号记为 EthernetX。其他表项保留原始验证值。

(recorded-result-07-policy-mqc)=
### 运行查询实测节选

r4 实际配置的流策略名为 P123-PBR。下列回显用于核对策略关联的分类器和行为。

```text
<VortexROS> display traffic policy user-defined P123-PBR
User Defined Traffic Policy Information:
    Policy: P123-PBR
      Description:
      Step: 1
      Share-mode
      Classifier: P123-PBR Precedence: 10
        Behavior: P123-PBR
        Redirecting:
          redirect ip-nexthop 10.201.12.2 interface Ethernet0

      Classifier: default-class Precedence: 65535
        Behavior: be
        -none-
```

(section-operator-07-policy-mqc-4)=
### 重定向及分类动作的实测结果

双栈流量在指定 VPN 实例验证了缺省路由、递归和 ECMP，覆盖未命中、重启及撤销。组合流中，匹配 ACL 的报文在出口实际观察到 DSCP 46。撤销策略后，IPv6 流恢复原始 DSCP。

<span id="precautions"></span>

(section-operator-07-policy-mqc-5)=
## 注意事项

先核对匹配范围与实际入出方向。重定向时要具备目标 VPN 的路由和正确的回程。

<p data-legacy-id="id1" class="manual-previous-section" data-section-moved><a href="#overview">介绍</a></p>
<p data-legacy-id="id2" class="manual-previous-section" data-section-moved><a href="#case-conditions-07-policy-mqc">配置准备</a></p>
<p data-legacy-id="id3" class="manual-previous-section" data-section-moved><a href="#examples">配置案例</a></p>
<p data-legacy-id="id4" class="manual-previous-section" data-section-moved><a href="#case-verification-07-policy-mqc">验证配置</a></p>
<p data-legacy-id="tcp-vpn" class="manual-previous-section" data-section-moved><a href="cases/example-2/">按 TCP 端口选择 VPN 的出口</a></p>
<p data-legacy-id="tcp" class="manual-previous-section" data-section-moved><a href="cases/example-3/">标记 TCP 流量并原位修改匹配条件</a></p>
