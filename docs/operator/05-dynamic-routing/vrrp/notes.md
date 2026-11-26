---
nav_title: 注意事项
---


# VRRP 与 VRRP6 网关冗余 注意事项

两端需使用相同 VRID、版本和虚拟地址，真实地址应互不冲突。单播 IPv6 peer 配真实链路本地地址。切换测试应从终端观察实际转发。

## 修改和删除

```text
interface Vlanif 100
 undo vrrp vrid 10 track interface Vlanif 200
 undo vrrp vrid 10 priority
 undo vrrp vrid 10 timer advertise
 undo vrrp vrid 10 virtual-ip 10.100.0.254
 undo vrrp vrid 10
```

`undo priority`恢复100，`undo timer advertise`恢复1秒，`undo preempt-mode`恢复抢占。`undo vrrp vrid 10`删除整个IPv4组；IPv6使用对应的 `undo vrrp6 vrid 20 ...`。
