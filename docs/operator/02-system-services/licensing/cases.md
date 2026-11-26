---
nav_title: 配置案例
---


# 离线设备授权 配置案例

## 操作流程

![待授权设备 → 离线申请与签发 → 同一台设备](cases.svg)

(case-conditions-02-system-services-licensing)=
## 配置条件

使用具备权限的管理账户。准备可在本机读写的文件路径，保留现有设备配置。

## 配置步骤

```vortexros-cli
license request export /tmp/device-request.bin
```

取得该申请对应的授权文件后，将它放入设备并导入。

```vortexros-cli
license import /tmp/device-license.bin
```

(case-verification-02-system-services-licensing)=
## 验证方法

对照以下命令和预期结果核对设备状态。

```vortexros-cli
display license
```

核对设备当前的授权状态与有效期。申请和授权文件名以实际路径为准。
