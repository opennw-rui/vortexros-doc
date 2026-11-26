# DHCPv4 客户端

## 功能介绍

在上联动态取得 IPv4 地址、租约与路由，适用于由上游网络分配地址的接口。

## 配置准备

选择能够到达上游 DHCP 服务器的三层接口。DNS 租约不修改设备的本机 DNS 解析设置。

## 配置案例

```text
interface Ethernet 1
 ip address dhcp-alloc
commit
display dhcp client
```

客户端只接收和维护IPv4地址、默认路由、classless route及租约生命周期。撤销：

```text
interface Ethernet 1
 undo ip address dhcp-alloc
commit
```

默认会安装DHCP学习到的默认路由，默认优先级为60。可以调整优先级，或显式禁止默认路由：

```text
interface Ethernet 1
 dhcp client default-route preference 80
 # 如不需要上游默认路由：
 undo dhcp client default-route enable
```

当无类静态路由选项有效时，设备优先使用其中的路由。关闭默认路由安装只影响租约中的 /0。

## 验证配置

```vortexros-cli
display dhcp client
display ip interface brief
display ip routing-table
```

检查租约有效期和接口地址，按配置核对默认路由或上游发布的具体前缀。
