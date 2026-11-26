# 重启与关机

## 功能介绍

系统管理员可在用户视图重启设备或关机。操作会中断所有服务与连接。

## 配置准备

安排维护窗口，准备能观察开机或恢复供电的独立控制台。若要保留已提交配置，先执行 save。

## 配置案例

以下为重启示例，按 CLI 提示完成确认。若需停止系统且由现场恢复电源，则使用 `poweroff`。

```vortexros-cli
save
display startup
reboot
```

## 验证配置

```vortexros-cli
display version
display startup
display health
```

重启后确认启动了预期镜像，设备管理和业务能够恢复。关机完成后从 Console 或设备电源状态确认结果。
