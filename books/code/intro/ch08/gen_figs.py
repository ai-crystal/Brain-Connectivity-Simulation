import sys
import pathlib

import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "common"))
from style import *  # noqa

OUT, _ = chapter_paths(__file__)

fig, ax = plt.subplots(figsize=(6.4, 3.2))
species = ["线虫", "果蝇", "小鼠", "人"]
counts = [302, 139255, 7.0e7, 8.6e10]
done = [True, True, False, False]
y = np.arange(len(species))

ax.plot(counts, y, color=C["grid"], lw=1.2, zorder=1)
for yi, c, d in zip(y, counts, done):
    ax.scatter(c, yi, s=70, zorder=3,
               facecolor=C["blue"] if d else "white",
               edgecolor=C["blue"], linewidth=1.3)
    ax.text(c * 1.6, yi, f"{c:,.0f}", va="center", ha="left", fontsize=8.5)

ax.set_xscale("log")
ax.set_yticks(y)
ax.set_yticklabels(species)
ax.set_xlim(100, 1e13)
ax.set_xlabel("神经元数量（对数坐标）")
ax.grid(axis="x", color=C["grid"], lw=0.6, alpha=0.7)
ax.set_axisbelow(True)

ax.scatter([], [], s=70, facecolor=C["blue"], edgecolor=C["blue"], label="已有完整连接组")
ax.scatter([], [], s=70, facecolor="white", edgecolor=C["blue"], label="尚无完整连接组")
ax.legend(loc="lower right", fontsize=8, handletextpad=0.6)
fig.tight_layout()
save(fig, OUT, "fig01_ladder.png")
