# 离线设备授权

## 功能介绍

设备管理员可以导出授权申请文件并导入与本机匹配的授权文件。适用于不直接接入签发服务的设备。

## 配置准备

使用具备权限的管理账户。准备可在本机读写的文件路径，保留现有设备配置。

## 配置案例

```vortexros-cli
license request export /tmp/device-request.bin
```

取得该申请对应的授权文件后，将它放入设备并导入。

```vortexros-cli
license import /tmp/device-license.bin
```

## 验证配置

```vortexros-cli
display license
```

核对设备当前的授权状态与有效期。申请和授权文件名以实际路径为准。
