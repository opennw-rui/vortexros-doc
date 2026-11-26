# 802.1Q 与 QinQ 三层子接口

## 功能介绍

三层子接口按 802.1Q 标签区分共用物理链路的多个网段。QinQ 用外层和内层标签共同区分业务。

## 配置准备

确保父接口按三层模式工作。对端须发送与相应子接口匹配的单标签或双标签。

## 配置案例

```text
interface Ethernet 1.100
 encapsulation dot1q vid 100
 ip address 10.100.0.1 255.255.255.0
```

QinQ示例：

```text
interface Ethernet 1.200
 encapsulation qinq vid 200 ce-vid 20
 ip address 10.200.20.1 255.255.255.0
```

提交后，只有标签匹配的报文进入对应子接口。父接口down时子接口随之down；父接口恢复后自动恢复。使用以下命令验证：

```vortexros-cli
display interface Ethernet 1.100
display ip interface brief
display ip routing-table protocol direct
```

## 验证配置

```vortexros-cli
display interface Ethernet 1.100
display interface Ethernet 1.200
display ip routing-table protocol direct
```

核对两个子接口的状态和直连路由。分别从两种标签的对端发包，确认流量经对应子接口进入。
