---
nav_title: 设备名称与登录提示
nav_overview: 介绍
nav_feature: true
---


(section-operator-02-system-services-identity-1)=
# 设备名称与登录提示

<span id="overview"></span>

设备名称用于区分不同站点和角色的设备。设置后，CLI 提示符会显示新名称，便于运维人员确认当前会话。

<span id="principles"></span>

(section-operator-02-system-services-identity-2)=
## 工作原理

sysname 设置设备名称，常用于识别终端提示符和运维记录。

<span id="examples"></span>

(section-operator-02-system-services-identity-3)=
## 配置与验证

(section-operator-02-system-services-identity-4)=
### 操作流程

![系统视图 → 设备名称 → 新的管理会话](identity/cases.svg)

(case-conditions-02-system-services-identity)=
### 配置条件

按站点和角色选用设备名称。下例使用 EDGE-01，可替换为实际名称。

(section-operator-02-system-services-identity-5)=
### 配置步骤

在系统视图输入以下配置并提交。

```vortexros-config
sysname EDGE-01
#
return
```

如果原会话还显示旧提示符，可开启新会话查看。确认后执行 `save`。

(case-verification-02-system-services-identity)=
### 验证方法

对照以下命令和预期结果核对设备状态。

```vortexros-cli
display current-configuration | include sysname
display version
```

检查配置中是否为 `sysname EDGE-01`，并从新会话核对 CLI 提示符。修改名称时重复同样步骤。

<span id="observed"></span>

(closeout-result-operator-02-system-services-identity)=
### 首启时的设备名称回显

空盘安装后默认设备名称为 VortexROS。用 `System name` 核对设备名称。另用 `display startup` 核对本次运行的具体系统镜像。

```text
<VortexROS> display version
VortexROS software, Version 0.1.0-dev
Copyright (C) 2026 VortexROS Project. All rights reserved.

System
  System name         : VortexROS
  Kernel              : Linux 7.3.6 x86_64
  Architecture        : amd64
```

<span id="precautions"></span>

(section-operator-02-system-services-identity-6)=
## 注意事项

使用便于区分站点和设备角色的名称。已有会话仍显示旧提示时，重新登录确认，再保存。

<p data-legacy-id="id2" class="manual-previous-section" data-section-moved><a href="#overview">介绍</a></p>
<p data-legacy-id="id3" class="manual-previous-section" data-section-moved><a href="#case-conditions-02-system-services-identity">配置准备</a></p>
<p data-legacy-id="id4" class="manual-previous-section" data-section-moved><a href="#examples">配置案例</a></p>
<p data-legacy-id="id5" class="manual-previous-section" data-section-moved><a href="#case-verification-02-system-services-identity">验证配置</a></p>
