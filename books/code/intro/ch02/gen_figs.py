import sys
import pathlib

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "common"))
from style import *  # noqa

OUT, _ = chapter_paths(__file__)

# 图 2-1 神经元结构
fig, ax = new_canvas(7.2, 3.8)
ax.set_ylim(0, 5.2)

soma = (3.5, 2.55)
ax.add_patch(Circle(soma, 0.58, facecolor=C["blue_l"], edgecolor=C["blue"], lw=1.3, zorder=4))
ax.add_patch(Circle((3.32, 2.62), 0.16, facecolor="white", edgecolor=C["muted"], lw=0.7, zorder=5))

# 树突分支
branches = [
    [(3.0, 2.9), (2.5, 3.45), (1.9, 3.55), (1.4, 3.95)],
    [(2.95, 2.7), (2.3, 2.9), (1.7, 2.85), (1.05, 3.15)],
    [(3.0, 2.25), (2.45, 2.05), (1.9, 1.85), (1.3, 1.55)],
    [(3.1, 2.05), (2.8, 1.55), (2.5, 1.15)],
]
for b in branches:
    xs, ys = zip(*b)
    ax.plot(xs, ys, color=C["blue"], lw=3.0, solid_capstyle="round", zorder=3)
    # 细小末梢
    ax.plot([xs[-1], xs[-1] - 0.18], [ys[-1], ys[-1] + 0.12], color=C["blue"], lw=1.6, zorder=3)

# 轴突
ax.plot([4.08, 7.55], [2.55, 2.55], color=C["orange"], lw=4.2, solid_capstyle="round", zorder=3)
# 髓鞘样分段，仅示意
for x0 in np.arange(4.5, 7.3, 0.55):
    ax.plot([x0, x0 + 0.32], [2.55, 2.55], color=C["orange_l"], lw=4.6, solid_capstyle="butt", zorder=4)
# 末梢分支
ends = [((7.55, 2.55), (8.35, 3.05)), ((7.55, 2.55), (8.35, 2.55)), ((7.55, 2.55), (8.35, 2.05))]
for p0, p1 in ends:
    ax.plot([p0[0], p1[0]], [p0[1], p1[1]], color=C["orange"], lw=2.2, zorder=3)
    ax.add_patch(Circle(p1, 0.11, facecolor=C["orange"], edgecolor="none", zorder=4))

# 标注
ax.annotate("树突", xy=(1.95, 3.55), xytext=(1.05, 4.45), fontsize=9.5,
            ha="center", va="center",
            arrowprops=dict(arrowstyle="-|>", color=C["muted"], lw=0.9,
                            shrinkA=2, shrinkB=2))
ax.annotate("胞体", xy=(3.5, 1.95), xytext=(3.5, 1.05), fontsize=9.5,
            ha="center", va="center",
            arrowprops=dict(arrowstyle="-|>", color=C["muted"], lw=0.9,
                            shrinkA=2, shrinkB=2))
ax.annotate("轴突", xy=(5.15, 2.85), xytext=(5.9, 3.85), fontsize=9.5,
            ha="center", va="center",
            arrowprops=dict(arrowstyle="-|>", color=C["muted"], lw=0.9,
                            shrinkA=2, shrinkB=2))
ax.annotate("突触末梢", xy=(8.42, 2.45), xytext=(8.95, 1.25), fontsize=9.5,
            ha="center", va="center",
            arrowprops=dict(arrowstyle="-|>", color=C["muted"], lw=0.9,
                            shrinkA=2, shrinkB=2))
ax.text(6.3, 1.55, "信号沿轴突传向其他神经元", fontsize=8.5, color=C["muted"],
        ha="center", va="center")
save(fig, OUT, "fig01_neuron.png")

# 图 2-2 化学突触
fig, ax = new_canvas(7.2, 4.0)
ax.set_ylim(0, 5.55)

# 突触前终末
ax.add_patch(FancyBboxPatch((0.55, 1.75), 3.55, 2.55,
                            boxstyle="round,pad=0,rounding_size=0.35",
                            facecolor=C["teal_l"], edgecolor=C["teal"], lw=1.2, zorder=2))
ax.text(2.3, 3.95, "突触前终末", fontsize=9.5, ha="center", va="center", color=C["ink"])
# 囊泡
rng = np.random.default_rng(3)
for cx, cy in [(2.75, 2.35), (3.1, 2.6), (3.25, 2.2), (2.85, 2.85), (3.35, 2.9), (3.55, 2.45)]:
    ax.add_patch(Circle((cx, cy), 0.15, facecolor="white", edgecolor=C["teal"], lw=0.9, zorder=3))
ax.annotate("囊泡", xy=(2.75, 2.35), xytext=(1.35, 2.25), fontsize=9,
            ha="center", va="center", color=C["muted"],
            arrowprops=dict(arrowstyle="-|>", color=C["muted"], lw=0.8, shrinkA=2, shrinkB=3))

# 突触后膜
ax.add_patch(FancyBboxPatch((5.85, 1.75), 3.55, 2.55,
                            boxstyle="round,pad=0,rounding_size=0.35",
                            facecolor=C["blue_l"], edgecolor=C["blue"], lw=1.2, zorder=2))
ax.text(7.6, 3.95, "突触后神经元", fontsize=9.5, ha="center", va="center", color=C["ink"])
# 受体
for y in [2.25, 2.6, 2.95]:
    ax.add_patch(FancyBboxPatch((5.85, y - 0.09), 0.26, 0.18,
                                boxstyle="round,pad=0,rounding_size=0.04",
                                facecolor=C["blue"], edgecolor="none", zorder=4))
ax.annotate("受体", xy=(6.0, 2.2), xytext=(7.0, 2.0), fontsize=9,
            ha="center", va="center", color=C["muted"],
            arrowprops=dict(arrowstyle="-|>", color=C["muted"], lw=0.8, shrinkA=2, shrinkB=3))

# 间隙标注
ax.annotate("", xy=(4.1, 4.35), xytext=(5.85, 4.35),
            arrowprops=dict(arrowstyle="<->", color=C["muted"], lw=0.9))
ax.text(4.97, 4.55, "间隙 20 至 30 纳米", fontsize=8.5, ha="center", va="bottom", color=C["muted"])

# 钙离子与递质
ax.annotate("钙离子内流", xy=(3.55, 1.85), xytext=(2.3, 1.05), fontsize=9,
            ha="center", va="center", color=C["orange"],
            arrowprops=dict(arrowstyle="-|>", color=C["orange"], lw=1.0, shrinkA=2, shrinkB=3))
for y in [2.45, 2.75]:
    ax.annotate("", xy=(5.8, y), xytext=(4.2, y),
                arrowprops=dict(arrowstyle="-|>", color=C["red"], lw=1.0))
ax.text(5.0, 1.35, "递质扩散过间隙", fontsize=8.5, ha="center", va="center", color=C["red"])
save(fig, OUT, "fig02_synapse.png")
