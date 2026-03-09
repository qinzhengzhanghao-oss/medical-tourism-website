# OpenClaw 在 Windows 电脑上安装使用的超详细操作指引

> 版本说明：本文根据当前本机自带 OpenClaw 文档整理，适用于希望在 **Windows 电脑** 上安装和使用 OpenClaw 的用户。  
> 重要结论：**官方推荐在 Windows 上通过 WSL2（推荐 Ubuntu）安装 OpenClaw**，而不是直接在原生 Windows 环境中长期运行。

---

## 一、先讲结论：Windows 上应该怎么装？

OpenClaw 官方推荐方案是：

- Windows 11 / Windows 10 上先安装 **WSL2**
- 在 WSL2 里安装 **Ubuntu**
- 然后在 Ubuntu（也就是 Linux 环境）里面安装并运行 OpenClaw

这样做的原因是：

1. OpenClaw 的 CLI、Gateway、依赖工具链，与 Linux 环境兼容性更好。
2. Node、pnpm、二进制依赖、Skills 等在 Linux/WSL2 下更稳定。
3. 原生 Windows 直接运行虽然有 PowerShell 安装脚本，但官方文档明确说：**更推荐 WSL2 路线**，原生 Windows 会更容易遇到工具兼容、路径、依赖和环境变量问题。

**一句话建议：**  
如果你是正常使用用户，请按本文的 **WSL2 标准安装法** 操作。

---

## 二、安装前准备

请先确认你的电脑满足以下条件。

### 1）系统要求

建议：

- Windows 11（优先推荐）
- 或 Windows 10（支持 WSL2 的版本）

### 2）管理员权限

安装 WSL2 时，通常需要：

- 以管理员身份打开 PowerShell
- 允许系统安装组件
- 按提示重启电脑

### 3）网络要求

安装时可能需要联网下载：

- WSL 组件
- Ubuntu 发行版
- Node.js / OpenClaw 相关依赖

如果网络环境较慢，安装过程可能会比预期更久。

### 4）你将会用到的几个名词

为了后面不混乱，先理解几个概念：

- **Windows**：你平时使用的系统桌面环境
- **PowerShell**：Windows 的命令行工具
- **WSL2**：Windows Subsystem for Linux，Windows 里的 Linux 子系统
- **Ubuntu**：你将在 WSL2 中安装的 Linux 发行版
- **OpenClaw CLI**：OpenClaw 的命令行工具
- **Gateway**：OpenClaw 后台服务/网关
- **Dashboard / Control UI**：OpenClaw 的网页控制界面

---

## 三、推荐安装法：通过 WSL2 安装 OpenClaw

# 第 1 步：以管理员身份打开 PowerShell

操作方法：

1. 点击 Windows 开始菜单
2. 搜索：`PowerShell`
3. 在搜索结果中找到 **Windows PowerShell** 或 **PowerShell**
4. 右键点击它
5. 选择 **“以管理员身份运行”**

如果系统弹出权限确认窗口，请点击 **“是”**。

---

# 第 2 步：安装 WSL2

在管理员 PowerShell 中输入下面命令，然后按回车：

```powershell
wsl --install
```

如果你想明确指定 Ubuntu 版本，也可以先查看可安装发行版：

```powershell
wsl --list --online
```

然后安装指定版本，例如：

```powershell
wsl --install -d Ubuntu-24.04
```

### 这一阶段会发生什么？

系统通常会自动：

- 启用 WSL 功能
- 启用虚拟机平台
- 下载 Linux 内核组件
- 安装 Ubuntu

### 如果系统提示重启

请按提示重启电脑。  
**重启后请重新打开 Ubuntu 或 PowerShell，继续下面步骤。**

---

# 第 3 步：首次打开 Ubuntu，并创建 Linux 用户

安装完成后：

1. 点击开始菜单
2. 搜索 **Ubuntu**
3. 打开 Ubuntu

第一次启动时，系统会提示你创建一个 Linux 用户名和密码。

例如：

- 用户名：你自己起一个
- 密码：你自己设置一个

注意：

- 输入密码时，终端中**不会显示字符**，这是正常现象
- 密码请自己记住，后续执行 `sudo` 命令时会用到

---

# 第 4 步：启用 systemd（非常重要）

OpenClaw 文档明确指出：在 WSL2 中安装 Gateway 服务，**需要启用 systemd**。

请在 **Ubuntu 终端** 中执行：

