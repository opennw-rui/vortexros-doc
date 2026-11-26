---
nav_title: 配置案例
---


# 配置备份、导入与启动文件 配置案例

## 操作流程

![当前运行配置 → 导出或载入配置文件 → 候选或下次启动](cases.svg)

(case-conditions-01-cli-configuration-files)=
## 配置条件

用具备权限的管理员登录，确认备份路径可写，输入文件符合当前版本的命令语法。含口令或密钥的备份按凭据材料保管。

## 配置步骤

```vortexros-cli
export configuration /tmp/backup.cfg
save maintenance.cfg
startup saved-configuration maintenance.cfg
display startup
```

需要手工回放配置时，先使用 `load configuration FILE` 查看待提交内容，确认后再执行 commit。按实际路径替换 FILE。

(case-verification-01-cli-configuration-files)=
## 验证方法

对照以下命令和预期结果核对设备状态。

```vortexros-cli
display configuration candidate
display configuration storage
display startup
```

核对待应用差异、保存位置和下次启动文件。要复查内容，可用具备权限的账户执行 display saved-configuration。
