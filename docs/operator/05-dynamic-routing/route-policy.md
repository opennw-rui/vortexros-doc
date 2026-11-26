---
nav_title: 前缀列表与路由策略
nav_overview: 介绍
nav_feature: true
---


(section-operator-05-dynamic-routing-route-policy-1)=
# 前缀列表与路由策略

<span id="overview"></span>

用前缀列表筛选路由，用路由策略决定接收、发布或调整属性。策略可复用于多个邻居。

<span id="principles"></span>

(section-operator-05-dynamic-routing-route-policy-2)=
## 工作原理

前缀列表先按地址与掩码长度匹配。路由策略可在匹配后接受、拒绝或设置属性，使用时必须绑定到相应协议、方向和地址族。配置完成后核对收到和最终采用的路由。

前缀列表按地址和长度匹配路由，路由策略可以拒绝路由或修改属性。IPv4、IPv6 的匹配方式分别配置。

<span id="examples"></span>

(section-operator-05-dynamic-routing-route-policy-3)=
## 配置与验证

(section-operator-05-dynamic-routing-route-policy-4)=
### 操作流程

![收到的路由前缀 → 前缀列表与策略节点 → 路由选用或通告](route-policy/cases.svg)

(case-conditions-05-dynamic-routing-route-policy)=
### 配置条件

先规划允许的地址范围和协议引用点。名称区分大小写。

(section-operator-05-dynamic-routing-route-policy-5)=
### 配置步骤

前缀列表负责匹配路由，路由策略决定允许、拒绝或修改匹配的路由。下面的策略只允许 `10.0.0.0/8` 中掩码长度为16至24的前缀，并把BGP本地优先级设为200：

```text
ip ip-prefix PL-IN index 10 permit 10.0.0.0 8 greater-equal 16 less-equal 24
route-policy RP-IN permit node 10
 if-match ip-prefix PL-IN
 apply local-preference 200
```

配置完成后，输入 `display ip ip-prefix ?`、`display route-policy ?` 或在协议中输入 `route-policy ?`，会同时显示参数说明和已经存在的对象名称。

命令关键字不区分大小写；用户定义的对象名按输入原样保存并区分大小写。例如`RP-IN`和`rp-in`是两个不同策略，引用时必须使用定义时的大小写。同一个route-policy节点只能有一个IPv4前缀列表条件和一个IPv6前缀列表条件；再次输入同地址族的`if-match`会替换原条件。需要匹配多个前缀时，应在同一个前缀列表中增加多条规则，或者使用不同的策略节点。

IPv6前缀列表和策略条件使用独立命令：

```text
ip ipv6-prefix V6-IN index 10 permit 2001:db8:: 32 greater-equal 48 less-equal 64
route-policy V6-POLICY permit node 10
 if-match ipv6 address prefix-list V6-IN
```

可使用`display ipv6 prefix V6-IN`验证IPv6列表。IPv4与IPv6列表可以同名，但引用命令明确区分地址族；旧入口`display ip ipv6-prefix`仍保留，便于已有运维脚本继续使用。

```vortexros-cli
display ip ip-prefix PL-IN
display route-policy RP-IN
display current-configuration | include PL-IN
```

删除前应先解除协议中的引用：

```text
undo route-policy RP-IN permit node 10
undo ip ip-prefix PL-IN
```

(case-verification-05-dynamic-routing-route-policy)=
### 验证方法

对照以下命令和预期结果核对设备状态。

```vortexros-cli
display ip ip-prefix PL-IN
display route-policy RP-IN
display ipv6 prefix V6-IN
```

确认前缀长度条件和策略动作正确，再查看引用该策略的协议，核对被允许和被拒绝的前缀。

<span id="observed"></span>

(section-operator-05-dynamic-routing-route-policy-6)=
### 运行查询实测节选

三节点实验中的前缀列表名为 LOOPBACKS。检查规则和掩码范围，再对照策略绑定方向及实际收到的路由。

```text
<VortexROS> display ip ip-prefix LOOPBACKS
Prefix-list LOOPBACKS
Permitted 1
Denied 0
        index: 10               permit  10.255.0.0/16 greater-equal 32 less-equal 32
```

<span id="precautions"></span>

(section-operator-05-dynamic-routing-route-policy-7)=
## 注意事项

修改节点前先查所有调用者。验证时同时检查命中和未命中的前缀；删除前先解除引用。

<p data-legacy-id="id2" class="manual-previous-section" data-section-moved><a href="#overview">介绍</a></p>
<p data-legacy-id="id3" class="manual-previous-section" data-section-moved><a href="#case-conditions-05-dynamic-routing-route-policy">配置准备</a></p>
<p data-legacy-id="id4" class="manual-previous-section" data-section-moved><a href="#examples">配置案例</a></p>
<p data-legacy-id="id5" class="manual-previous-section" data-section-moved><a href="#case-verification-05-dynamic-routing-route-policy">验证配置</a></p>
