import sys
import pathlib

import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "common"))
from style import *  # noqa

OUT, _ = chapter_paths(__file__)

C_M, G_NA, G_K, G_L = 1.0, 120.0, 36.0, 0.3
E_NA, E_K, E_L = 50.0, -77.0, -54.4


def rates(v):
    am = 0.1 * (v + 40) / (1 - np.exp(-(v + 40) / 10))
    bm = 4 * np.exp(-(v + 65) / 18)
    ah = 0.07 * np.exp(-(v + 65) / 20)
    bh = 1 / (1 + np.exp(-(v + 35) / 10))
    an = 0.01 * (v + 55) / (1 - np.exp(-(v + 55) / 10))
    bn = 0.125 * np.exp(-(v + 65) / 80)
    return am, bm, ah, bh, an, bn


def hh_rhs(t, y, I):
    v, m, h, n = y
    i_na = G_NA * m ** 3 * h * (v - E_NA)
    i_k = G_K * n ** 4 * (v - E_K)
    i_l = G_L * (v - E_L)
    am, bm, ah, bh, an, bn = rates(v)
    return [(I - i_na - i_k - i_l) / C_M,
            am * (1 - m) - bm * m,
            ah * (1 - h) - bh * h,
            an * (1 - n) - bn * n]


def run(I, T=300.0):
    v0 = -65.0
    am, bm, ah, bh, an, bn = rates(v0)
    y0 = [v0, am / (am + bm), ah / (ah + bh), an / (an + bn)]
    sol = solve_ivp(hh_rhs, (0, T), y0, args=(I,), max_step=0.02, rtol=1e-6)
    return sol.t, sol.y[0]


def spike_rate(I):
    t, v = run(I, 400)
    mask = t > 200
    v, t = v[mask], t[mask]
    peaks = np.where((v[:-1] < 0) & (v[1:] >= 0))[0]
    return len(peaks) / ((t[-1] - t[0]) / 1000.0) if len(peaks) else 0.0


currents = np.linspace(0, 20, 41)
freqs = [spike_rate(I) for I in currents]

fig, ax = plt.subplots(figsize=(6.2, 3.2))
ax.plot(currents, freqs, "o-", color=C["blue"], ms=3.0, lw=1.1)
ax.set_xlabel("注入电流 (微安/平方厘米)")
ax.set_ylabel("放电频率 (Hz)")
ax.set_xlim(0, 20)
ax.set_ylim(0, 100)
ax.grid(color=C["grid"], lw=0.6, alpha=0.7)
ax.set_axisbelow(True)
ax.annotate("基强度之后\n频率突然跳起", xy=(6.4, 52), xytext=(9.2, 18),
            fontsize=7.8, color=C["muted"],
            arrowprops=dict(arrowstyle="-|>", color=C["muted"], lw=0.8))

inset = ax.inset_axes([0.08, 0.12, 0.34, 0.30])
t, v = run(12.0, 80.0)
inset.plot(t, v, color=C["orange"], lw=0.8)
inset.set_xlim(0, 80)
inset.set_ylim(-80, 60)
inset.set_xticks([])
inset.set_yticks([-60, 40])
inset.tick_params(labelsize=6.5, length=2)
inset.set_title("电流 12 时的放电", fontsize=7, pad=2)
fig.tight_layout()
save(fig, OUT, "fig01_fi_rate.png")