```bash
sudo tee /etc/wsl.conf >/dev/null <<'EOF'
[boot]
systemd=true
EOF
```

执行后，回到 **PowerShell**（Windows 那边），输入：

```powershell
wsl --shutdown
```

这条命令的作用是：

- 完全关闭当前 WSL 实例
- 让刚才写入的 `systemd=true` 配置生效

然后：

1. 再次打开 Ubuntu
2. 输入下面命令验证：

```bash
systemctl --user status
```

### 正常结果

如果没有明显报错，说明 systemd 基本已经启用成功。

### 如果出现异常

你可以先关闭 Ubuntu，再重新执行：

```powershell
wsl --shutdown
```

然后再次打开 Ubuntu 重试。

---

# 第 5 步：安装 Node.js（建议 22 及以上）

根据 OpenClaw 文档，前置要求是：

- **Node >= 22**

有两种思路：

## 方式 A：使用 OpenClaw 官方安装脚本自动处理（更省事）

在 Ubuntu 终端里直接执行：

```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```

这个脚本会尝试：

- 检测系统
- 确保 Node.js 版本满足要求
- 安装 OpenClaw CLI
- 处理一些常见权限与依赖问题

这是最适合普通用户的方式。

## 方式 B：你已经自己装好了 Node

如果你已经在 Ubuntu 里安装好了 Node 22+，也可以后续直接执行：

```bash
npm install -g openclaw@latest
```

不过对于多数用户，仍然建议优先使用官方安装脚本。

---

# 第 6 步：安装 OpenClaw CLI

在 Ubuntu 中执行以下推荐命令：

```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```

### 这条命令会做什么？

根据本机文档，安装脚本通常会：

1. 检测当前系统（Linux / macOS / WSL）
2. 检查 Node.js 是否达到 22+
3. 默认用 npm 全局安装 OpenClaw
4. 处理 Linux 下常见的 npm 权限问题
5. 安装完成后尽力运行诊断修复

### 安装完成后如何验证？

执行：

```bash
openclaw --help
```

如果能看到帮助信息，说明 CLI 基本安装成功。

你还可以执行：

```bash
openclaw status
```

用于检查当前状态。

---

# 第 7 步：运行 OpenClaw 新手引导

官方推荐在安装完成后执行：

```bash
openclaw onboard --install-daemon
```

这是最关键的一步之一。它会帮你配置：

- 模型认证（例如 OAuth / API Key）
- Gateway 网关
- 聊天渠道（如 Telegram、Discord、WhatsApp 等）
- 工作区与初始设置
- 后台服务安装

### 为什么推荐加 `--install-daemon`？

因为这样会尽量把 OpenClaw 的后台服务一起装好，后续开机/使用更方便。

### 引导中你可能会看到什么？

通常会涉及：

1. 选择本地或远程 Gateway
2. 配置模型认证
3. 是否安装后台服务
4. 是否连接消息渠道
5. 是否写入默认配置

如果你不确定怎么选，优先按默认建议选择即可。

---

# 第 8 步：检查 Gateway 服务是否成功

安装/引导结束后，在 Ubuntu 中执行：

```bash
openclaw gateway status
```

如果服务正常，你应该能看到 Gateway 相关状态信息。

如果你想前台直接运行，也可以用：

```bash
openclaw gateway --port 18789 --verbose
```

默认情况下，Dashboard / Control UI 常见地址是：

```text
http://127.0.0.1:18789/
```

你可以在 **Windows 浏览器** 中尝试打开它。

说明：WSL2 中运行的本地服务，很多情况下 Windows 主机可以直接通过 `127.0.0.1` 访问。

---

# 第 9 步：打开 OpenClaw 控制界面

安装成功后，你可以通过以下方式访问：

## 方式 A：命令启动 Dashboard

在 Ubuntu 中执行：

```bash
openclaw dashboard
```

## 方式 B：直接在浏览器打开

在 Windows 浏览器中输入：

```text
http://127.0.0.1:18789/
```

如果你的 Gateway 已启动，这里通常就能打开控制界面。

---

# 第 10 步：做一次完整自检

官方文档给了几条很有用的检测命令。建议依次执行：

```bash
openclaw status
openclaw health
openclaw security audit --deep
```

### 这些命令分别干什么？

- `openclaw status`：查看当前总体状态
- `openclaw health`：查看健康状态、是否缺认证等
- `openclaw security audit --deep`：做更深入的安全检查

如果你后续遇到故障，官方也推荐执行：

