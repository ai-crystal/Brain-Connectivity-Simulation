import sys
import pathlib

import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "common"))
from style import *  # noqa

OUT, _ = chapter_paths(__file__)

# ---------- 混沌：Lorenz ----------
sigma, rho, beta = 10.0, 28.0, 8.0 / 3.0


def lorenz(t, s):
    x, y, z = s
    return [sigma * (y - x), x * (rho - z) - y, x * y - beta * z]


T = 40.0
te = np.linspace(0, T, 8000)
s1 = solve_ivp(lorenz, (0, T), [1.0, 1.0, 1.0], t_eval=te, rtol=1e-9, atol=1e-9).y
s2 = solve_ivp(lorenz, (0, T), [1.0 + 1e-5, 1.0, 1.0], t_eval=te, rtol=1e-9, atol=1e-9).y
dist = np.sqrt(((s1 - s2) ** 2).sum(axis=0))

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6.4, 3.9), sharex=True,
                               gridspec_kw={"height_ratios": [1.2, 1]})
ax1.plot(te, s1[0], color=C["blue"], lw=1.1, label="初始条件 A")
ax1.plot(te, s2[0], color=C["orange"], lw=1.1, ls="--", label="初始条件 B")
ax1.set_ylabel("变量 x")
ax1.legend(loc="upper right", fontsize=7.5, ncol=2)
ax1.grid(axis="y", color=C["grid"], lw=0.5, alpha=0.6)
ax1.set_axisbelow(True)

ax2.semilogy(te, np.maximum(dist, 1e-12), color=C["red"], lw=1.2)
ax2.set_xlabel("时间")
ax2.set_ylabel("两条轨道的距离")
ax2.yaxis.set_major_formatter(FuncFormatter(lambda v, p: f"{v:g}"))
ax2.set_xlim(0, T)
ax2.grid(axis="y", color=C["grid"], lw=0.5, alpha=0.6)
ax2.set_axisbelow(True)
ax2.axvline(18, color=C["muted"], lw=0.8, ls=":")
ax2.text(18.6, ax2.get_ylim()[1] * 0.25, "指数分离", fontsize=8, color=C["muted"])
fig.tight_layout()
save(fig, OUT, "fig01_chaos.png")

# ---------- 分支过程雪崩 ----------
rng = np.random.default_rng(7)


def sample_avalanche(sigma_b, cap=2000):
    size = 0
    active = 1
    while active > 0:
        size += active
        if size > cap:
            return None
        active = rng.poisson(sigma_b * active)
    return size


fig, ax = plt.subplots(figsize=(6.2, 3.0))
for sigma_b, color, label in [(0.85, C["teal"], "分支比 0.85"),
                              (1.0, C["blue"], "分支比 1.0"),
                              (1.12, C["orange"], "分支比 1.12")]:
    sizes = [sample_avalanche(sigma_b) for _ in range(20000)]
    sizes = np.array([s for s in sizes if s], dtype=float)
    bins = np.logspace(0, 3.2, 34)
    hist, edges = np.histogram(sizes, bins=bins)
    centers = np.sqrt(edges[:-1] * edges[1:])
    ax.loglog(centers, hist, "o", ms=2.6, color=color, alpha=0.8, label=label)

ax.set_xlabel("雪崩大小（神经元数）")
ax.set_ylabel("出现次数")
ax.set_xlim(1, 2000)
ax.legend(fontsize=7.5)
ax.grid(color=C["grid"], lw=0.5, alpha=0.6, which="major")
ax.set_axisbelow(True)
fig.tight_layout()
save(fig, OUT, "fig02_avalanche.png")
