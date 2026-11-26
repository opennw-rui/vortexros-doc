# 首次启动与管理接入

从系统盘启动后，在 Console 用安装时设置的 `vortexros` 账户和密码登录。先核对启动镜像、保存配置和已加载接口。

```text
<VortexROS> display version
<VortexROS> display startup
<VortexROS> display interface brief
<VortexROS> display ip interface brief
<VortexROS> display current-configuration
```

在独立 Console 上配置管理口地址和回程路由。按需要启用 STelnet，核对 AAA 与 VTY 权限，再从另一终端实际登录 SSH。通过后执行 `save`。首次恢复出厂或以空配置启动时，按 Console 提示更改初始口令后再配置 SSH。

[配置与保存](../operator/01-cli.md) · [AAA、SSH 与 VTY](../operator/02-system-services.md)
