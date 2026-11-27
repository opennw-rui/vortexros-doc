---
nav_title: Docker 与 Compose
nav_overview: 介绍
nav_feature: true
---


(section-operator-11-applications-installed-apps-1)=
# Docker 与 Compose

<span id="overview"></span>

系统管理员在 Linux 维护终端使用原生 `docker` 和 `docker compose` 管理容器。可通过镜像仓库拉取镜像，也可导入离线镜像归档。

<span id="principles"></span>

(section-operator-11-applications-installed-apps-2)=
## 工作原理

使用原生 Docker 命令管理镜像、容器、网络和卷。使用标准 `compose.yaml` 管理多容器应用。

切换系统镜像时保留原生 Docker 和 containerd 配置、容器、镜像和命名卷，适用于使用相同容器运行时版本和存储后端的系统镜像。

默认使用共享持久区保存 `/var/lib/docker`、`/var/lib/containerd`、`/etc/docker` 和 `/etc/containerd`。应用数据宜使用命名卷。Compose 文件和宿主机绑定挂载目录需要放在另行选定的共享存储或数据盘上。

<span id="examples"></span>

(section-operator-11-applications-installed-apps-3)=
## 配置与验证

(section-operator-11-applications-installed-apps-4)=
### 操作流程

![离线镜像归档 → 原生 Docker 导入 → Compose 启动与检查](installed-apps/cases.svg)

(case-conditions-11-applications-installed-apps)=
### 配置条件

使用系统管理员的 Linux 维护终端。准备与设备架构一致、用 `docker save` 导出的 `busybox.tar`，归档中包含示例标签 `busybox:1.37`。

(section-operator-11-applications-installed-apps-5)=
### 配置步骤

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
### 验证方法

```sh
sudo docker compose ps
sudo docker compose logs --no-log-prefix example
```

`ps` 的 `STATUS` 应显示 `Up`，日志应含 `ready`。执行 `sudo docker compose down` 可停止并移除本项目的容器，命名卷继续保留。

<span id="observed"></span>

(section-operator-11-applications-installed-apps-6)=
### 原生容器数据跨镜像切换的实测结果

签名开发镜像空盘安装后，原生 Docker 和 Compose 通过离线构建、导入及双栈通信验证。系统从 A 启动 B 再回退到 A，旧系统能读到 B 写入的命名卷数据，容器、镜像、卷和防火墙配置均保留。

<span id="precautions"></span>

(section-operator-11-applications-installed-apps-7)=
## 注意事项

Docker 安装后默认停用。在需要自动启动 Docker 的系统镜像上执行 `sudo systemctl enable --now docker`。系统切换会重启设备，应用按各容器的重启策略恢复。

共享数据目录保留本机最新写入。将 Compose 项目及绑定到容器的宿主目录放在共享持久区或独立数据盘。

切换系统镜像后，可在 Compose 项目目录执行 `sudo docker compose ps`，确认容器已按预期启动，再从应用内读取切换前的持久数据。Docker 服务是否随启动开启按系统镜像分别设置。

<p data-legacy-id="id2" class="manual-previous-section" data-section-moved><a href="#overview">介绍</a></p>
<p data-legacy-id="id3" class="manual-previous-section" data-section-moved><a href="#case-conditions-11-applications-installed-apps">配置准备</a></p>
<p data-legacy-id="id4" class="manual-previous-section" data-section-moved><a href="#examples">配置案例</a></p>
<p data-legacy-id="id5" class="manual-previous-section" data-section-moved><a href="#case-verification-11-applications-installed-apps">验证配置</a></p>
