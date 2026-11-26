# SSH 公钥认证

## 功能介绍

将用户的 OpenSSH 公钥导入设备并按名称关联到账户，适用于管理终端的免口令公钥认证。

## 配置准备

准备客户端公钥文件，并确认 STelnet 已可用。只复制 .pub 文件内容。

## 配置案例

在系统视图输入 `rsa peer-public-key workstation encoding-type openssh`。进入命名视图后执行 `public-key-code begin`，在下一行粘贴本机的 OpenSSH 公钥整行或 Base64 数据。执行 `public-key-code end` 完成录入，`peer-public-key end` 返回系统视图。

```text
ssh user vortexros assign rsa-key workstation
commit
return
display aaa user vortexros
```

Ed25519 使用 `ed25519 peer-public-key` 和 `assign ed25519-key`。撤销时用 `undo ssh user vortexros assign rsa-key workstation`，提交后从独立会话验证相应密钥已经失效。

## 验证配置

```vortexros-cli
display aaa user vortexros
display ssh user vortexros login-info succeeded
display ssh user vortexros login-info failed
```

从客户端使用与 workstation 公钥配对的私钥发起新会话，检查对应用户出现在成功记录中。撤销后先从独立会话复验。

[STelnet 与 VTY](stelnet.md)
