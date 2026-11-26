# 签名镜像升级

## 功能介绍

设备可以在维护窗口试启动一份签名镜像。确认成功后，新镜像成为默认启动镜像，上一份确认镜像会保留为后备。

## 配置准备

准备与设备架构相符的签名 TAR 和独立 Console。保存已生效的配置，将 TAR 放入 `/vortexros/install/`。下列 `IMAGE.tar` 应替换为实际文件名，可用问号和 Tab 补齐。

## 配置案例

```vortexros-cli
save
check system-software IMAGE.tar
startup system-software IMAGE.tar
display system-software operation
display startup
```

在准备作业完成、确认下次启动镜像正确后，执行 `reboot`。要在重启前取消，用 `undo startup system-software`。

## 验证配置

```vortexros-cli
display version
display startup
display system-software operation
display health
```

核对本次和默认启动的镜像，确认操作已完成，再测试管理连接与相关业务。若试启动未成功，通过 Console 检查设备选回的镜像与启动配置。
