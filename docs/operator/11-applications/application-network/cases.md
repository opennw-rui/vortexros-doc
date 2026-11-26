---
nav_title: 配置案例
nav_overview: 案例索引
---


# Docker 网络与端口发布 配置案例

(case-conditions-11-applications-application-network)=
## 配置条件

在 Linux 维护终端启动 Docker。准备案例使用的容器镜像。

```{toctree}
:maxdepth: 1

cases/example-1
cases/example-2
```

(case-verification-11-applications-application-network)=
## 通用验证

```sh
sudo docker network ls
sudo docker ps
```

使用网络列表核对容器网络，使用容器列表核对容器状态和发布端口。实际网络和服务连通性按各案例验证。
