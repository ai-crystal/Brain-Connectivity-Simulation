import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "common"))
from style import *  # noqa

OUT, _ = chapter_paths(__file__)

# 图 1-1 四层管线
fig, ax = new_canvas(7.2, 4.2)
ys = 4.35
xs = [1.25, 3.75, 6.25, 8.75]
labels = [
    "连接组\nFlyWire\n13.9 万神经元",
    "神经元模型\n漏电积分\n发放",
    "接口\n感觉输入\n运动读出",
    "虚拟身体\nMuJoCo\n87 个关节",
]
nums = ["①", "②", "③", "④"]
for x, t, n in zip(xs, labels, nums):
    box(ax, x, ys, 2.15, 1.85, t, fs=8.6)
    ax.text(x, ys + 1.22, n, ha="center", va="center", fontsize=12, color=C["blue"])
for i in range(3):
    arrow(ax, (xs[i] + 1.08, ys), (xs[i + 1] - 1.08, ys), color=C["blue"], lw=1.4)

box(ax, 5.0, 1.3, 9.1, 0.95,
    "闭环：身体运动改变感觉输入，新的输入再送回大脑",
    fc=C["grey_l"], ec=C["muted"], fs=9)
arrow(ax, (8.75, ys - 0.95), (8.75, 1.8), color=C["muted"], lw=1.1)
arrow(ax, (1.25, 1.8), (1.25, ys - 0.95), color=C["muted"], lw=1.1)
save(fig, OUT, "fig01_pipeline.png")

# 图 1-2 感觉运动闭环
fig, ax = new_canvas(6.4, 4.4)
ax.set_ylim(0, 6.9)
box(ax, 2.6, 5.4, 3.2, 1.35, "大脑模型\n13.9 万个 LIF 神经元", fs=9)
box(ax, 7.4, 5.4, 3.2, 1.35, "下降神经元\n转向、前进、进食", fs=9, fc=C["teal_l"], ec=C["teal"])
box(ax, 7.4, 1.6, 3.2, 1.35, "身体与环境\nMuJoCo 物理仿真", fs=9, fc=C["orange_l"], ec=C["orange"])
box(ax, 2.6, 1.6, 3.2, 1.35, "感觉神经元\n味觉、嗅觉、触觉、视觉", fs=9, fc=C["teal_l"], ec=C["teal"])

arrow(ax, (4.25, 5.4), (5.75, 5.4), color=C["blue"], lw=1.5)
ax.text(5.0, 5.62, "运动指令", ha="center", va="bottom", fontsize=8.5, color=C["muted"])
arrow(ax, (7.4, 4.7), (7.4, 2.3), color=C["orange"], lw=1.5)
ax.text(7.62, 3.5, "执行", ha="left", va="center", fontsize=8.5, color=C["muted"])
arrow(ax, (5.75, 1.6), (4.25, 1.6), color=C["teal"], lw=1.5)
ax.text(5.0, 1.82, "感觉信号", ha="center", va="bottom", fontsize=8.5, color=C["muted"])
arrow(ax, (2.6, 2.3), (2.6, 4.7), color=C["blue"], lw=1.5)
ax.text(2.38, 3.5, "输入", ha="right", va="center", fontsize=8.5, color=C["muted"])

ax.text(5.0, 3.5, "每 15 毫秒\n同步一次", ha="center", va="center", fontsize=10,
        color=C["ink"], linespacing=1.6,
        bbox=dict(boxstyle="round,pad=0.5", facecolor="white", edgecolor=C["grid"]))
save(fig, OUT, "fig02_loop.png")
