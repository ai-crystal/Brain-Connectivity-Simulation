#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""发布前体检：检查链接、图片、PDF 页数与 README 是否一致。"""

import json
import re
import sys
from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parents[2]
BOOKS = ROOT / "books"
MD_LINK = re.compile(r"(?<!\!)\[[^\]]*\]\(([^)\s]+)(?:\s+'[^']*')?\)")
IMG_LINK = re.compile(r"!\[[^\]]*\]\(([^)\s]+)\)")

errors = []


def check_md(path: Path):
    text = path.read_text(encoding="utf-8")
    for m in IMG_LINK.finditer(text):
        src = m.group(1)
        if src.startswith("http"):
            continue
        target = (path.parent / src).resolve()
        if not target.exists():
            errors.append(f"{path.relative_to(ROOT)} 图片不存在：{src}")
    for m in MD_LINK.finditer(text):
        link = m.group(1)
        if link.startswith("http") or link.startswith("#"):
            continue
        link = link.split("#")[0]
        if not link.endswith(".md"):
            if link.endswith(".pdf"):
                if link.startswith("/"):
                    target = (ROOT / link.lstrip("/")).resolve()
                else:
                    target = (path.parent / link).resolve()
                if not target.exists():
                    errors.append(f"{path.relative_to(ROOT)} PDF 链接不存在：{link}")
            continue
        if link.startswith("/"):
            target = (ROOT / link.lstrip("/")).resolve()
        else:
            target = (path.parent / link).resolve()
        if not target.exists():
            errors.append(f"{path.relative_to(ROOT)} 链接不存在：{link}")


def check_sidebar(path: Path):
    text = path.read_text(encoding="utf-8")
    for m in re.finditer(r"\]\((/[^)\s]+)", text):
        link = m.group(1).lstrip("/")
        if not (ROOT / link).exists():
            errors.append(f"{path.relative_to(ROOT)} 侧栏链接不存在：{link}")


def main():
    for md in ROOT.rglob("*.md"):
        if any(part.startswith(".") for part in md.relative_to(ROOT).parts):
            continue
        if md == ROOT / "papers":
            continue
        check_md(md)
        if md.name == "_sidebar.md":
            check_sidebar(md)

    for book in (BOOKS / "intro", BOOKS / "theory"):
        for name in ("README.md", "_sidebar.md", "book.json", "structure.json"):
            if not (book / name).exists():
                errors.append(f"{book.name} 缺少 {name}")
        meta = json.loads((book / "book.json").read_text(encoding="utf-8"))
        pdf = ROOT / "output" / meta["pdf"]
        if not pdf.exists():
            errors.append(f"缺少 PDF：{meta['pdf']}")
            continue
        with pymupdf.open(pdf) as doc:
            pages = doc.page_count
        readme = (book / "README.md").read_text(encoding="utf-8")
        m = re.search(r"共\s*\d+\s*章\s*·\s*(\d+)\s*页", readme)
        if not m or int(m.group(1)) != pages:
            errors.append(f"{book.name} 首页页数与 PDF 不一致（PDF {pages} 页）")

    if errors:
        print("体检未通过：")
        for e in errors:
            print(" -", e)
        sys.exit(1)
    print("全部通过")


if __name__ == "__main__":
    main()
