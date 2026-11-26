# 离线安装与管理应用

## 功能介绍

可从签名离线包安装应用，并单独启动、停止、查看和删除。应用数据存放在独立应用卷。

## 配置准备

使用系统管理员的本机维护 shell，准备 VROS-APPS 数据卷和有效的签名包。

## 配置案例

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

## 验证配置

```vortexros-cli
display service
display health
```

在维护 shell 使用 `sudo vortexros-image app list` 和 `sudo vortexros-image app status app-name` 核对应用实际状态。用 app logs 查看应用日志。
