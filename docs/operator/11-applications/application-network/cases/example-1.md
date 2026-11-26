---
nav_title: 创建内部双栈网络
---

# 创建内部双栈网络

## 拓扑

![容器 box-a 与 box-b 经 Docker 内部双栈网络互通](example-1.svg)

## 配置条件

在 Linux 维护终端使用运行中的原生 Docker。预先加载包含 `busybox:1.37` 的镜像。为容器选取不与设备现有网段重叠的 IPv4 和 IPv6 子网。

## 配置步骤

```sh
sudo docker network create --driver bridge --internal --ipv6 \
  --subnet 172.25.40.0/24 --subnet fd42:40::/64 example-net
sudo docker run -d --name box-a --network example-net \
  --ip 172.25.40.10 --ip6 fd42:40::10 busybox:1.37 sleep 600
sudo docker run -d --name box-b --network example-net \
  --ip 172.25.40.11 --ip6 fd42:40::11 busybox:1.37 sleep 600
```

## 验证方法

```sh
sudo docker network inspect --format '{{.Internal}} {{.EnableIPv6}}' example-net
sudo docker exec box-a ping -c 2 172.25.40.11
sudo docker exec box-a ping6 -c 2 fd42:40::11
```

第一条命令的预期回显为 `true true`，两次 ping 应收到响应。主机防火墙控制外部访问边界。若设备默认关闭 Docker 防火墙，在要求网络隔离的部署中同时核对主机转发规则。

```sh
sudo docker stop box-a box-b
sudo docker rm box-a box-b
sudo docker network rm example-net
```
