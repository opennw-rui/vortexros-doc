---
nav_title: 用 Compose 发布容器端口
---

# 用 Compose 发布容器端口

## 拓扑

![本机客户端通过回环发布端口访问同设备上的容器](example-2.svg)

## 配置条件

在 Linux 维护终端操作。预先加载 `busybox:1.37`，并确保本机 TCP 8080 可用。此案例使用 Docker 的原生防火墙规则管理。

## 配置步骤

在 `/etc/docker/daemon.json` 中将 `iptables` 设为 `true`。配置 Docker 的 IPv6 防火墙时，可单独启用 `ip6tables`。按设备配置保留同一文件中的其他选项。

```sh
sudo dockerd --validate --config-file=/etc/docker/daemon.json
sudo systemctl restart docker
```

在项目目录保存 `compose.yaml`。下例把发布端口绑定到 IPv4 回环地址。

```yaml
services:
  web:
    image: busybox:1.37
    pull_policy: never
    command: ["sh", "-c", "mkdir -p /www && echo ready >/www/index.html && exec httpd -f -p 8080 -h /www"]
    ports:
      - "127.0.0.1:8080:8080"
```

```sh
sudo docker compose up -d
```

## 验证方法

对照{ref}`本功能页的实测结果 <recorded-result-11-applications-application-network>`可以核对设备实际显示的字段或业务表现。不同拓扑请按本案例的地址和接口检查。

```sh
sudo docker compose port web 8080
curl -fsS http://127.0.0.1:8080/
```

第一条命令应显示 `127.0.0.1:8080`，HTTP 正文应为 `ready`。执行 `sudo docker compose down` 后，从本机再次访问该地址应无法建立连接。
