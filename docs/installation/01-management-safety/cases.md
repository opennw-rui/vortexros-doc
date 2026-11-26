---
nav_title: 配置案例
---


# 管理通道与控制台 配置案例

## 拓扑

![本地 Console → 待管理设备 → 独立 SSH 终端](cases.svg)

(case-conditions-installation-01-management-safety)=
## 配置条件

已有本地显示、键盘或可见 GRUB 的串口，准备一个独立终端用于测试。

## 配置步骤

Live GRUB 提供串口和本地显示两个入口，约 10 秒后进入默认选项。本地显示使用已接入的显示器和键盘。选串口时，终端速率默认 115200，常用设置为 8N1。

安装器显示检测到的控制台，并让用户选择是否在已安装系统中启用串口。首次冷启动应从实际选定的控制台登录。升级、数据面重置、管理链路迁移和恢复出厂期间保留一条独立控制台。

在另一个会话验证新管理路径能够登录，再撤销旧路径。使用 `display users` 确认 Console 与 SSH 会话，使用 `display ssh user login-info` 查看认证结果。

[首次启动](../06-first-start.md) · [系统与访问管理](../../operator/02-system-services.md)

(case-verification-installation-01-management-safety)=
## 验证方法

对照以下命令和预期结果核对设备状态。

从计划保留的 Console 登录后运行 `display users`。SSH 新会话也应可登录，并在 `display ssh user login-info` 出现相应记录。
