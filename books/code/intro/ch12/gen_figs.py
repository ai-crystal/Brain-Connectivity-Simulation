import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "common"))
from style import *  # noqa

OUT, _ = chapter_paths(__file__)

fig, ax = new_canvas(7.2, 4.4)
ax.set_ylim(0, 6.1)

layers = [
    (4.95, "身体与环境　MuJoCo 物理引擎", C["orange_l"], C["orange"]),
    (3.65, "接口　感觉输入与运动读出", C["teal_l"], C["teal"]),
    (2.35, "模型　13.9 万个 LIF 神经元", C["blue_l"], C["blue"]),
    (1.05, "数据　FlyWire 全脑连接组", C["grey_l"], C["muted"]),
]
for y, text, fc, ec in layers:
    box(ax, 4.6, y, 6.6, 1.0, text, fc=fc, ec=ec, fs=9)

for y0, y1 in [(1.55, 1.85), (2.85, 3.15), (4.15, 4.45)]:
    arrow(ax, (4.6, y0), (4.6, y1), color=C["muted"], lw=1.1)
    arrow(ax, (5.4, y1), (5.4, y0), color=C["muted"], lw=1.1, ls="--")

ax.text(8.6, 4.95, "物理与感官", fontsize=8, color=C["orange"], ha="left", va="center")
ax.text(8.6, 3.65, "映射与编码", fontsize=8, color=C["teal"], ha="left", va="center")
ax.text(8.6, 2.35, "动力学", fontsize=8, color=C["blue"], ha="left", va="center")
ax.text(8.6, 1.05, "结构", fontsize=8, color=C["muted"], ha="left", va="center")

ax.text(4.6, 5.85, "自下而上：结构约束模型，模型驱动接口，接口耦合身体",
        fontsize=8.8, color=C["muted"], ha="center")
save(fig, OUT, "fig01_system.png")
