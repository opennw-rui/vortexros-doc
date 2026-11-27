---
nav_feature: true
---

# 脱敏支持包与加密备份

选择要交付的数据。排查软件版本或服务时序时导出脱敏支持包。需要保存设备配置和身份材料时，使用接收者证书导出加密备份。

## 工作原理

| 产物 | 内容 | 适用场景 |
| --- | --- | --- |
| 脱敏支持包 | 软件镜像台账和当前启动的受管服务时间线，时间线保留 UTC 时间、服务分类和级别。 | 核对升级进度或服务事件顺序。 |
| 加密设备备份 | 已选定的启动配置原文、设备身份和已有的密钥与授权状态。 | 由持有对应私钥的管理员在离线环境核验备份。 |

加密备份读取设备当前选定的已保存启动配置。要把正在运行的配置纳入备份，先确认启动文件选择，按需执行 `save`。

## 操作与验证

### 导出支持包

以系统管理员身份进入 Linux 维护终端。在 Console 救援中，完成认证后也可直接运行 `support-bundle support-01.tar.gz`。

```sh
sudo vortexros-image support-bundle support-01.tar.gz
sudo ls -l /vortexros/install/support-01.tar.gz
sudo tar -tzf /vortexros/install/support-01.tar.gz
```

预期文件权限为 `0600`。开发版实测归档只有 `system.json` 和 `journal-timeline.txt` 两项。同名文件已经存在时，另选文件名。提交给协助排查的人前，可以查看两项内容，确认需要的时间段和镜像信息齐全。

(encrypted-device-backup)=
### 导出并离线验证加密设备备份

在离线管理机准备 RSA 公钥证书，将证书 `recipient.pem` 放入设备的 `/vortexros/install/`。对应私钥留在管理机。先在设备 CLI 执行 `display startup`，核对 `Next startup saved-configuration file`。

```sh
sudo vortexros-image secure-backup branch-gateway.tar.cms recipient.pem
sudo ls -l /vortexros/install/branch-gateway.tar.cms
```

将 CMS 文件拷回受控管理机。在该管理机的 shell 解密并列出归档内容。

```sh
openssl cms -decrypt -binary -inform DER \
  -in branch-gateway.tar.cms -recip recipient.pem -inkey recipient.key \
  -out branch-gateway.tar
tar -tf branch-gateway.tar
```

预期存在 `startup.cfg` 和 `identity/machine-id`。配置加密密钥、SSH 主机密钥和授权条目按设备实际状态出现。验证后按保管要求处理解密后的文件。救援入口使用 `secure-backup branch-gateway.tar.cms recipient.pem`，两个参数仍使用上述安装目录内的文件名。

## 注意事项

系统软件回退、导入设备配置和恢复备份是不同的操作。配置导入见[配置备份、导入与启动文件](../01-cli/configuration-files.md)，系统不可用时见[通过控制台进入救援](../../installation/system-recovery.md)。备份中的授权仍按实际设备身份校验。
