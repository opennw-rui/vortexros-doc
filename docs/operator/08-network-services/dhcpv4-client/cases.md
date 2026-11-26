---
nav_title: 配置案例
---


# DHCPv4 客户端 配置案例

## 拓扑

![三层 DHCPv4 客户口 → 同网段 → 上游 DHCPv4 服务器](cases.svg)

(case-conditions-08-network-services-dhcpv4-client)=
## 配置条件

选择能够到达上游 DHCP 服务器的三层接口。DNS 租约不修改设备的本机 DNS 解析设置。

## 配置步骤

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

(case-verification-08-network-services-dhcpv4-client)=
## 验证方法

对照以下命令和预期结果核对设备状态。

```vortexros-cli
display dhcp client
display ip interface brief
display ip routing-table
```

检查租约有效期和接口地址，按配置核对默认路由或上游发布的具体前缀。
