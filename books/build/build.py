#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""构建单册书籍：组装 Markdown、调用 pandoc 转 Typst、再编译成 PDF。

用法：
    python books/build/build.py --book books/intro
    python books/build/build.py --book books/intro --no-pdf
    python books/build/build.py --figures
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BUILD_ROOT = ROOT / "books" / "build"
TMP_ROOT = BUILD_ROOT / ".build"
PAPERS = ROOT / "papers"


def eprint(*args):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass
    print(*args, file=sys.stderr)


# ---------- 工具 ----------

def typst_str(value: str) -> str:
    """把 Python 字符串转成 Typst 字符串字面量。"""
    s = str(value).replace("\\", "\\\\").replace('"', '\\"')
    s = s.replace("\n", " ")
    return '"' + s + '"'


def find_pandoc() -> str:
    try:
        import pypandoc
        return pypandoc.get_pandoc_path()
    except Exception:
        pass
    for name in ("pandoc", "pandoc.exe"):
        p = shutil.which(name)
        if p:
            return p
    raise SystemExit("找不到 pandoc，请先安装 pypandoc_binary 或 pandoc")


def ensure_deps():
    try:
        import typst  # noqa: F401
    except Exception:
        raise SystemExit("缺少 typst 包，请运行：python -m pip install typst")
    try:
        import pymupdf  # noqa: F401
    except Exception:
        pass


# ---------- 读取配置 ----------

