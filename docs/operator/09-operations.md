# 诊断、清理、健康与服务恢复

## Ping、tracert与mtr

```vortexros-cli
ping 192.0.2.1
ping -vpn-instance BLUE 10.0.0.1
tracert 198.51.100.1
mtr -vpn-instance BLUE 10.0.0.1
```

普通和带VPN的命令都会边执行边显示结果。Ctrl+C只中止当前诊断命令，并尽量显示已经产生的统计信息，不会关闭SSH会话。错误消息保留诊断含义，但不会暴露系统中的程序路径。

`mtr`在CLI中保持交互式刷新和按键控制，但用户不能借此进入Linux shell。

## Display

推荐从摘要逐级深入：

```vortexros-cli
display service verbose
display health verbose
display alarm active
display interface brief
display ip routing-table
display current-configuration
```

命令错误只显示一次错误位置和原因，不重复回显整条命令，也不会附加与用户无关的内部读取错误。

自动化安装、升级和发布验收必须使用严格健康检查，而不是把 systemd
`READY=1` 或 `display health` 的可读输出当作已经收敛：

```vortexros-cli
health check --wait --timeout 2m --json
```

该命令仅在 Running/Actual generation一致、reconcile为`in-sync`、没有活动告警且所有必需VPP API组可用时返回0。`--timeout`会自动启用等待；超时或未收敛返回非零。`--json`只输出一次最终快照，适合作为安装程序的稳定接口。

## Clear与Reset

- `clear`清理计数、动态表项或当前Candidate；
- `reset`执行服务重启、远端列表刷新或协议会话重置；
- 二者都是即时运维命令，不进入配置；
- 对外部连接、路由邻居或转发有影响的操作需要管理员权限和明确确认。

示例：

```vortexros-cli
reset mac-address
clear nat-policy counters
reset service vpp
reset service bgp
reset route-static group name CDN
```

## VPP恢复

```vortexros-cli
display vpp api compatibility verbose
display vpp interface-ownership verbose
display vpp takeover transaction
reset service vpp
```

VPP接管阶段只检查核心API、startup中的全部预期物理接口及对应LCP。该门槛未通过时会恢复全部Linux接口；门槛通过后，FRR、策略或隧道等后续收敛失败只进入degraded并重试，不再回绑驱动。

## 动态路由服务恢复

动态路由服务异常时，先检查具体协议的邻居和路由，再重启最小范围的服务。重启协议服务不会修改已保存配置，服务恢复后设备会重新应用已经提交的协议配置。

```vortexros-cli
display service verbose
display ip routing-table
display ospf peer brief
display bgp peer
display bfd
```

## 告警与日志

告警显示严重度、功能模块、错误码、受影响对象、首次/最近发生时间、累计次数以及当前是否已恢复。相同故障会合并计数，避免重复信息淹没有效日志。

```vortexros-cli
display alarm active
display alarm history last 100
display logbuffer last 100
```

需要关联多个日期或引导周期时，管理员可在系统诊断环境查询原始 journal。

## 配置恢复与电源操作

在独立 Console 上确认恢复对象。`reset saved-configuration` 把当前启动文件替换为出厂配置，指定文件名时仅替换该文件。`display startup` 用于核对下次启动选择。已运行的业务配置会继续使用到重启或执行整机恢复。

`restore factory-configuration` 在确认后重置运行与启动配置，清理受管账号和服务状态，并归还数据面接口。用 Console 完成默认管理员首次改密，再重新配置管理通道。需要保存当前业务时，先导出并检查配置文件可读。

系统管理员从用户视图执行 `reboot` 或 `poweroff`，确认前安排业务窗口。软件升级和回退按[签名镜像流程](../installation/07-upgrade-uninstall.md)操作。

## 故障处理顺序

1. 保住管理连接和当前会话；
2. 记录 `display health/service/alarm`；
3. 判断是配置错误、接口/路由依赖缺失，还是相关服务未就绪；
4. 先等待当前自动恢复动作完成；
5. 再执行最小范围reset；
6. 修复待提交配置后重新commit并检查状态；
7. 业务验证通过后save。

不要直接删除 `/var/lib/vortexros`、`/run/vortexros` 或服务运行目录来“清错”，否则可能破坏自动恢复所需的信息。无法恢复时先保存display和日志信息，再按安装手册中的恢复流程处理。
