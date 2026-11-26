import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "common"))
from style import *  # noqa

OUT, _ = chapter_paths(__file__)

fig, ax = new_canvas(7.2, 3.8)
ax.set_ylim(0, 5.28)

# 主链路
box(ax, 1.05, 3.6, 1.75, 1.2, "大脑模型\n神经元群", fs=8.8)
box(ax, 3.35, 3.6, 1.75, 1.2, "运动接口\n下降神经元", fs=8.8, fc=C["teal_l"], ec=C["teal"])
box(ax, 5.65, 3.6, 1.75, 1.2, "身体\n关节与肌肉", fs=8.8, fc=C["orange_l"], ec=C["orange"])
box(ax, 7.95, 3.6, 1.75, 1.2, "环境\n物体与气味", fs=8.8, fc=C["orange_l"], ec=C["orange"])

arrow(ax, (1.95, 3.6), (2.45, 3.6), color=C["blue"])
arrow(ax, (4.25, 3.6), (4.75, 3.6), color=C["teal"])
arrow(ax, (6.55, 3.6), (7.05, 3.6), color=C["orange"])
ax.text(2.2, 3.85, "指令", fontsize=8, color=C["muted"], ha="center")
ax.text(4.5, 3.85, "力矩", fontsize=8, color=C["muted"], ha="center")
ax.text(6.8, 3.85, "接触", fontsize=8, color=C["muted"], ha="center")

# 反馈链路
box(ax, 7.95, 1.35, 1.75, 1.2, "感觉器官\n受体与神经元", fs=8.8, fc=C["teal_l"], ec=C["teal"])
box(ax, 5.65, 1.35, 1.75, 1.2, "感觉接口\n放电率编码", fs=8.8, fc=C["teal_l"], ec=C["teal"])
box(ax, 3.35, 1.35, 1.75, 1.2, "延迟\n传导与处理", fs=8.8, fc=C["grey_l"], ec=C["muted"])
box(ax, 1.05, 1.35, 1.75, 1.2, "大脑模型\n更新状态", fs=8.8)

arrow(ax, (7.95, 2.95), (7.95, 2.0), color=C["orange"])
arrow(ax, (7.07, 1.35), (6.56, 1.35), color=C["teal"])
arrow(ax, (4.77, 1.35), (4.26, 1.35), color=C["muted"])
arrow(ax, (2.47, 1.35), (1.96, 1.35), color=C["blue"])
arrow(ax, (1.05, 2.0), (1.05, 2.95), color=C["blue"])

ax.text(8.25, 2.45, "刺激", fontsize=8, color=C["muted"], ha="left")
ax.text(3.35, 2.55, "延迟 15 毫秒", fontsize=8.2, color=C["red"], ha="center", va="top")

# 扰动
arrow(ax, (9.3, 5.0), (8.6, 4.25), color=C["red"], lw=1.1)
ax.text(9.35, 5.05, "扰动", fontsize=8.5, color=C["red"], ha="left", va="bottom")
ax.text(5.0, 0.5, "行为来自大脑、身体、环境三者的耦合", fontsize=9,
        color=C["muted"], ha="center")
save(fig, OUT, "fig01_loop.png")
