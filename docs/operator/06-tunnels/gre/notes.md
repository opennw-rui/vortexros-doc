---
nav_title: 注意事项
---


# GRE Tunnel 注意事项

- 源地址和目的地址须使用同一底层路由表。底层 VPN 与 Tunnel 接口承载内层业务所用的 VPN 可分别选择。
- 两端的 GRE key 应一致。对称修改或撤销 key 后，用内层双向流量验证。
- 外层 IPv4 MTU 为 1500、使用 GRE key 且无其他额外封装时，内层 MTU 可设为 1472。实际路径 MTU 更小时应相应调小。
- 删除前先移除指向 Tunnel1 的静态路由和协议、策略引用。在系统视图执行 `undo interface Tunnel 1` 并提交，再检查接口及相关直连路由。
