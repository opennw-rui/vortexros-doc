# 受管应用与隔离网络

具备受管应用组件、应用公钥及独立数据卷的系统，可在本机维护环境安装签名的离线应用包。准备独立的 VROS-APPS 数据卷后，由系统管理员显式启用运行时。

```sh
sudo vortexros-image docker-enable
sudo vortexros-image app install /path/app-bundle.tar
sudo vortexros-image app list
sudo vortexros-image app start app-name
sudo vortexros-image app status app-name
sudo vortexros-image app logs app-name
```

把示例路径与应用名换成实际值。安装会验证签名、镜像架构和载荷完整性，然后创建应用。容器需显式启动。用 `app stop` 停止应用，确认已停后可用 `app remove` 删除容器。同名应用重新安装时会使用原有的应用数据卷。

默认应用没有网络。为已签名声明使用应用桥的容器创建隔离双栈桥。桥上的应用可以互通，外部出口通过显式策略配置。

```sh
sudo vortexros-image app bridge-create 192.0.2.0/24 2001:db8:400::/64 1420
sudo vortexros-image app bridge-status
```

带受管出口的应用桥在创建时接收策略文件。策略可指定上联、DNS 服务器、允许的目标和端口，以及从明确来源访问的端口发布。部署后分别验证获准和被拒连接。清除策略会撤销出口、发布和显式路由通告，保留应用与桥。先停止并移除仍引用该桥的容器，再执行 `app bridge-remove`。

[系统与访问管理](02-system-services.md) · [运行检查](09-operations.md)
