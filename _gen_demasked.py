#!/usr/bin/env python3.11
# -*- coding: utf-8 -*-
"""生成对外分发的「全功能脱敏版」：凭据打码 + 保留全部控制台能力。

v7.0 说明：
- 已无 license_auth / update_checker（一机一码与在线更新已在源码层移除）；
- 脱敏版（free）即为「全功能脱敏版」：所有控制台能力开放（含图片/文件原图下载），
  仅将开放平台凭据脱敏为占位符，需使用者填入自己的凭据。
"""
import json
import os
import re

SRC = "/workspace/yuanbao-v65"
OUT = "/workspace/yuanbao-v65-demasked"
os.makedirs(os.path.join(OUT, "templates"), exist_ok=True)

# ───────── 1. app_脱敏.py ─────────
with open(os.path.join(SRC, "app.py"), encoding="utf-8") as f:
    code = f.read()

# ① 打码：硬编码的默认元宝 ID
code = code.replace(
    'DEFAULT_YUANBAO_ID = "szUvRH8s4ekettawNjDREmAG4W7h+Lhb8Sy9tq/otZU="',
    'DEFAULT_YUANBAO_ID = "YOUR_YUANBAO_ID_HERE"',
)

with open(os.path.join(OUT, "app_脱敏.py"), "w", encoding="utf-8") as f:
    f.write(code)
print("已生成 app_脱敏.py")

# ───────── 2. index.html ─────────
with open(os.path.join(SRC, "templates", "index.html"), encoding="utf-8") as f:
    html = f.read()

# 兜底打码
html = html.replace('szUvRH8s4ekettawNjDREmAG4W7h+Lhb8Sy9tq/otZU=', 'YOUR_YUANBAO_ID_HERE')

with open(os.path.join(OUT, "templates", "index.html"), "w", encoding="utf-8") as f:
    f.write(html)
print("已生成 templates/index.html")

# ───────── 3. config.json ─────────
with open(os.path.join(SRC, "config.json"), encoding="utf-8") as f:
    cfg = json.load(f)
cfg["EDITION"] = "free"
cfg["ADMIN_PASSWORD_HASH"] = "0000000000000000000000000000000000000000000000000000000000000000"
cfg["ADMIN_USERNAME"] = "YOUR_ADMIN_USERNAME_HERE"
cfg["APP_KEY"] = "YOUR_APP_KEY_HERE"
cfg["APP_SECRET"] = "YOUR_APP_SECRET_HERE"
cfg["YUANBAO_ID"] = "YOUR_YUANBAO_ID_HERE"
cfg["PAN123_DOWNLOAD_URL"] = "YOUR_PAN123_DOWNLOAD_URL_HERE"
cfg["PAN123_EXTRACT_CODE"] = ""
cfg["GITHUB_TOKEN"] = ""
cfg["BOT_FORWARD_PASSWORD"] = "YOUR_BOT_FORWARD_PASSWORD_HERE"
with open(os.path.join(OUT, "config.json"), "w", encoding="utf-8") as f:
    json.dump(cfg, f, ensure_ascii=False, indent=2)
print("已生成 config.json（脱敏 free 版 = 全功能脱敏版）")

print("\n完成。输出目录：", OUT)
