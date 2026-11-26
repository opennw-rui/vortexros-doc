# 访问控制、QoS 与 NAT

- [ACL 访问控制](07-policy/acl.md)。ACL 按地址、协议及端口匹配报文。接口引用 ACL 后可限制访问，也可在流量策略中复用相同的匹配规则。
- [接口 QoS 限速](07-policy/interface-qos.md)。接口 QoS 对指定方向的业务限速，适用于按链路容量限制流量。
- [MQC 分类、流量策略与重定向](07-policy/mqc.md)。MQC 将匹配、动作和应用位置分开。可按业务流分类，对匹配报文限速、重标记或重定向。
- [TCP MSS 调整](07-policy/tcp-mss.md)。当三层路径中存在封装开销时，TCP MSS 调整可限制握手协商的报文段大小。
- [NAT 地址与端口转换](07-policy/nat.md)。NAT 可将源或目的地址和端口映射到其他值，适用于内网出口或受控的服务访问。

```{toctree}
:maxdepth: 1
:hidden:

07-policy/acl
07-policy/interface-qos
07-policy/mqc
07-policy/tcp-mss
07-policy/nat
```