```bash
openclaw status --all
```

这是很适合复制给别人排查问题的一份完整状态报告。

---

## 四、如果你执意要在原生 Windows PowerShell 中安装

虽然**官方更推荐 WSL2**，但 OpenClaw 也提供了 PowerShell 安装器。

### 1）先确保你有 Node.js 22+

如果没有，请先安装 Node.js。  
文档提到 Windows 常见方式包括：

- winget
- Chocolatey
- Scoop
- 手动下载安装包

### 2）在 PowerShell 中运行安装器

```powershell
iwr -useb https://openclaw.ai/install.ps1 | iex
```

### 3）如果想按 Git 方式安装

```powershell
iwr -useb https://openclaw.ai/install.ps1 | iex -InstallMethod git
```

或者指定目录：

```powershell
iwr -useb https://openclaw.ai/install.ps1 | iex -InstallMethod git -GitDir "C:\\openclaw"
```

### 4）原生 Windows 常见问题

#### 问题 A：`spawn git ENOENT`

意思通常是：**没装 Git**。

解决办法：

1. 安装 Git for Windows  
   下载地址：`https://git-scm.com/download/win`
2. 安装完后关闭 PowerShell
3. 重新打开 PowerShell
4. 再次运行安装器

#### 问题 B：`openclaw` 不是可识别的命令

这通常说明：**npm 全局安装目录没有加入 PATH 环境变量**。

常见目录是：

```text
%AppData%\npm
```

你也可以在 PowerShell 中查询：

```powershell
npm config get prefix
```

然后把对应的全局 bin 路径加入系统 PATH，再重新打开 PowerShell。

### 5）为什么仍然不推荐原生 Windows？

因为即便安装器能运行，后续在：

- 工具兼容性
- 二进制依赖
- 技能运行环境
- 脚本行为
- 路径差异

这些方面，原生 Windows 更容易出现小坑。  
所以如果你希望长期稳定使用，还是建议回到 **WSL2 方案**。

---

## 五、安装成功后的最简使用路线

如果你只是想“先用起来”，不要一开始就折腾太多渠道。

官方最短路径是：

1. 安装 OpenClaw
2. 运行：

```bash
openclaw onboard --install-daemon
```

3. 启动/确认 Gateway
4. 在浏览器打开：

```text
http://127.0.0.1:18789/
```

5. 直接用 Control UI 聊天

也就是说，**一开始并不需要先配 WhatsApp / Telegram / Discord**，你可以先通过浏览器界面确认一切正常。

---

## 六、详细排错指南

下面是安装过程中最常见的问题。

### 1）`wsl --install` 失败

可能原因：

- Windows 版本过旧
- 没有管理员权限
- 虚拟化相关组件未启用
- 公司电脑权限受限

建议处理：

1. 确认你是管理员 PowerShell
2. 先执行系统更新
3. 重启后重试
4. 如果是公司电脑，联系管理员确认 WSL / 虚拟化策略

---

### 2）Ubuntu 能打开，但 `systemctl --user status` 异常

通常是 `systemd` 还没真正生效。

请重新确认：

- `/etc/wsl.conf` 中是否写入了：

```ini
[boot]
systemd=true
```

- 是否执行了：

```powershell
wsl --shutdown
```

- 是否重新打开了 Ubuntu

---

### 3）安装脚本执行后，提示找不到 `openclaw`

这是很常见的 PATH 问题。

处理办法：

1. 先关闭当前终端
2. 重新打开 Ubuntu
3. 再执行：

```bash
openclaw --help
```

如果仍不行，再检查 Node/npm 是否正确安装。

---

### 4）`openclaw health` 提示认证未配置

这通常说明：

- 你已经安装了 OpenClaw
- 但还没有完成模型认证配置

解决办法：

- 重新运行：

```bash
openclaw onboard --install-daemon
```

然后在向导里完成 OAuth 或 API Key 等配置。

---

### 5）Gateway 启动了，但浏览器打不开页面

请逐项检查：

1. 是否真的运行了 Gateway
   ```bash
   openclaw gateway status
   ```
2. 是否监听在 18789 端口
3. 你访问的是不是：
   ```text
   http://127.0.0.1:18789/
   ```
4. 是否因为你修改过配置导致端口不同
5. 终端里是否有报错输出

如果还是不通，可以执行：

```bash
openclaw status --all
```

保留输出用于进一步排查。

---

