# 应用桥、出口与端口发布

## 功能介绍

应用可通过隔离的双栈桥互通。需要访问外部服务或向指定来源发布端口时，可单独配置受管出口策略。

## 配置准备

准备独立应用卷、支持应用桥的签名应用，以及在默认路由表可达的上联。先创建桥，再安装和启动使用该桥的应用。

## 配置案例

```sh
sudo vortexros-image app bridge-create 192.0.2.0/24 2001:db8:400::/64 1420
sudo vortexros-image app bridge-status
```

在维护 shell 可使用 `app bridge-policy /path/policy.json` 设置受管策略。下例仅允许指定 HTTPS 目标、指定 DNS，并发布一个端口。应用必须使用与 target 一致的固定地址。

```json
{
  "uplink": "Ethernet2",
  "dns": [
    "198.51.100.2"
  ],
  "allow": [
    {
      "destination": "198.51.100.2/32",
      "protocol": "tcp",
      "port": 443
    }
  ],
  "publish": [
    {
      "application": "probe",
      "protocol": "tcp",
      "listen": "198.51.100.1:8443",
      "target": "192.0.2.10:443",
      "from": [
        "198.51.100.0/25"
      ]
    }
  ],
  "advertise": false
}
```

要撤销出口、端口发布及显式通告，执行 `sudo vortexros-image app bridge-policy-clear`。要删除桥，请先停止并移除使用该桥的应用。

## 验证配置

```vortexros-cli
display ip routing-table
display ipv6 routing-table
```

使用 app bridge-status 查看桥与策略。从应用和管理站分别测试允许和拒绝的流量。当 advertise 为 true 时，核对桥前缀是否按配置通告；清除策略后确认通告撤销。
