---
nav_title: 静态路由组
nav_overview: 介绍
nav_feature: true
---


(section-operator-04-ip-routing-static-route-groups-1)=
# 静态路由组

<span id="overview"></span>

用一个可维护的前缀清单管理具有相同下一跳和属性的多条静态路由。可录入手工成员，也可从文件或 URL 读取。

<span id="principles"></span>

(section-operator-04-ip-routing-static-route-groups-2)=
## 工作原理

路由组负责把一组前缀导入选定的地址族和路由表。组已配置、前缀已加载、条目已进入转发各是独立检查项。使用命名组时可精确撤销该组，其它来源的前缀按各自配置继续存在。

多个 IPv4 或 IPv6 前缀可以共用下一跳和属性。成员可手工维护或从受管列表更新。

<span id="examples"></span>

(section-operator-04-ip-routing-static-route-groups-3)=
## 配置与验证

(case-conditions-04-ip-routing-static-route-groups)=
### 配置条件

提前准备源文件或 URL、下一跳和 VPN。大批量变更前准备可用的回退配置。

```{toctree}
:maxdepth: 1

static-route-groups/cases/example-1
static-route-groups/cases/example-2
static-route-groups/cases/example-3
```

(case-verification-04-ip-routing-static-route-groups)=
### 通用验证

```vortexros-cli
display route-static group name CDN verbose
display ip routing-table group name CDN verbose
```

确认组内的前缀数量、数据来源和刷新状态。检查相关路由是否使用预期的下一跳，随后测试一个新增前缀和一个已撤销前缀。

<span id="observed"></span>

(recorded-result-04-ip-routing-static-route-groups)=
(result-operator-04-ip-routing-static-route-groups)=
### 刷新、断源和撤销的实测结果

本地文件与 HTTP 来源均通过导入和刷新验证。HTTP 临时不可用时，已安装的路由继续转发。恢复来源后可继续刷新。撤销路由组绑定时，只删除该组下发的路由，普通静态路由保留。

<span id="precautions"></span>

(section-operator-04-ip-routing-static-route-groups-4)=
## 注意事项

刷新文件或 URL 前检查列表内容和大小。与现有普通路由共存时，核对下一跳、优先级和 Tag 是否兼容。

<p data-legacy-id="id2" class="manual-previous-section" data-section-moved><a href="#overview">介绍</a></p>
<p data-legacy-id="id3" class="manual-previous-section" data-section-moved><a href="#case-conditions-04-ip-routing-static-route-groups">配置准备</a></p>
<p data-legacy-id="id4" class="manual-previous-section" data-section-moved><a href="#examples">配置案例</a></p>
<p data-legacy-id="id6" class="manual-previous-section" data-section-moved><a href="#case-verification-04-ip-routing-static-route-groups">验证配置</a></p>
<p data-legacy-id="url" class="manual-previous-section" data-section-moved><a href="cases/example-2/">文件成员与URL成员</a></p>
<p data-legacy-id="id5" class="manual-previous-section" data-section-moved><a href="cases/example-3/">普通静态路由与路由组共同提供两条下一跳</a></p>
