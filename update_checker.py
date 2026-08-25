# -*- coding: utf-8 -*-
"""
更新检查器（Update Checker）
================================
- 读取「更新源」：默认本地 updates/version.json；也可配置为远程 URL（开源版由作者自行托管）
- 与当前版本比较，判断是否可更新
- 自动抓取（auto-grab）：把新版本 files 列表中的文件从更新源复制到项目根目录（原地覆盖）

对外开源版用法
--------------
1. 作者把更新包（例如 app.py、templates/index.html 等）放进某个可公开访问的目录，
   并放一份 version.json（version 高于用户当前版本）。
2. 在开源构建里把 UPDATE_SOURCE 指向该 version.json 的 URL。
3. 用户在控制台「检查更新」→ 发现新版本 → 完成在线认证（一机一码）→ 点「立即更新」，
   控制台自动抓取文件并原地重启。
"""
import os
import json
import shutil

try:
    import requests
    _HAS_REQUESTS = True
except Exception:
    _HAS_REQUESTS = False

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPDATES_DIR = os.path.join(BASE_DIR, 'updates')
CURRENT_VERSION = '6.7.0'

# 更新源：本地清单文件（默认）；开源版可改为远程 URL（在 config.json 中设置 UPDATE_SOURCE）
LOCAL_MANIFEST = os.path.join(UPDATES_DIR, 'version.json')


def get_current_version() -> str:
    return CURRENT_VERSION


def _parse(v: str):
    try:
        return tuple(int(x) for x in str(v).split('.'))
    except Exception:
        return (0,)


def _fetch_manifest(source: str):
    """返回 (manifest_dict, error_or_None)"""
    source = source or LOCAL_MANIFEST
    if source.startswith('http://') or source.startswith('https://'):
        if not _HAS_REQUESTS:
            return None, 'no_requests_lib'
        try:
            r = requests.get(source, timeout=15)
            r.raise_for_status()
            return r.json(), None
        except Exception as e:
            return None, str(e)
    if os.path.isfile(source):
        try:
            with open(source, 'r', encoding='utf-8') as f:
                return json.load(f), None
        except Exception as e:
            return None, str(e)
    return None, 'no_manifest'


def check_update(source: str = None) -> dict:
    """检查更新，返回结构化信息"""
    m, err = _fetch_manifest(source)
    if m is None:
        return {
            'has_update': False,
            'current': CURRENT_VERSION,
            'error': err or 'no_manifest',
        }
    latest = str(m.get('version', '0.0.0'))
    has = _parse(latest) > _parse(CURRENT_VERSION)
    return {
        'has_update': has,
        'current': CURRENT_VERSION,
        'latest': latest,
        'release_name': m.get('release_name', ''),
        'released_at': m.get('released_at', ''),
        'changelog': m.get('changelog', ''),
        'require_auth': bool(m.get('require_auth', True)),
        'files': m.get('files', []),
        'min_version': m.get('min_version', '0.0.0'),
        'source': source or LOCAL_MANIFEST,
    }


def apply_update(manifest=None, source_dir: str = None) -> list:
    """自动抓取：将 manifest.files 列出的文件复制到项目目录（原地覆盖）

    manifest 可为 dict（直接传清单），或 str（指向清单路径/URL）。
    返回实际成功复制的相对路径列表。
    """
    if isinstance(manifest, str):
        m, _ = _fetch_manifest(manifest)
    elif isinstance(manifest, dict):
        m = manifest
    else:
        m = None
    if not m:
        return []
    files = m.get('files', [])
    src_root = source_dir or UPDATES_DIR
    base = BASE_DIR
    applied = []
    for rel in files:
        src = os.path.join(src_root, rel)
        dst = os.path.join(base, rel)
        if not os.path.isfile(src):
            continue
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)
        applied.append(rel)
    return applied


if __name__ == '__main__':
    print('当前版本 :', get_current_version())
    print('检查结果 :', check_update())
