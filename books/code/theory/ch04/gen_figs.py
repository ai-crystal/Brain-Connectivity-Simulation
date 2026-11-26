import sys
import pathlib

import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "common"))
from style import *  # noqa

OUT, _ = chapter_paths(__file__)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6.6, 2.9))

x = np.linspace(0, 600, 400)
for lam, color, label in [(100, C["orange"], "长度常数 100 微米"),
                          (200, C["blue"], "长度常数 200 微米"),
                          (400, C["teal"], "长度常数 400 微米")]:
    ax1.plot(x, np.exp(-x / lam), color=color, lw=1.5, label=label)
ax1.axhline(np.exp(-1), color=C["muted"], lw=0.7, ls=":")
ax1.text(585, np.exp(-1) + 0.03, "37%", fontsize=8, color=C["muted"], ha="right")
ax1.set_xlabel("距胞体的距离 (微米)")
ax1.set_ylabel("归一化电位")
ax1.set_xlim(0, 600)
ax1.set_ylim(0, 1.05)
ax1.legend(loc="upper right", fontsize=7.5)
ax1.grid(color=C["grid"], lw=0.5, alpha=0.6)
ax1.set_axisbelow(True)

t = np.linspace(0, 30, 400)
tau_near, tau_far = 2.0, 6.0


def alpha(t, tau):
    y = (t / tau) * np.exp(1 - t / tau)
    return y


ax2.plot(t, alpha(t, tau_near), color=C["blue"], lw=1.5, label="近端突触")
ax2.plot(t, 0.45 * alpha(t - 2.0, tau_far), color=C["orange"], lw=1.5, label="远端突触")
ax2.set_xlabel("时间 (ms)")
ax2.set_ylabel("归一化突触后电位")
ax2.set_xlim(0, 30)
ax2.set_ylim(0, 1.08)
ax2.legend(loc="upper right", fontsize=7.5)
ax2.grid(axis="y", color=C["grid"], lw=0.5, alpha=0.6)
ax2.set_axisbelow(True)
fig.tight_layout()
save(fig, OUT, "fig01_cable.png")
