# 元宝Bot插件满血v8.0内测版 · 手机 Termux 部署指南

> 适用对象：想在 Android 手机上用 **Termux（终端模拟器）** 自托管「元宝Bot插件满血v8.0内测版」的用户。
> 内部测试版 zip 已内置真实开放平台凭据与登录密码，解压即可运行；全功能脱敏版 zip 需先填入你自己的开放平台凭据。

---

## 一、前言

本版本（v8.0）为全功能控制台：圆形 tab 栏、重写后的毛玻璃消息面板、动画输入框、统一设计语言。已移除厂商动态光影、在线更新、一机一码验证。
本指南带你把分发包在手机上跑起来，并长期后台存活。

---

## 二、准备工作

1. **安装 Termux**
   - 强烈建议从 **F-Droid** 安装（Google Play 上的 Termux 已停止维护、版本过旧）：
     `https://f-droid.org/packages/com.termux/`
   - 打开后先授权存储：`termux-setup-storage`（弹窗点「允许」）
2. **可选增强组件**
   - `Termux:Widget`：桌面一键启动脚本
   - `Termux:Boot`：开机自启
3. **网络**：手机需能访问外网（控制台要连 `wss://bot-wss.yuanbao.tencent.com`）

---

## 三、安装系统依赖

```bash
pkg update && pkg upgrade -y
pkg install -y python python3-pip git nodejs openssl openssl-tool
```

验证版本：

```bash
python3 --version
node --version
npm --version
```

> ⚠️ 注意：Termux 里的 Python 命令是 `python3`（指向 3.11）。若 `start.sh` 里的 `python3.11` 报错找不到命令，
> 把 `start.sh` 第一行 `PY=${PY:-python3.11}` 改成 `PY=${PY:-python3}` 即可。

---

## 四、把项目传到手机

**方式 A：直接用本包（推荐）**
把分发包（如 `元宝Bot插件满血v8.0内测版.zip`）通过数据线 / 网盘 / 文件传输助手传到手机存储，在 Termux 里解压：

```bash
cd /storage/downloads
unzip 元宝Bot插件满血v8.0内测版.zip -d ~/
cd ~/元宝Bot插件满血v8.0内测版
```

**方式 B：git clone（走代码仓库时）**

```bash
cd ~
git clone <你的仓库地址> yuanbao
cd yuanbao
```

---

## 五、安装依赖

Python 依赖：

```bash
pip install --upgrade pip
pip install flask requests
```

Node 依赖（bot-forward 转发服务，**可选**，不启转发可跳过）：

```bash
cd bot-forward
npm install
cd ..
```

---

## 六、配置 config.json

用 Termux 自带编辑器修改：`nano config.json` 或 `vim config.json`。关键字段：

| 字段 | 说明 |
|------|------|
| `PORT` | 监听端口，默认 `5000` |
| `EDITION` | 内部测试版保持 `internal_beta`；全功能脱敏版为 `free`（默认即为全功能） |
| `ADMIN_USERNAME` / `ADMIN_PASSWORD_HASH` | 控制台登录用户名与密码哈希 |
| `APP_KEY` / `APP_SECRET` / `YUANBAO_ID` | 元宝派开放平台凭据（内部版已内置真实值；脱敏版需填入你自己的） |
| `DEFAULT_GROUP_CODE` | 默认监听群号 |
| `BOT_FORWARD_PASSWORD` | bot-forward 转发服务密码 |

登录地址：`http://localhost:5000/login`

---

## 七、启动

**方式 1：前台调试**

```bash
python3.11 app_脱敏.py
```

**方式 2：自带启动脚本（含依赖自检 + 健康检查）**

```bash
bash start.sh
```

**方式 3：后台常驻（推荐，配合 keepalive 自愈）**

```bash
nohup bash start.sh >/dev/null 2>&1 &
nohup bash keepalive.sh >/dev/null 2>&1 &
```

`keepalive.sh` 每 5 秒检查进程，挂了自动拉起（基于 PID 锁，不会重复拉起多个）。

---

## 八、保持后台存活（关键，否则 Android 会杀进程）

1. **电池优化**：手机 `设置 → 应用 → Termux → 电池 → 设为「不受限制 / 不允许省电」`
2. **唤醒锁**：Termux 内执行 `termux-wake-lock`（屏幕熄灭也保持运行；`termux-wake-unlock` 释放）
3. **开机自启**（需安装 Termux:Boot）：

```bash
mkdir -p ~/.termux/boot
cat > ~/.termux/boot/start-yuanbao.sh <<'EOF'
#!/data/data/com.termux/files/usr/bin/sh
termux-wake-lock
cd ~/元宝Bot插件满血v8.0内测版
bash start.sh &
bash keepalive.sh &
EOF
chmod +x ~/.termux/boot/start-yuanbao.sh
```

---

## 九、访问方式

- **手机本机**：浏览器打开 `http://localhost:5000` 或 `http://127.0.0.1:5000`
- **同 WiFi 局域网**：其他设备访问 `http://<手机局域网IP>:5000`
  查 IP：`ip addr show wlan0 | grep inet`
- **公网访问**：用内网穿透把 5000 端口暴露出去，例如：

```bash
# Cloudflare Tunnel（无需自有域名）
pkg install -y cloudflared
cloudflared tunnel --url http://localhost:5000
```

> ⚠️ 一旦暴露公网，**务必保留登录闸并改成强密码**，避免被他人进入控制台。

---

## 十、故障排查

| 现象 | 处理 |
|------|------|
| `ModuleNotFoundError` | 重新 `pip install flask requests` |
| 端口被占用 | 改 `config.json` 的 `PORT`，或 `pkill -f app_脱敏.py` |
| 看运行日志 | `tail -f logs/start.log` |
| 连不上元宝派 | 检查 `APP_KEY/APP_SECRET/YUANBAO_ID`；手机网络是否可达 `wss` |
| 进程反复重启 | 看 `logs/keepalive.log` 与 `logs/auto_restart.log` |

---

## 十一、安全提醒

本内部测试版 zip **内置真实开放平台凭据与登录密码**，仅供你本人手机自托管使用，
**请勿公开发布或转发给无关人员**。任何对外传播、商业使用均违反版权声明（见 `LICENSE`）。
