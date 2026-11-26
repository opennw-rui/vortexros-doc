---
nav_title: 配置案例
---


# 重启与关机 配置案例

## 操作流程

![系统管理员 → 保存配置并重启 → Console 与业务检查](cases.svg)

(case-conditions-09-operations-power)=
## 配置条件

安排维护窗口，准备能观察开机或恢复供电的独立控制台。若要保留已提交配置，先执行 save。

## 配置步骤

以下为重启示例，按 CLI 提示完成确认。若需停止系统且由现场恢复电源，则使用 `poweroff`。

```vortexros-cli
save
display startup
reboot
```

(case-verification-09-operations-power)=
## 验证方法

对照以下命令和预期结果核对设备状态。

```vortexros-cli
display version
display startup
display health
```

重启后确认启动了预期镜像，设备管理和业务能够恢复。关机完成后从 Console 或设备电源状态确认结果。