def load_json(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def collect_files(book_dir: Path) -> list:
    structure = load_json(book_dir / "structure.json")
    files = []
    for key in ("front", "chapters", "appendix", "back"):
        files.extend(structure.get(key, []))
    return files


IMG_RE = re.compile(r"!\[([^\]]*)\]\(([^)\s]+)(\s+\"[^\"]*\")?\)")


def rewrite_images(text: str, book_name: str) -> str:
    def repl(m):
        alt, src, title = m.group(1), m.group(2), m.group(3) or ""
        if re.match(r"^[a-zA-Z]+://", src) or src.startswith("/"):
            return m.group(0)
        p = src.replace("\\", "/")
        while p.startswith("../"):
            p = p[3:]
        p = p.lstrip("./")
        return f"![{alt}](/books/{book_name}/{p}{title})"

    return IMG_RE.sub(repl, text)


def build_markdown(book_dir: Path, out_md: Path, book_name: str):
    parts = []
    for rel in collect_files(book_dir):
        f = book_dir / rel
        if not f.exists():
            raise SystemExit(f"缺少文件：{f}")
        text = f.read_text(encoding="utf-8").strip()
        text = rewrite_images(text, book_name)
        parts.append(text)
    body = "\n\n".join(parts) + "\n"
    out_md.write_text(body, encoding="utf-8")
    return len(body)


# ---------- 体检 ----------

def check_book(book_dir: Path, meta: dict):
    problems = []
    for rel in collect_files(book_dir):
        f = book_dir / rel
        if not f.exists():
            problems.append(f"缺少文件 {rel}")
            continue
        text = f.read_text(encoding="utf-8")
        for m in IMG_RE.finditer(text):
            src = m.group(2)
            if re.match(r"^[a-zA-Z]+://", src):
                continue
            p = (f.parent / src).resolve()
            if not p.exists():
                problems.append(f"{rel} 引用了不存在的图片 {src}")
        if "```" in text:
            fences = text.count("```")
            if fences % 2 != 0:
                problems.append(f"{rel} 代码块围栏数量为奇数")
    for key in ("cover", "back"):
        p = (book_dir / meta[key]).resolve()
        if not p.exists():
            problems.append(f"缺少{key}图片 {meta[key]}")
    if problems:
        eprint("体检未通过：")
        for p in problems:
            eprint("  -", p)
        raise SystemExit(1)
    print(f"体检通过：{book_dir.name}")


# ---------- 主流程 ----------

def make_main_typ(meta: dict, body_path: Path, out: Path, toc_depth: int):
    meta_dict = dict(meta)
    lines = ["#let meta = ("]
    for k, v in meta_dict.items():
        if isinstance(v, (list, tuple)):
            lines.append(f"  {k}: ({', '.join(typst_str(x) for x in v)}),")
        else:
            lines.append(f"  {k}: {typst_str(v)},")
    lines.append(")")
    lines.append("")
    lines.append((BUILD_ROOT / "template.typ").read_text(encoding="utf-8"))
    lines.append("")
    lines.append("#cover-page()")
    lines.append("#title-page()")
    lines.append("#copyright-page()")
    lines.append('#set page(numbering: "i")')
    lines.append('#align(center)[#text(size: 20pt, weight: "bold", font: ("Microsoft YaHei", "SimHei"))[目录]]')
    lines.append("#v(8mm)")
    lines.append(f'#outline(title: none, depth: {toc_depth}, indent: auto)')
    lines.append("#counter(page).update(0)")
    lines.append('#set page(numbering: "1")')
    lines.append(body_path.read_text(encoding="utf-8"))
    lines.append("#back-page()")
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_book(book_arg: str, make_pdf: bool = True):
    book_dir = (ROOT / book_arg).resolve()
    book_name = book_dir.name
    meta = load_json(book_dir / "book.json")
    structure = load_json(book_dir / "structure.json")
    toc_depth = int(meta.get("toc_depth", 2))

    check_book(book_dir, meta)
    for key in ("cover", "back"):
        meta[key] = "/books/" + book_name + "/" + meta[key]

    work = TMP_ROOT / book_name
    work.mkdir(parents=True, exist_ok=True)
    combined = work / "combined.md"
    n = build_markdown(book_dir, combined, book_name)
    print(f"正文合并完成，共 {n} 字符")

    pandoc = find_pandoc()
    body_typ = work / "body.typ"
    cmd = [
        pandoc, str(combined),
        "-f", "markdown+smart+tex_math_dollars+pipe_tables+footnotes+implicit_figures+backtick_code_blocks",
        "-t", "typst",
        "--wrap=none",
        "--columns=500",
        "-o", str(body_typ),
    ]
    subprocess.run(cmd, check=True)

    main_typ = work / "main.typ"
    make_main_typ(meta, body_typ, main_typ, toc_depth)

    if not make_pdf:
        print("已生成 Typst 源，跳过 PDF")
        return

    import typst
    pdf_rel = meta["pdf"]
    pdf_out = ROOT / "output" / pdf_rel
    pdf_out.parent.mkdir(parents=True, exist_ok=True)
    typst.compile(
        str(main_typ),
        output=str(pdf_out),
        root=str(ROOT),
        font_paths=[str(Path(os.environ.get("WINDIR", "C:/Windows")) / "Fonts")],
    )
    size_mb = pdf_out.stat().st_size / 1024 / 1024
    pages = ""
    try:
        import pymupdf
        with pymupdf.open(pdf_out) as doc:
            pages = f"，{doc.page_count} 页"
    except Exception:
        pass
    print(f"PDF 生成：output/{pdf_rel}（{size_mb:.1f} MB{pages}）")


def build_figures(only: str = None):
    code_root = ROOT / "books" / "code"
    scripts = sorted(set(code_root.rglob("fig_*.py")) | set(code_root.rglob("gen_figs.py")))
    if only:
        scripts = [s for s in scripts if only in str(s)]
    if not scripts:
        print("没有找到绘图脚本")
        return
    py = sys.executable
    for s in scripts:
        print("绘制", s.relative_to(ROOT))
        subprocess.run([py, str(s)], check=True, cwd=str(ROOT))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--book", help="册目录，如 books/intro")
    ap.add_argument("--no-pdf", action="store_true")
    ap.add_argument("--figures", action="store_true")
    ap.add_argument("--only", default=None)
    args = ap.parse_args()

    ensure_deps()
    if args.figures:
        build_figures(args.only)
        return
    if not args.book:
        for name in ("intro", "theory"):
            build_book(f"books/{name}", not args.no_pdf)
        return
    build_book(args.book, not args.no_pdf)


if __name__ == "__main__":
    main()
