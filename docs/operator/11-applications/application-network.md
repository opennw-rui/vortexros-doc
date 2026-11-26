---
nav_title: Docker 网络与端口发布
nav_overview: 介绍
nav_feature: true
---


(section-operator-11-applications-application-network-1)=
# Docker 网络与端口发布

<span id="overview"></span>

Docker 提供原生网络驱动、地址配置与端口发布。VortexROS 默认关闭 Docker 的 IPv4 和 IPv6 防火墙规则管理。管理员可配置主机规则，也可按地址族启用 Docker 自己的规则。

<span id="principles"></span>

(section-operator-11-applications-application-network-2)=
## 工作原理

使用 `docker network` 或 Compose 的 `networks` 定义容器桥和子网。使用 Docker 端口发布参数或 Compose 的 `ports` 配置服务监听地址和端口。

<span id="examples"></span>

(section-operator-11-applications-application-network-3)=
## 配置与验证

(case-conditions-11-applications-application-network)=
### 配置条件

在 Linux 维护终端启动 Docker。准备案例使用的容器镜像。

```{toctree}
:maxdepth: 1

application-network/cases/example-1
application-network/cases/example-2
```

(case-verification-11-applications-application-network)=
### 通用验证

```sh
sudo docker network ls
sudo docker ps
```

使用网络列表核对容器网络，使用容器列表核对容器状态和发布端口。实际网络和服务连通性按各案例验证。

<span id="observed"></span>

(recorded-result-11-applications-application-network)=
### 容器双栈与防火墙的实测结果

开发镜像验证了原生 Docker 网络上的容器双栈互通。IPv4 和 IPv6 的 Docker 防火墙默认关闭，按需要打开两项配置后，分别核对了对应地址族的规则和转发行为。

<span id="precautions"></span>

(section-operator-11-applications-application-network-4)=
## 注意事项

为容器选择与现有业务和管理网段不重叠的子网。默认关闭 Docker 的 `iptables` 和 `ip6tables` 时，容器出网 NAT、入口访问控制和端口发布的转发规则由管理员配置。启用 Docker 规则后，按实际地址族检查端口可达范围。

<p data-legacy-id="id2" class="manual-previous-section" data-section-moved><a href="#overview">介绍</a></p>
<p data-legacy-id="id3" class="manual-previous-section" data-section-moved><a href="#case-conditions-11-applications-application-network">配置准备</a></p>
<p data-legacy-id="id4" class="manual-previous-section" data-section-moved><a href="#examples">配置案例</a></p>
<p data-legacy-id="id6" class="manual-previous-section" data-section-moved><a href="#case-verification-11-applications-application-network">验证配置</a></p>
<p data-legacy-id="id5" class="manual-previous-section" data-section-moved><a href="cases/example-2/">用 Compose 发布容器端口</a></p>
