---
nav_title: 配置案例
---

# 用 Compose 离线启动容器

## 操作流程

![离线镜像归档 → 原生 Docker 导入 → Compose 启动与检查](cases.svg)

(case-conditions-11-applications-installed-apps)=
## 配置条件

使用系统管理员的 Linux 维护终端。准备与设备架构一致、用 `docker save` 导出的 `busybox.tar`，归档中包含示例标签 `busybox:1.37`。

## 配置步骤

```sh
sudo systemctl start docker
sudo docker load -i /path/busybox.tar
sudo docker compose version
```

在项目目录保存以下 `compose.yaml`。需要在系统镜像切换后使用同一份 Compose 文件时，将项目放到共享持久区。

```yaml
services:
  example:
    image: busybox:1.37
    pull_policy: never
    command: ["sh", "-c", "echo ready; exec sleep 86400"]
    restart: unless-stopped
    volumes:
      - data:/data
volumes:
  data:
```

```sh
sudo docker compose up -d
```

(case-verification-11-applications-installed-apps)=
## 验证方法

```sh
sudo docker compose ps
sudo docker compose logs --no-log-prefix example
```

`ps` 的 `STATUS` 应显示 `Up`，日志应含 `ready`。执行 `sudo docker compose down` 可停止并移除本项目的容器，命名卷继续保留。
