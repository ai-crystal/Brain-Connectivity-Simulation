"""绘图共用样式与工具。"""
import pathlib

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Rectangle

plt.rcParams.update({
    "font.sans-serif": ["SimHei", "Microsoft YaHei", "DejaVu Sans"],
    "mathtext.fontset": "dejavusans",
    "axes.unicode_minus": False,
    "font.size": 11.5,
    "figure.dpi": 200,
    "savefig.dpi": 200,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.08,
    "axes.linewidth": 0.9,
    "axes.edgecolor": "#333333",
    "axes.labelcolor": "#222222",
    "xtick.color": "#333333",
    "ytick.color": "#333333",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "legend.frameon": False,
})

# 插图在 PDF 中会被缩到版心宽度，统一放大字号以保证可读性
_FONT_SCALE = 1.30
_orig_text = matplotlib.axes.Axes.text
_orig_annotate = matplotlib.axes.Axes.annotate
_orig_legend = matplotlib.axes.Axes.legend


def _scale(kw):
    if kw.get("fontsize") is not None:
        kw["fontsize"] = kw["fontsize"] * _FONT_SCALE
    if kw.get("size") is not None:
        kw["size"] = kw["size"] * _FONT_SCALE
    return kw


def _text(self, x, y, s, *a, **kw):
    return _orig_text(self, x, y, s, *a, **_scale(kw))


def _annotate(self, *a, **kw):
    return _orig_annotate(self, *a, **_scale(kw))


def _legend(self, *a, **kw):
    return _orig_legend(self, *a, **_scale(kw))


matplotlib.axes.Axes.text = _text
matplotlib.axes.Axes.annotate = _annotate
matplotlib.axes.Axes.legend = _legend

C = {
    "ink": "#1f2933",
    "muted": "#5b6770",
    "blue": "#2f5d72",
    "blue_l": "#dce8ee",
    "teal": "#2f7d6e",
    "teal_l": "#dcefe9",
    "orange": "#c46a2b",
    "orange_l": "#f6e4d5",
    "red": "#b03a2e",
    "red_l": "#f6dedb",
    "grey_l": "#eef1f3",
    "grid": "#d9dee3",
}


def chapter_paths(file):
    """根据脚本位置返回插图输出目录与章号。"""
    here = pathlib.Path(file).resolve()
    root = here.parents[4]
    book = here.parents[1].name
    chapter = here.parent.name.replace("ch", "")
    out = root / "books" / book / "images" / chapter
    out.mkdir(parents=True, exist_ok=True)
    return out, chapter


def new_canvas(w=6.4, h=3.6):
    fig = plt.figure(figsize=(w, h))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10 * h / w)
    ax.axis("off")
    return fig, ax


def box(ax, x, y, w, h, text, fc=None, ec=None, fs=9, color=None, bold=False, radius=0.12, lw=1.0):
    fc = fc or C["blue_l"]
    ec = ec or C["blue"]
    patch = FancyBboxPatch(
        (x - w / 2, y - h / 2), w, h,
        boxstyle=f"round,pad=0,rounding_size={radius}",
        facecolor=fc, edgecolor=ec, linewidth=lw, zorder=2,
    )
    ax.add_patch(patch)
    ax.text(
        x, y, text, ha="center", va="center", fontsize=fs,
        color=color or C["ink"], zorder=3,
        fontweight="bold" if bold else "normal",
        linespacing=1.5,
    )
    return patch


def arrow(ax, p1, p2, color=None, lw=1.2, style="-|>", rad=0.0, ls="-", shrink=6):
    color = color or C["muted"]
    a = FancyArrowPatch(
        p1, p2, arrowstyle=style, mutation_scale=12,
        color=color, linewidth=lw, linestyle=ls,
        connectionstyle=f"arc3,rad={rad}",
        shrinkA=shrink, shrinkB=shrink, zorder=1,
    )
    ax.add_patch(a)
    return a


def save(fig, out_dir, name):
    path = out_dir / name
    fig.savefig(path, facecolor="white")
    plt.close(fig)
    print("saved", path)
