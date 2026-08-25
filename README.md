# 元宝Bot插件满血v7.6 Release Preview

> 元宝派 Bot 全功能控制台 · 创作者专属发行版

本软件是面向元宝派 Bot 控制专属定制的**全功能控制台插件**，覆盖实时消息、自动回复、插件生态、AI 聊天、图片/文件预览与下载等完整能力。

---

## ⚠️ 版权与开源许可（Apache-2.0）

本项目基于创建者的原创成果，采用 **Apache License 2.0** 开源（详见根目录 `LICENSE`）。在遵守 Apache-2.0 条款的前提下，允许使用、修改、分发（含商业使用），但**必须保留原版权声明与许可声明**，并注明对代码的修改。

> 请注意：本仓库为**脱敏版**（`config.json` 中所有敏感凭据均为占位符）。请勿上传或提交含真实开放平台凭据的配置。

---

## 一、版本说明

| 版本渠道 | 说明 |
|----------|------|
| 内部测试版（`internal_beta`） | 创建者自用的全功能版本，内置真实开放平台凭据 |
| 全功能脱敏版（`free`） | **对外分发版本（本仓库）**：所有控制台能力开放使用，但凭据已脱敏为占位符，需填入你自己的开放平台凭据后运行 |
| 高级版 / 旗舰版 / 体验版 / 初级版 / 中级版 | 历史渠道版本，能力按会员体系区分 |

> **v7.6 Release Preview**：版本号全局统一升级；**脱敏版绝不自动下载群聊中的任何图片/文件到本地**——仅当用户开启「消息保存到本地」（`MSG_LOG_ENABLED`）时，才写入**纯文本**聊天记录（`logs/messages_*.log` / `.txt`），媒体文件一律不落盘。

---

## 二、部署步骤（以全功能脱敏版为例）

1. 把分发包（如 `元宝Bot插件满血v7.6脱敏版-无本地文件保存.zip`）解压到任意目录。
2. 安装依赖：
   ```bash
   pip install flask requests
   ```
3. 启动：
   ```bash
   python3 app_脱敏.py
   ```
   默认监听 `http://0.0.0.0:5000`，浏览器打开 `http://localhost:5000/login` 登录。
4. **填入你自己的凭据**：复制 `config.example.json` 为 `config.json`（或直接编辑 `config.json`），将占位符替换为你的真实开放平台凭据（见第三节）。
   > 注意：`config.json` 已被 `.gitignore` 忽略，避免真实凭据被提交到 GitHub。

---

## 三、必填配置（编辑 `config.json`）

| 字段 | 说明 |
|------|------|
| `APP_KEY` / `APP_SECRET` | 元宝派开放平台应用凭据（脱敏版为占位 `YOUR_APP_KEY_HERE`） |
| `YUANBAO_ID` | 你的元宝 ID（占位 `YOUR_YUANBAO_ID_HERE`） |
| `ADMIN_USERNAME` / `ADMIN_PASSWORD_HASH` | 控制台登录用户名与密码哈希 |
| `DEFAULT_GROUP_CODE` | 默认监听群号 |
| `BOT_FORWARD_PASSWORD` | bot-forward 转发服务密码（可选） |

> 没有开放平台凭据将无法连接元宝派。请前往元宝派开放平台申请你自己的应用。

---

## 四、手机 Termux 自托管

详见 `TERMEX部署指南.md`（手机 Termux 安装部署方式），覆盖：Termux 安装、依赖、传包解压、配置、启动、后台保活、局域网/公网访问与故障排查。

---

## 五、文件清单

| 文件 | 作用 |
|------|------|
| `app_脱敏.py` | 主程序（Flask 后端） |
| `config.json` | 配置文件（脱敏版为占位凭据） |
| `templates/index.html` | 前端主页面 |
| `templates/login.html` | 登录页 |
| `bot-forward/` | 消息转发服务（Node，可选） |
| `plugins/` | 插件生态目录 |
| `updates/version.json` | 版本清单 |
| `LICENSE` | 版权与分发声明 |
| `README.md` | 本说明 |
| `TERMEX部署指南.md` | 手机 Termux 部署指南 |
| `项目详细介绍.md` | 项目功能与架构详细介绍 |

---

© 2026 元宝Bot插件 · 创建者保留所有权利
