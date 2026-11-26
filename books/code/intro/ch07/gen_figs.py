import sys
import pathlib

import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "common"))
from style import *  # noqa

OUT, _ = chapter_paths(__file__)

fig, axes = plt.subplots(1, 2, figsize=(6.4, 2.9), sharey=True)
names = ["线虫", "果蝇半脑", "果蝇全脑"]
neurons = [302, 25000, 139255]
synapses = [7000, 2.0e7, 5.0e7]
colors = [C["teal"], C["blue"], C["orange"]]

for ax, vals, title, unit in [
    (axes[0], neurons, "神经元数量", "个"),
    (axes[1], synapses, "突触数量", "个"),
]:
    y = np.arange(len(names))
    ax.barh(y, vals, color=colors, height=0.55, edgecolor="none")
    ax.set_xscale("log")
    ax.set_yticks(y)
    ax.set_yticklabels(names)
    ax.set_title(title, fontsize=10, pad=8)
    ax.set_xlabel("数量（对数坐标）")
    ax.grid(axis="x", color=C["grid"], lw=0.6, alpha=0.7)
    ax.set_axisbelow(True)
    for yi, v in zip(y, vals):
        label = f"{v:,.0f}"
        ax.text(v * 1.25, yi, label, va="center", ha="left", fontsize=8)
    ax.set_xlim(100, 2e8)

axes[0].invert_yaxis()
fig.tight_layout()
save(fig, OUT, "fig01_scale.png")
