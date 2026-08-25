# -*- coding: utf-8 -*-
"""
在线网络认证系统 · 一机一码
================================
- 机器指纹：hostname + 主网卡 MAC + 文件系统设备号（尽量跨重启稳定）
- 30 位验证密码：数字 + 字母 + 特殊符号，由「机器指纹 + 服务端密钥」HMAC 派生
- 一机一码：同一服务端密钥下，不同机器指纹 → 不同密码；
            密码仅在本机（对应指纹）才能校验通过，拷贝到别的机器会校验失败

设计说明
--------
所谓「在线网络认证」在本实现中即控制台自身提供的 HTTP 接口
(/api/auth/*)：客户端把本机指纹发给认证服务，服务用密钥签名后返回 30 位密码；
激活时再用同一密钥校验该密码是否与本机指纹匹配。由于沙箱网络仅放行白名单域名，
无法接入外部 SaaS 鉴权，故认证服务内置于控制台（自托管），逻辑与「一机一码」完全一致。
如需接入你自己的远端鉴权，把 AUTH_SECRET 与签发逻辑放到你的服务器即可。
"""
import os
import re
import hmac
import hashlib
import random
import string
import uuid

# 服务端密钥（一机一码的核心：改了它，已下发的密码全部失效，需重新签发）
AUTH_SECRET = os.environ.get('YUANBAO_AUTH_SECRET', 'yuanbao-bot-console-v66-online-auth-2026')

# 30 位密码字符集：字母 + 数字 + 特殊符号
_CODE_ALPHABET = string.ascii_letters + string.digits + "!@#$%^&*()-_=+[]{};:,.<>?"
_SPECIALS = set("!@#$%^&*()-_=+[]{};:,.<>?")


def get_machine_fingerprint() -> str:
    """稳定的机器指纹（跨重启尽量不变）"""
    parts = []
    # 主机名
    try:
        parts.append(os.uname().nodename if hasattr(os, 'uname') else os.getenv('COMPUTERNAME', ''))
    except Exception:
        parts.append('')
    # 主网卡 MAC
    try:
        parts.append('%012x' % uuid.getnode())
    except Exception:
        parts.append('')
    # 文件系统设备号（近似硬件 ID）
    try:
        st = os.stat('/' if os.name != 'nt' else 'C:\\')
        parts.append(str(st.st_dev))
    except Exception:
        parts.append('')
    raw = '|'.join(parts)
    return hashlib.sha256(raw.encode('utf-8')).hexdigest()[:32]


def derive_code(fingerprint: str) -> str:
    """由「指纹 + 服务端密钥」派生 30 位验证密码（确定性，一机一码）"""
    if not fingerprint:
        raise ValueError('fingerprint 不能为空')
    sig = hmac.new(AUTH_SECRET.encode('utf-8'), fingerprint.encode('utf-8'),
                   hashlib.sha256).digest()
    rng = random.Random(int.from_bytes(sig, 'big'))
    code = []
    i = 0
    while len(code) < 30:
        code.append(_CODE_ALPHABET[sig[i % len(sig)] % len(_CODE_ALPHABET)])
        i += 1
    code = code[:30]
    # 强制包含 数字 / 字母 / 特殊符号
    if not any(c.isdigit() for c in code):
        code[0] = rng.choice(string.digits)
    if not any(c.isalpha() for c in code):
        code[1] = rng.choice(string.ascii_letters)
    if not any(c in _SPECIALS for c in code):
        code[2] = rng.choice(list(_SPECIALS))
    return ''.join(code)


def verify_code(code: str, fingerprint: str) -> bool:
    """校验密码是否由本机指纹签发（一机一码）"""
    if not code or len(code) != 30:
        return False
    return hmac.compare_digest(str(code), derive_code(fingerprint))


if __name__ == '__main__':
    fp = get_machine_fingerprint()
    print('本机指纹 :', fp)
    print('验证密码 :', derive_code(fp))
