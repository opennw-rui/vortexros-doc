---
nav_title: 注意事项
---


# Docker 与 Compose 注意事项

Docker 安装后默认停用。在需要自动启动 Docker 的系统镜像上执行 `sudo systemctl enable --now docker`。系统切换会重启设备，应用按各容器的重启策略恢复。

共享数据目录保留本机最新写入。将 Compose 项目及绑定到容器的宿主目录放在共享持久区或独立数据盘。
