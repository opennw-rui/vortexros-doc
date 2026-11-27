---
nav_title: NAT 地址与端口转换
nav_overview: 介绍
nav_feature: true
---


(section-operator-07-policy-nat-1)=
# NAT 地址与端口转换

<span id="overview"></span>

NAT 可将源或目的地址和端口映射到其他值，适用于内网出口或受控的服务访问。

<span id="principles"></span>

(section-operator-07-policy-nat-2)=
## 工作原理

源 NAT 改写源地址或端口，目的 NAT 改写目的地址或端口。会话型转换还需正确处理返回流。除了配置和策略命中计数，应在对端或线上确认实际看到的地址、端口及回包。

支持源地址转换、PAT、目标转换与回流。统计可按策略或规则启用，会话可按原始五元组查询。

<span id="examples"></span>

(section-operator-07-policy-nat-3)=
## 配置与验证

(case-conditions-07-policy-nat)=
### 配置条件

规划内外网接口、地址池和规则顺序。确认地址池的回程能到达设备。

```{toctree}
:maxdepth: 1

nat/cases/example-1
nat/cases/outbound-pat
```

(case-verification-07-policy-nat)=
### 通用验证

```vortexros-cli
display nat-policy configuration
display nat-policy statistics
display nat-policy sessions
```

发起匹配业务后，预期命中规则的计数增加，连接建立时可看到会话的原始与转换后地址、端口。源转换时从目的端确认看到的源值。目的转换时从服务端确认报文到达实际监听地址和端口。另用一条不命中该规则的流量核对边界。

<span id="observed"></span>

(recorded-result-07-policy-nat)=
### 实际 TCP 会话中的源地址与端口转换

GRE 上的组合策略验证中，客户端原始源为 203.0.113.99:57029，PAT 后在隧道内的目的端看到源为 192.0.2.2:19942。目的 192.0.2.1:18551 保持不变。TCP 会话建立后验证了撤销与恢复。

<span id="precautions"></span>

(section-operator-07-policy-nat-4)=
## 注意事项

确保转换地址有回程。规则变更后要用新连接检查；已有会话可能继续使用之前的映射。

<p data-legacy-id="id1" class="manual-previous-section" data-section-moved><a href="#overview">介绍</a></p>
<p data-legacy-id="id2" class="manual-previous-section" data-section-moved><a href="#case-conditions-07-policy-nat">配置准备</a></p>
<p data-legacy-id="id3" class="manual-previous-section" data-section-moved><a href="#examples">配置案例</a></p>
<p data-legacy-id="id4" class="manual-previous-section" data-section-moved><a href="#case-verification-07-policy-nat">验证配置</a></p>
<p data-legacy-id="pat" class="manual-previous-section" data-section-moved><a href="cases/outbound-pat/">用地址池做出方向 PAT</a></p>
