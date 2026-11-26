import sys
import pathlib

import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "common"))
from style import *  # noqa

OUT, _ = chapter_paths(__file__)

# ---------- HH 仿真 ----------
C_M = 1.0
G_NA, G_K, G_L = 120.0, 36.0, 0.3
E_NA, E_K, E_L = 50.0, -77.0, -54.4


def am(v):
    return 0.1 * (v + 40) / (1 - np.exp(-(v + 40) / 10))


def bm(v):
    return 4 * np.exp(-(v + 65) / 18)


def ah(v):
    return 0.07 * np.exp(-(v + 65) / 20)


def bh(v):
    return 1 / (1 + np.exp(-(v + 35) / 10))


def an(v):
    return 0.01 * (v + 55) / (1 - np.exp(-(v + 55) / 10))


def bn(v):
    return 0.125 * np.exp(-(v + 65) / 80)


def x_inf(a, b):
    return a / (a + b)


def rhs(t, y):
    v, m, h, n = y
    i_ext = 20.0 if 5.0 <= t <= 6.0 else 0.0
    i_na = G_NA * m ** 3 * h * (v - E_NA)
    i_k = G_K * n ** 4 * (v - E_K)
    i_l = G_L * (v - E_L)
    dv = (i_ext - i_na - i_k - i_l) / C_M
    dm = am(v) * (1 - m) - bm(v) * m
    dh = ah(v) * (1 - h) - bh(v) * h
    dn = an(v) * (1 - n) - bn(v) * n
    return [dv, dm, dh, dn]


v0 = -65.0
y0 = [v0, x_inf(am(v0), bm(v0)), x_inf(ah(v0), bh(v0)), x_inf(an(v0), bn(v0))]
sol = solve_ivp(rhs, (0, 30), y0, max_step=0.01, dense_output=True)
tt = np.linspace(0, 30, 6000)
vv, mm, hh, nn = sol.sol(tt)

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6.4, 4.2), sharex=True,
                               gridspec_kw={"height_ratios": [1.35, 1]})
ax1.plot(tt, vv, color=C["blue"], lw=1.6)
ax1.axhline(-55, color=C["red"], lw=0.9, ls="--")
ax1.text(20.5, -52, "阈值", color=C["red"], fontsize=8.5, ha="left", va="bottom")
ax1.set_ylabel("膜电位 (mV)")
ax1.set_ylim(-85, 55)
ax1.annotate("动作电位", xy=(5.9, 35), xytext=(10.5, 38), fontsize=9,
             color=C["ink"], ha="left", va="center",
             arrowprops=dict(arrowstyle="-|>", color=C["muted"], lw=0.9))
ax1.annotate("超极化", xy=(8.2, -78), xytext=(14.0, -80), fontsize=9,
             color=C["ink"], ha="left", va="center",
             arrowprops=dict(arrowstyle="-|>", color=C["muted"], lw=0.9))

ax2.plot(tt, mm, color=C["blue"], lw=1.4, label="m 钠激活")
ax2.plot(tt, hh, color=C["orange"], lw=1.4, label="h 钠失活")
ax2.plot(tt, nn, color=C["teal"], lw=1.4, label="n 钾激活")
ax2.set_ylabel("门控变量")
ax2.set_xlabel("时间 (ms)")
ax2.set_ylim(-0.02, 1.05)
ax2.legend(loc="upper right", ncol=3, fontsize=8, handlelength=1.6, columnspacing=1.2)
for a in (ax1, ax2):
    a.grid(axis="y", color=C["grid"], lw=0.6, alpha=0.7)
    a.set_axisbelow(True)
fig.tight_layout()
save(fig, OUT, "fig01_action_potential.png")

# ---------- 突触后电位总和 ----------
dt = 0.01
T = 40.0
t = np.arange(0, T, dt)
EL, VT, VR = -70.0, -55.0, -75.0
tau_m, tau_s = 20.0, 5.0
E_syn, E_inh = 0.0, -80.0


def simulate(events, inhib_events=()):
    v = EL
    g_e = 0.0
    g_i = 0.0
    out = []
    spikes = []
    for ti in t:
        for te, ge in events:
            if abs(ti - te) < dt / 2:
                g_e += ge
        for te, gi in inhib_events:
            if abs(ti - te) < dt / 2:
                g_i += gi
        dv = (-(v - EL) + g_e * (E_syn - v) + g_i * (E_inh - v)) / tau_m
        v += dv * dt
        g_e += -g_e / tau_s * dt
        g_i += -g_i / tau_s * dt
        if v >= VT:
            spikes.append(ti)
            out.append(np.nan)
            v = VR
            continue
        out.append(v)
    return np.array(out), spikes


ev = [(3.0 + 4.0 * k, 0.55) for k in range(4)]
v_exc, sp1 = simulate(ev)
v_inh, sp2 = simulate(ev, [(3.0 + 4.0 * 2 + 1.5, 1.6)])

fig, ax = plt.subplots(figsize=(6.4, 3.1))
ax.plot(t, v_exc, color=C["blue"], lw=1.6, label="只有兴奋性输入")
ax.plot(t, v_inh, color=C["teal"], lw=1.6, ls="-", label="兴奋加抑制")
ax.axhline(VT, color=C["red"], lw=0.9, ls="--")
ax.text(38, VT + 1.2, "阈值", color=C["red"], fontsize=8.5, ha="right", va="bottom")
for ts in sp1:
    ax.axvline(ts, color=C["blue"], lw=0.8, ls=":", alpha=0.8)
ax.set_xlabel("时间 (ms)")
ax.set_ylabel("膜电位 (mV)")
ax.set_ylim(-78, -50)
ax.set_xlim(0, 40)
ax.legend(loc="lower right", fontsize=8.5)
ax.grid(axis="y", color=C["grid"], lw=0.6, alpha=0.7)
ax.set_axisbelow(True)
fig.tight_layout()
save(fig, OUT, "fig02_summation.png")
