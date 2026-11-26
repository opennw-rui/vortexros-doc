# 验签、升级、回退与救援

## 试启动新镜像

先执行 `save`，把签名 TAR 放入 `/vortexros/install/`。在用户视图依次执行以下命令，文件名使用已有制品。可用 `?` 与 Tab 查找支持的文件。

```text
<VortexROS> check system-software IMAGE.tar
<VortexROS> startup system-software IMAGE.tar
<VortexROS> display system-software operation
<VortexROS> display startup
```

确认验签通过、准备作业完成且下一启动镜像正确。在维护窗口中执行 `reboot`。系统使用保存的配置试启动，确认成功后更新默认镜像。遇到启动失败时查看 Console，核对镜像事务和默认启动项。等待系统确认完成后，再发起下一次镜像切换。

`undo startup system-software` 撤销尚未执行的启动选择。

## 回退与删除

`display startup` 的 `Backup system software` 显示上一份确认镜像。初次安装只有一个确认镜像时显示 `NULL`。用以下命令选择后备软件并重启。

```text
<VortexROS> display system-software
<VortexROS> startup system-software backup
<VortexROS> display startup
<VortexROS> reboot
```

要选择另一份符合条件的已确认镜像，使用 `startup system-software installed IMAGE-ID`。回退后核对实际运行镜像、配置、管理连接和业务路由。用 `delete system-software IMAGE-ID` 删除不再需要的已保留镜像。运行中、默认、后备及已安排启动的镜像受保护。

## 救援

从已安装系统的 GRUB 选择本地显示或串口救援。使用与救援提示一致的入口确认配置和镜像。安装、重启和恢复出厂属于不同操作。需要保留业务配置时，应先导出并在隔离环境验证备份。

[配置恢复与运行检查](../operator/09-operations.md)

```{toctree}
:maxdepth: 1

software-upgrade
software-rollback
system-recovery
```
