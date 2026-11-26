---
nav_title: 配置案例
---


# 签名镜像升级 配置案例

## 操作流程

![设备及签名 TAR → 验签和试启动 → 确认版本和业务](cases.svg)

(case-conditions-installation-software-upgrade)=
## 配置条件

准备与设备架构相符的签名 TAR 和独立 Console。保存已生效的配置，将 TAR 放入 `/vortexros/install/`。下列 `IMAGE.tar` 应替换为实际文件名，可用问号和 Tab 补齐。

## 配置步骤

```vortexros-cli
save
check system-software IMAGE.tar
startup system-software IMAGE.tar
display system-software operation
display startup
```

在准备作业完成、确认下次启动镜像正确后，执行 `reboot`。要在重启前取消，用 `undo startup system-software`。

(case-verification-installation-software-upgrade)=
## 验证方法

对照以下命令和预期结果核对设备状态。

```vortexros-cli
display version
display startup
display system-software operation
display health
```

核对本次和默认启动的镜像，确认操作已完成，再测试管理连接与相关业务。若试启动未成功，通过 Console 检查设备选回的镜像与启动配置。
