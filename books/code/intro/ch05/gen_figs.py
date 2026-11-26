import sys
import pathlib

import matplotlib.pyplot as plt
from matplotlib.patches import Circle

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "common"))
from style import *  # noqa

OUT, _ = chapter_paths(__file__)

# 图 5-1 分辨率与视野
fig, ax = plt.subplots(figsize=(6.4, 3.9))
methods = [
    ("电子显微镜", 0.6, 0.004, 14, 0, "left"),
    ("膨胀显微", 1.2, 0.07, -12, 10, "right"),
    ("共聚焦", 1.6, 0.20, 8, -20, "left"),
    ("双光子", 2.4, 0.32, 8, 12, "left"),
    ("光片", 9.0, 0.30, 0, 14, "center"),
    ("钙成像", 2.5, 10.0, 16, 10, "left"),
    ("高密度电极", 3.5, 20.0, -10, 12, "right"),
    ("功能磁共振", 90.0, 1000.0, 0, -20, "center"),
    ("脑电", 220.0, 8000.0, -10, 8, "right"),
]
for name, fov, res, dx, dy, ha in methods:
    ax.scatter(fov, res, s=40, color=C["blue"], zorder=3, edgecolor="white", linewidth=0.8)
    ax.annotate(name, xy=(fov, res), xytext=(dx, dy), textcoords="offset points",
                fontsize=8.2, color=C["ink"], ha=ha, va="center")

ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlim(0.25, 500)
ax.set_ylim(0.0015, 30000)
ax.set_xticks([0.3, 1, 3, 10, 30, 100, 300])
ax.set_xticklabels(["0.3", "1", "3", "10", "30", "100", "300"])
ax.set_yticks([0.003, 0.01, 0.03, 0.1, 0.3, 1, 3, 10, 30, 100, 1000, 10000])
ax.set_yticklabels(["0.003", "0.01", "0.03", "0.1", "0.3", "1", "3", "10", "30", "100", "1000", "10000"])
ax.set_xlabel("一次成像覆盖的视野（毫米）")
ax.set_ylabel("可分辨的最小结构（微米）")
ax.grid(color=C["grid"], lw=0.6, alpha=0.7)
ax.set_axisbelow(True)
ax.text(0.28, 15000, "分辨率高，视野小", fontsize=8.5, color=C["muted"], va="top")
ax.text(470, 0.0022, "视野大，分辨率低", fontsize=8.5, color=C["muted"], ha="right", va="bottom")
fig.tight_layout()
save(fig, OUT, "fig01_methods.png")

# 时间线（生成到第 6 章目录）
here = pathlib.Path(__file__).resolve()
root = here.parents[4]
out6 = root / "books" / "intro" / "images" / "06"
out6.mkdir(parents=True, exist_ok=True)

fig, ax = plt.subplots(figsize=(6.2, 4.6))
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis("off")
events = [
    ("1963", "Brenner 选择线虫作为模式动物"),
    ("1986", "White 等人发表线虫完整连接组"),
    ("2004", "自动切片与扫描电镜投入使用"),
    ("2013", "Janelia 启动果蝇半脑计划"),
    ("2020", "果蝇中央脑连接组发布"),
    ("2024", "FlyWire 成年果蝇全脑连接组"),
    ("2025", "全脑模型在 12 片神经形态芯片上运行"),
    ("2026", "Eon 把全脑模型接上虚拟身体"),
]
ax.plot([4.55, 4.55], [0.7, 9.3], color=C["muted"], lw=1.2, zorder=1)
for i, (year, text) in enumerate(events):
    y = 8.9 - i * 1.12
    ax.add_patch(Circle((4.55, y), 0.09, facecolor=C["blue"], edgecolor="white",
                        linewidth=1.0, zorder=3))
    ax.text(4.28, y, year, ha="right", va="center", fontsize=9.5, color=C["blue"])
    ax.text(4.82, y, text, ha="left", va="center", fontsize=8.8, color=C["ink"])
fig.savefig(out6 / "fig01_timeline.png", facecolor="white")
plt.close(fig)
print("saved", out6 / "fig01_timeline.png")
