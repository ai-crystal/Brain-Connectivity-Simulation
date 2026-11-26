import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "common"))
from style import *  # noqa

OUT, _ = chapter_paths(__file__)

fig, ax = new_canvas(7.2, 3.8)
ax.set_ylim(0, 5.28)

steps = [
    (1.3, 0.95, "静态激活\n忽略时间", C["grey_l"], C["muted"]),
    (3.8, 1.95, "速率模型\n连续放电率", C["blue_l"], C["blue"]),
    (6.3, 2.95, "脉冲模型\n离散放电事件", C["teal_l"], C["teal"]),
    (8.8, 3.95, "生物物理模型\n离子通道与房室", C["orange_l"], C["orange"]),
]
for x, y, t, fc, ec in steps:
    box(ax, x, y, 2.0, 1.0, t, fc=fc, ec=ec, fs=8.6)

for i in range(3):
    x0, y0 = steps[i][0] + 1.0, steps[i][1] + 0.42
    x1, y1 = steps[i + 1][0] - 1.0, steps[i + 1][1] - 0.42
    arrow(ax, (x0, y0), (x1, y1), color=C["muted"], lw=1.0, ls="--", shrink=2)

arrow(ax, (0.30, 0.55), (0.30, 4.6), color=C["ink"], lw=1.2)
ax.text(0.10, 2.55, "细节与计算成本增加", rotation=90, ha="center", va="center",
        fontsize=8.5, color=C["ink"])
arrow(ax, (0.30, 0.35), (9.8, 0.35), color=C["muted"], lw=1.0)
ax.text(5.0, 0.12, "覆盖的行为范围变窄", ha="center", va="center",
        fontsize=8.5, color=C["muted"])
save(fig, OUT, "fig01_ladder.png")