### 6）安装渠道（如 WhatsApp / Telegram）后没有消息响应

文档提示一个非常重要的点：

- 某些私聊渠道默认需要 **配对审批**

例如文档给出的命令：

```bash
openclaw pairing list whatsapp
openclaw pairing approve whatsapp <code>
```

如果机器人看似在线但不回复，很可能是配对还没批准。

---

## 七、进阶说明：WSL2 网络与局域网访问

一般情况下，你自己在这台 Windows 电脑上使用 OpenClaw，不需要折腾这一段。

但如果你希望：

- 局域网其他设备访问 WSL 中服务
- 将 WSL 内某个端口暴露给其他机器

那就需要额外做 Windows 端口转发（`portproxy`）和防火墙规则配置。

官方文档已经给出 PowerShell 示例，核心思路是：

1. 获取当前 WSL 的 IP
2. 用 `netsh interface portproxy` 把 Windows 端口转发到 WSL 内部端口
3. 允许防火墙放行对应端口

注意：

- **WSL IP 重启后可能会变化**
- 因此转发规则有时需要刷新
- 如果你只是本机使用，通常没必要配置

---

## 八、最推荐的标准操作清单（适合新手）

如果你想要一个最稳的顺序，照下面走：

### A. 在 Windows 管理员 PowerShell 中

```powershell
wsl --install -d Ubuntu-24.04
```

重启电脑。

### B. 在 Ubuntu 中

```bash
sudo tee /etc/wsl.conf >/dev/null <<'EOF'
[boot]
systemd=true
EOF
```

### C. 回到 PowerShell 中

```powershell
wsl --shutdown
```

### D. 重新打开 Ubuntu，验证 systemd

```bash
systemctl --user status
```

### E. 在 Ubuntu 中安装 OpenClaw

```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```

### F. 执行初始化引导

```bash
openclaw onboard --install-daemon
```

### G. 检查状态

```bash
openclaw gateway status
openclaw status
openclaw health
```

### H. 浏览器打开控制界面

```text
http://127.0.0.1:18789/
```

---

## 九、给完全不懂命令行的用户的额外提醒

1. **不要跳步。** 先装 WSL，再装 Ubuntu，再启用 systemd，再装 OpenClaw。
2. **命令要在正确的位置运行。**
   - `wsl --install`：在 Windows PowerShell 中
   - `sudo tee /etc/wsl.conf ...`：在 Ubuntu 终端中
   - `curl -fsSL https://openclaw.ai/install.sh | bash`：在 Ubuntu 终端中
3. **重启和 `wsl --shutdown` 很重要。** 有些配置不重启/不关闭 WSL 就不会生效。
4. **看不懂报错时，不要乱改。** 先把报错复制保存，再针对性排查。
5. **第一次目标不是“全功能上线”，而是“先能打开控制界面并正常聊天”。**

---

## 十、安装完成后的验收标准

如果下面几项都满足，基本就算安装成功：

- 你能正常打开 Ubuntu
- 在 Ubuntu 中执行 `openclaw --help` 有结果
- `openclaw onboard --install-daemon` 已执行完成
- `openclaw gateway status` 没有明显异常
- 浏览器能打开 `http://127.0.0.1:18789/`
- 你能在 Control UI 中正常发消息并得到回复

---

## 十一、官方依据（本文整理来源）

本文依据当前本机内置 OpenClaw 文档整理，核心结论包括：

1. **Windows 推荐走 WSL2（Ubuntu）路线**
2. WSL2 中安装 Gateway 服务前，**需要启用 systemd**
3. 推荐使用：
   ```bash
   curl -fsSL https://openclaw.ai/install.sh | bash
   ```
4. 安装后建议执行：
   ```bash
   openclaw onboard --install-daemon
   ```
5. 可通过以下命令做检查：
   ```bash
   openclaw gateway status
   openclaw status
   openclaw health
   openclaw security audit --deep
   ```

参考文档来源：

- `docs/zh-CN/platforms/windows.md`
- `docs/zh-CN/install/installer.md`
- `docs/zh-CN/start/getting-started.md`

---

## 十二、如果你想要，我还可以继续帮你做这三件事

如果后面你愿意，我还能继续给你补这三类文件：

1. **一键傻瓜版**：只保留最必要步骤，适合发给小白同事
2. **带截图占位版**：每一步预留截图位置，方便你做培训文档
3. **故障排查版**：专门整理“安装失败怎么办”的 FAQ 手册

---

**文档结束。**
