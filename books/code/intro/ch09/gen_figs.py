import sys
import pathlib

import matplotlib.pyplot as plt
from matplotlib.patches import Circle

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "common"))
from style import *  # noqa

OUT, _ = chapter_paths(__file__)

fig, ax = plt.subplots(figsize=(6.2, 4.4))
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis("off")

events = [
    ("1907", "积分发放模型（Lapicque）"),
    ("1943", "阈值逻辑神经元（McCulloch-Pitts）"),
    ("1949", "赫布学习规则"),
    ("1952", "霍奇金赫胥黎方程"),
    ("1961", "FitzHugh-Nagumo 二维模型"),
    ("1972", "Wilson-Cowan 神经质量模型"),
    ("1982", "Hopfield 吸引子网络"),
    ("1996", "平衡网络理论"),
    ("2003", "Izhikevich 四参数模型"),
]
ax.plot([4.7, 4.7], [0.55, 9.4], color=C["muted"], lw=1.2, zorder=1)
for i, (year, text) in enumerate(events):
    y = 9.0 - i * 1.0
    ax.add_patch(Circle((4.7, y), 0.08, facecolor=C["blue"], edgecolor="white",
                        linewidth=1.0, zorder=3))
    ax.text(4.42, y, year, ha="right", va="center", fontsize=9.2, color=C["blue"])
    ax.text(4.95, y, text, ha="left", va="center", fontsize=8.8, color=C["ink"])
save(fig, OUT, "fig01_models.png")
