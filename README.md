# VortexROS 用户手册

本手册适用于 VortexROS `v0.1.0-dev` 开发版。覆盖离线安装、设备配置、运行检查、签名镜像升级、回退与救援。

[在线手册](https://opennw-rui.github.io/vortexros-doc/)

- [安装、升级与救援](docs/installation/index.md)
- [操作手册](docs/operator/index.md)
- [全命令参考](docs/operator/reference/commands.md)

先把开发版部署到虚拟机或测试设备。真机启用 DPDK、改变管理接口或执行整机回退前，准备可用的独立控制台。

## 构建在线手册

```sh
python -m pip install -r docs/requirements.txt
sphinx-build -b dirhtml -W docs _site
```

GitHub Pages 从 `gh-pages` 分支发布静态输出。构建产物根目录须有 `.nojekyll`。
