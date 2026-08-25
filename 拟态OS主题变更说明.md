# 拟态 OS 全场景主题 — 变更说明

## 概述

基于用户提供的 **`元宝Bot插件满血v7.0免登录脱敏版`** 原始项目，恢复了原版架构，并在其原有主题系统之上**独立新增**了一套「拟态 OS 全场景主题」（Neumorphism OS）。

原版架构（单文件 `app_脱敏.py` + 内嵌式 `templates/index.html`）的鉴权、连接、协议、QQ 厂商主题（`QQ_THEMES`）、液态玻璃、鸿蒙空间光感等**全部逻辑保持不变**。

## 恢复内容

从用户上传的 `元宝Bot插件满血v7.0免登录脱敏版.zip` 提取并覆盖：

- `app_脱敏.py`（免登录版，登录闸已 patch 为直接放行）
- `templates/index.html`（原版前端，526KB 含内嵌样式与脚本）
- `templates/login.html`、`config.json`、`bot-forward/` 等全部原版文件

重写版（`app.py` / `core/` / `web/` / `static/`）已移除，备份保留于 `/workspace/yuanbao-v65-rewritten-backup`。

## 新增：拟态 OS 全场景主题

### 设计原则

- **独立叠加层**：通过 `html[data-series="neu"]` 属性激活，不影响原厂 `QQ_THEMES` 主题逻辑
- **单一主题切换多色**：复用原版 `--primary` 派生体系，支持 6 色实时切换
- **全场景覆盖**：按钮、卡片、输入框、Tab 栏、消息气泡等全部界面元素

### 注入位置

| 类型 | 位置 | 内容 |
|------|------|------|
| CSS | 主 `<style>` 块之后，新增 `<style id="neu-os-style">` | 拟态双阴影、按压凹陷、进场动画、水波纹、卡片柔和化 |
| HTML | 设置页「🎨 主题」区块之后 | 系列切换按钮 + 多色选择网格 `#neuAccentGrid` |
| JS | 主 `<script>` 开头 | `setSeries()` / `setAccent()` / `renderNeuPanel()` / `syncNeuUI()` / `bindNeuRipple()` / `restoreNeu()` |
| 初始化 | `init()` 中 `renderThemeGrid()` 之后 | 调用 `restoreNeu()` + `renderNeuPanel()` + `bindNeuRipple(document)` + `syncNeuUI()` |

### 功能特性

1. **拟态 OS 开关**：设置页「🪨 拟态 OS / 🔘 原厂主题」一键切换
2. **6 色主色**：蓝 / 青 / 绿 / 紫 / 橙 / 粉，单击即换（`--primary` 实时派生 `--primary-hover` / `--primary-deep` / `--on-primary` / `--accent` / `--msg-self`）
3. **双阴影柔和表面**：所有卡片/面板呈凸起质感，输入框呈凹陷质感
4. **全局动画**：进场 `neu-rise` 上浮、按钮按压回弹、点击水波纹反馈
5. **明暗共存**：拟态 OS 模式下「🌓 明暗切换」独立工作，`data-theme` 与 `data-series` 互不干扰
6. **无障碍降级**：`prefers-reduced-motion` 下自动关闭动画
7. **状态持久化**：`localStorage` 保存 `neuSeries` + `neuAccent`，刷新后恢复

### 技术要点

- 修复了原版 `html.no-effect .btn { box-shadow: revert !important }` 对拟态阴影的覆盖——拟态 CSS 的 `box-shadow` 统一加 `!important` 确保生效
- 拟态 CSS 变量（`--neu-distance` / `--neu-blur` / `--neu-shadow-light` / `--neu-shadow-dark`）按 `data-theme` 明/暗自动适配

## 验证结果

通过 Playwright 真实浏览器验证（原版免登录服务器）：

| 项目 | 结果 |
|------|------|
| 初始状态（原厂主题） | ✅ `data-series=null`，标题 v7.0，QQ 芯片 24 个 |
| 拟态 OS 开启 | ✅ `data-series="neu"`，按钮/卡片双阴影生效，6 色芯片渲染 |
| 多色切换（绿/橙/紫） | ✅ `--primary` 实时变化，active 态正确 |
| 水波纹动画 | ✅ 点击生成 `.neu-ripple` 元素 |
| 明暗 + 拟态共存 | ✅ `data-theme="dark"` + `data-series="neu"` 同时生效 |
| 恢复原厂 | ✅ `data-series=null`，原厂 QQ 主题完整保留 |
| JS 语法 | ✅ `node --check` 通过 |
| Python 编译 | ✅ `py_compile app_脱敏.py` 通过 |
| 控制台错误 | ✅ 无主题相关错误 |
| API 健康检查 | ✅ `/`、`/api/health` 等均 200 |

## 使用方式

1. 启动：`python3.11 app_脱敏.py`（免登录版，直接访问 `http://localhost:5000/`）
2. 设置页 → 「🪨 拟态 OS 全场景主题」→ 点击「🪨 拟态 OS」开启
3. 选择喜欢的拟态主色，配合「🌓 明暗切换」调整明暗
4. 点击任意按钮可见水波纹反馈，全局界面呈柔和拟态质感
