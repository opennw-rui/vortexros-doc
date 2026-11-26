# EVPN

按业务目标选择 EVPN 功能。动态 VXLAN 负责发现远端 VTEP 和学习二层端点，Type-5 承载租户 IP 前缀，多归属让客户网段同时接入两台 PE，Vbdif 网关通告发布网关的 MAC/IP。

```{toctree}
:maxdepth: 1

/operator/06-tunnels/vxlan-evpn
/operator/06-tunnels/evpn-type5
/operator/06-tunnels/evpn-multihoming
/operator/06-tunnels/evpn-gateway
```

配置前先确认 VTEP 间的底层 IP 可达性。接入口和 VNI 的映射参见 [Bridge Domain](../03-interfaces-l2/bridge-domain.md)。
