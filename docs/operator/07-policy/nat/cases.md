---
nav_title: 配置案例
nav_overview: 案例索引
---


# NAT 地址与端口转换 配置案例

(case-conditions-07-policy-nat)=
## 配置条件

规划内外网接口、地址池和规则顺序。确认地址池的回程能到达设备。

```{toctree}
:maxdepth: 1

cases/example-1
cases/outbound-pat
```

(case-verification-07-policy-nat)=
## 通用验证

```vortexros-cli
display nat-policy configuration
display nat-policy statistics
display nat-policy sessions
```

发起匹配业务并检查命中计数、映射和双向连接，另用不命中规则的流量核对其处理结果。
