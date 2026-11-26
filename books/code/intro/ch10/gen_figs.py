import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "common"))
from style import *  # noqa

OUT, _ = chapter_paths(__file__)

fig, ax = new_canvas(7.2, 3.6)
ax.set_ylim(0, 5.0)

boxes = [
    (1.15, 3.3, "读取输入\n与上一时刻状态"),
    (3.45, 3.3, "更新膜电位\n数值积分一步"),
    (5.75, 3.3, "检测阈值\n是否放电"),
    (8.05, 3.3, "记录脉冲\n加入事件队列"),
    (8.05, 1.2, "传递突触\n投递到下游"),
    (3.45, 1.2, "推进时间\n进入下一步"),
]
for x, y, t in boxes:
    box(ax, x, y, 1.95, 1.35, t, fs=8.5)

arrow(ax, (2.14, 3.3), (2.45, 3.3), color=C["blue"])
arrow(ax, (4.44, 3.3), (4.75, 3.3), color=C["blue"])
arrow(ax, (6.74, 3.3), (7.05, 3.3), color=C["blue"])
arrow(ax, (8.05, 2.62), (8.05, 1.88), color=C["blue"])
arrow(ax, (7.07, 1.2), (4.44, 1.2), color=C["teal"])
arrow(ax, (3.45, 1.88), (3.45, 2.62), color=C["teal"])
arrow(ax, (2.48, 1.2), (1.15, 1.2), color=C["teal"], style="-", shrink=0)
arrow(ax, (1.15, 1.2), (1.15, 2.62), color=C["teal"], shrink=0)

ax.text(5.75, 4.55, "每个时间步重复一次", fontsize=9, color=C["muted"], ha="center")
ax.text(8.85, 2.3, "脉冲", fontsize=8, color=C["muted"], ha="left", va="center")
ax.text(5.75, 0.45, "反馈与时间推进", fontsize=9, color=C["teal"], ha="center")
save(fig, OUT, "fig01_loop.png")
