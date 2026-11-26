---
nav_title: 配置案例
---


# 回退与删除系统镜像 配置案例

## 操作流程

![当前运行镜像 → 选择后备镜像并重启 → 登录和业务复核](cases.svg)

(case-conditions-installation-software-rollback)=
## 配置条件

安排维护窗口并保存当前配置，准备可用的 Console。若 `Backup system software` 为 `NULL`，表示当前没有后备镜像。

## 配置步骤

```vortexros-cli
display system-software
startup system-software backup
display startup
```

确认回退目标后执行 `reboot`。若选择另一份可用的已确认镜像，使用 `startup system-software installed IMAGE-ID`。核对角色后，可用 `delete system-software IMAGE-ID` 删除不再使用的镜像。

(case-verification-installation-software-rollback)=
## 验证方法

对照以下命令和预期结果核对设备状态。

```vortexros-cli
display version
display startup
display system-software
display health
```

确认设备运行目标版本并加载预期的业务配置。重新测试管理登录、关键协议邻居和业务流量；删除镜像后从清单核对结果。
