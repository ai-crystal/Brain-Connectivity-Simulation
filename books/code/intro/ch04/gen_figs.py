import sys
import pathlib

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "common"))
from style import *  # noqa

OUT, _ = chapter_paths(__file__)

fig, axes = plt.subplots(2, 2, figsize=(6.4, 4.6))
for ax in axes.ravel():
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis("off")


def node(ax, x, y, color=None, r=0.55):
    ax.add_patch(Circle((x, y), r, facecolor=color or C["blue_l"],
                        edgecolor=C["blue"], lw=1.1, zorder=3))


def exc(ax, p1, p2, rad=0.0):
    ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle="-|>", mutation_scale=11,
                                 color=C["blue"], lw=1.2, zorder=2,
                                 connectionstyle=f"arc3,rad={rad}",
                                 shrinkA=9, shrinkB=9))


def inh(ax, p1, p2, rad=0.0):
    ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle="-[", mutation_scale=9,
                                 color=C["red"], lw=1.2, zorder=2,
                                 connectionstyle=f"arc3,rad={rad}",
                                 shrinkA=9, shrinkB=9))


# (a) 发散
ax = axes[0, 0]
node(ax, 1.8, 5.0)
for y in (8.0, 5.0, 2.0):
    node(ax, 8.2, y, C["teal_l"])
    exc(ax, (2.35, 5.0), (7.65, y), rad=0.0)
ax.set_title("发散", fontsize=9.5, pad=6)

# (b) 汇聚
ax = axes[0, 1]
node(ax, 8.2, 5.0)
for y in (8.0, 5.0, 2.0):
    node(ax, 1.8, y, C["teal_l"])
    exc(ax, (2.35, y), (7.65, 5.0), rad=0.0)
ax.set_title("汇聚", fontsize=9.5, pad=6)

# (c) 前馈抑制
ax = axes[1, 0]
node(ax, 1.4, 5.0, C["teal_l"])
node(ax, 5.0, 7.6)
node(ax, 5.0, 2.4, C["red_l"])
node(ax, 8.6, 5.0)
exc(ax, (1.95, 5.2), (4.45, 7.3))
exc(ax, (1.95, 4.8), (4.45, 2.7))
inh(ax, (5.55, 2.55), (8.15, 4.75), rad=0.25)
exc(ax, (5.55, 7.45), (8.15, 5.25), rad=-0.2)
ax.set_title("前馈抑制", fontsize=9.5, pad=6)

# (d) 相互抑制
ax = axes[1, 1]
node(ax, 3.0, 5.0, C["red_l"])
node(ax, 7.0, 5.0, C["red_l"])
inh(ax, (3.55, 5.15), (6.45, 5.15), rad=-0.55)
inh(ax, (6.45, 4.85), (3.55, 4.85), rad=-0.55)
ax.set_title("相互抑制", fontsize=9.5, pad=6)

fig.tight_layout(h_pad=1.0)
save(fig, OUT, "fig01_motifs.png")

# 环形吸引子
fig = plt.figure(figsize=(6.4, 3.2))
ax1 = fig.add_axes([0.02, 0.05, 0.46, 0.9])
ax1.set_xlim(-1.35, 1.35)
ax1.set_ylim(-1.35, 1.35)
ax1.set_aspect("equal")
ax1.axis("off")

N = 20
angles = np.linspace(0, 2 * np.pi, N, endpoint=False)
center = np.pi / 2
sigma = 0.55
act = np.exp(-0.5 * ((np.angle(np.exp(1j * (angles - center)))) / sigma) ** 2)
for a, s in zip(angles, act):
    x, y = np.cos(a), np.sin(a)
    ax1.add_patch(Circle((x, y), 0.085, facecolor=plt.cm.Blues(0.25 + 0.7 * s),
                         edgecolor=C["blue"], lw=0.8, zorder=3))
for a in angles:
    a2 = a + 2 * np.pi / N
    ax1.add_patch(FancyArrowPatch((0.93 * np.cos(a), 0.93 * np.sin(a)),
                                  (0.93 * np.cos(a2), 0.93 * np.sin(a2)),
                                  arrowstyle="-|>", mutation_scale=7,
                                  color=C["grid"], lw=0.7, zorder=2))
ax1.annotate("", xy=(0, 1.06), xytext=(0, 1.30),
             arrowprops=dict(arrowstyle="-|>", color=C["orange"], lw=1.1))
ax1.text(0.12, 1.20, "方向", fontsize=8, color=C["orange"], ha="left", va="center")
ax1.text(0, -1.28, "环上的神经元按偏好方向排列", fontsize=8.5,
         color=C["muted"], ha="center", va="center")

ax2 = fig.add_axes([0.55, 0.16, 0.42, 0.72])
deg = np.degrees(np.angle(np.exp(1j * (np.linspace(0, 2 * np.pi, 400) - center))))
x = np.linspace(-180, 180, 400)
y = np.exp(-0.5 * (x / 32) ** 2)
ax2.plot(x, y, color=C["blue"], lw=1.8)
ax2.fill_between(x, 0, y, color=C["blue"], alpha=0.15)
ax2.set_xlabel("偏好方向（度）")
ax2.set_ylabel("活动强度")
ax2.set_xlim(-180, 180)
ax2.set_ylim(0, 1.12)
ax2.set_xticks([-180, -90, 0, 90, 180])
ax2.grid(axis="y", color=C["grid"], lw=0.6, alpha=0.7)
ax2.set_axisbelow(True)
save(fig, OUT, "fig02_ring.png")
