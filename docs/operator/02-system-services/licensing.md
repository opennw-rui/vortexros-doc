---
nav_title: 离线设备授权
nav_overview: 介绍
nav_feature: true
---


(section-operator-02-system-services-licensing-1)=
# 离线设备授权

<span id="overview"></span>

设备管理员可以导出授权申请文件并导入与本机匹配的授权文件。适用于不直接接入签发服务的设备。

<span id="principles"></span>

(section-operator-02-system-services-licensing-2)=
## 工作原理

设备可导出与本机绑定的申请，导入签名授权后可查询状态及有效期。

<span id="examples"></span>

(section-operator-02-system-services-licensing-3)=
## 配置与验证

(section-operator-02-system-services-licensing-4)=
### 操作流程

![待授权设备 → 离线申请与签发 → 同一台设备](licensing/cases.svg)

(case-conditions-02-system-services-licensing)=
### 配置条件

使用具备权限的管理账户。准备可在本机读写的文件路径，保留现有设备配置。

(section-operator-02-system-services-licensing-5)=
### 配置步骤

```vortexros-cli
license request export
```

命令会打印 `/vortexros/license/vortexros-<Node ID>.vreq` 的实际路径。Node ID 是设备的授权编号，可以通过 `display license` 核对。也可以指定 `license request export router01.vreq`，或填写有写入权限的绝对路径。省略文件后缀时会补齐 `.vreq`。重复导出时，使用一个新的文件名可保留之前的请求。

取得该申请对应的 `.vlic` 授权文件后，将它放入设备并导入。

```vortexros-cli
license import router01.vlic
```

(case-verification-02-system-services-licensing)=
### 验证方法

对照以下命令和预期结果核对设备状态。

```vortexros-cli
display license
```

核对设备当前的授权状态与有效期。申请和授权文件名以实际路径为准。

显式指定无后缀的文件名 `manual-request` 时，实测导出路径以 `manual-request.vreq` 结尾。自动导出的文件名包含本机 `display license` 所示的完整 Node ID。再次执行自动导出会报告文件已存在。

<span id="observed"></span>

(r4-result-operator-02-system-services-licensing)=
### 内置试用授权的实测回显

r4 空盘首启的授权状态节选。active 和已启用的 Configuration access 表示当前可以修改配置。其余信息及有效期以本机查询为准。

```text
<VortexROS> display license
License status       : active
License type         : trial
License ID           : built-in-trial
Binding              : software-host-bound
Configuration access : enabled
```

<span id="precautions"></span>

(section-operator-02-system-services-licensing-6)=
## 注意事项

申请文件和授权文件分别交给对应设备。验收时记录授权状态，避免将不同设备的文件混用。

<p data-legacy-id="id2" class="manual-previous-section" data-section-moved><a href="#overview">介绍</a></p>
<p data-legacy-id="id3" class="manual-previous-section" data-section-moved><a href="#case-conditions-02-system-services-licensing">配置准备</a></p>
<p data-legacy-id="id4" class="manual-previous-section" data-section-moved><a href="#examples">配置案例</a></p>
<p data-legacy-id="id5" class="manual-previous-section" data-section-moved><a href="#case-verification-02-system-services-licensing">验证配置</a></p>
