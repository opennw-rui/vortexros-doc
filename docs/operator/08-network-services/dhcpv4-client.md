---
nav_title: DHCPv4 客户端
nav_overview: 介绍
nav_feature: true
---


(section-operator-08-network-services-dhcpv4-client-1)=
# DHCPv4 客户端

<span id="overview"></span>

在上联动态取得 IPv4 地址、租约与路由，适用于由上游网络分配地址的接口。

<span id="principles"></span>

(section-operator-08-network-services-dhcpv4-client-2)=
## 工作原理

客户端在接口上主动请求租约，得到地址后按当前配置应用路由、DNS 等信息。运行状态只能说明客户端已启动，应验证确实取得租约且更新后还能通信。

从上游接收 IPv4 地址、租约及路由。是否使用上游缺省路由可单独设置。

<span id="examples"></span>

(section-operator-08-network-services-dhcpv4-client-3)=
## 配置与验证

(section-operator-08-network-services-dhcpv4-client-4)=
### 拓扑

![R1、DHCPv4 服务器 的设备互联](dhcpv4-client/cases.svg)

(case-conditions-08-network-services-dhcpv4-client)=
### 配置条件

选择能够到达上游 DHCP 服务器的三层接口。DNS 租约不修改设备的本机 DNS 解析设置。

(section-operator-08-network-services-dhcpv4-client-5)=
### 配置步骤

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
### 验证方法

对照以下命令和预期结果核对设备状态。

```vortexros-cli
display dhcp client
display ip interface brief
display ip routing-table
```

检查租约有效期和接口地址，按配置核对默认路由或上游发布的具体前缀。

<span id="observed"></span>

(section-operator-08-network-services-dhcpv4-client-6)=
### 已获得租约的实测回显

测试客户端的 Ethernet1 取得地址后，查询在同一行显示 `running` 和实际租约地址。请核对地址确实落在服务端地址池内。

```text
<VortexROS> display dhcp client interface Ethernet1

Ethernet1  IPv4            client  -             default       running  198.18.82.59/24  -
```

<span id="precautions"></span>

(section-operator-08-network-services-dhcpv4-client-7)=
## 注意事项

只在三层接口启用。测试前确认上游服务可达，将管理会话与待更改地址隔离。

<p data-legacy-id="id1" class="manual-previous-section" data-section-moved><a href="#overview">介绍</a></p>
<p data-legacy-id="id2" class="manual-previous-section" data-section-moved><a href="#case-conditions-08-network-services-dhcpv4-client">配置准备</a></p>
<p data-legacy-id="id3" class="manual-previous-section" data-section-moved><a href="#examples">配置案例</a></p>
<p data-legacy-id="id4" class="manual-previous-section" data-section-moved><a href="#case-verification-08-network-services-dhcpv4-client">验证配置</a></p>
