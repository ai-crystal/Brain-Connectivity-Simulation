import sys
import pathlib

import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "common"))
from style import *  # noqa

OUT, _ = chapter_paths(__file__)

dt = np.linspace(-60, 60, 600)
A_plus, A_minus = 1.0, 1.1
tau_plus, tau_minus = 18.0, 22.0
dw = np.where(dt >= 0, A_plus * np.exp(-dt / tau_plus),
              -A_minus * np.exp(dt / tau_minus))

fig, ax = plt.subplots(figsize=(6.2, 3.0))
ax.plot(dt, dw, color=C["blue"], lw=1.8)
ax.axhline(0, color=C["muted"], lw=0.8)
ax.axvline(0, color=C["muted"], lw=0.8)
ax.fill_between(dt, 0, dw, where=dw > 0, color=C["blue"], alpha=0.12)
ax.fill_between(dt, 0, dw, where=dw < 0, color=C["red"], alpha=0.12)
ax.set_xlabel("突触后放电时间减突触前放电时间 (ms)")
ax.set_ylabel("突触权重变化")
ax.set_xlim(-60, 60)
ax.set_ylim(-1.2, 1.2)
ax.text(30, 0.72, "前于后\n增强", fontsize=8.5, color=C["blue"], ha="center")
ax.text(-30, -0.85, "后于前\n减弱", fontsize=8.5, color=C["red"], ha="center")
ax.grid(axis="y", color=C["grid"], lw=0.5, alpha=0.6)
ax.set_axisbelow(True)
fig.tight_layout()
save(fig, OUT, "fig01_stdp.png")
