"""
generar_figuras.py
Genera las figuras PNG para clase1/img/
Basado en el apunte de Ballario — La Estática Aplicada (UTN FRLP)
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patheffects as pe
from matplotlib.patches import FancyArrowPatch, Arc
import os

# ── Configuración global ────────────────────────────────────────────────────
OUT_DIR = "clase1/img"
os.makedirs(OUT_DIR, exist_ok=True)

STYLE = {
    "force":     {"color": "#1a1a2e", "lw": 2.0},
    "resultant": {"color": "#e63946", "lw": 2.5},
    "component": {"color": "#457b9d", "lw": 1.8},
    "aux":       {"color": "#6c757d", "lw": 1.2, "ls": "--"},
    "moment":    {"color": "#2d6a4f", "lw": 1.8},
    "pair":      {"color": "#6a0572", "lw": 1.8},
    "bg":        "#f8f9fa",
    "grid":      "#dee2e6",
    "text":      "#1a1a2e",
    "fontsize":  11,
    "dpi":       150,
    "figsize":   (7, 5),
}

def save(fig, name):
    path = os.path.join(OUT_DIR, f"{name}.png")
    fig.savefig(path, dpi=STYLE["dpi"], bbox_inches="tight",
                facecolor="#f8f9fa")
    plt.close(fig)
    print(f"  ✓ {path}")

def arrow(ax, x0, y0, dx, dy, **kwargs):
    defaults = dict(head_width=0.12, head_length=0.18,
                    length_includes_head=True, fc=kwargs.get("color", "k"),
                    ec=kwargs.get("color", "k"), lw=kwargs.get("lw", 1.5),
                    zorder=3)
    defaults.update({k: v for k, v in kwargs.items()
                     if k not in ("color", "lw")})
    ax.arrow(x0, y0, dx, dy, **defaults)

def label(ax, x, y, txt, ha="center", va="center", size=None, color=None):
    ax.text(x, y, txt, ha=ha, va=va,
            fontsize=size or STYLE["fontsize"],
            color=color or "#1a1a2e",
            fontfamily="DejaVu Sans")

def setup_ax(ax, xlim, ylim, title="", grid=True):
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect("equal")
    ax.set_facecolor("#f8f9fa")
    if grid:
        ax.grid(True, color="#dee2e6", lw=0.6, zorder=0)
    ax.set_axisbelow(True)
    if title:
        ax.set_title(title, fontsize=STYLE["fontsize"] + 1,
                     color="#1a1a2e", pad=8)
    ax.tick_params(left=False, bottom=False,
                   labelleft=False, labelbottom=False)
    for spine in ax.spines.values():
        spine.set_visible(False)

# ── 01 · Representación de una fuerza -──────────────────────────────────────
def fig_fuerza():
    fig, ax = plt.subplots(figsize=STYLE["figsize"])
    setup_ax(ax, (-0.5, 6.5), (-0.5, 4.0),
             "Representación gráfica de una fuerza")

    import numpy as np

    # ── geometría base ───────────────────────────────────────────────────────
    Ax, Ay = 1.0, 1.0   # punto de aplicación A
    dx, dy = 3.0, 1.5   # vector P (sobre la recta de acción)
    Bx, By = Ax + dx, Ay + dy

    length = np.hypot(dx, dy)
    ux, uy = dx / length, dy / length          # unitario paralelo
    nx, ny = -uy, ux                           # unitario normal (izq.)

    # ── recta de acción (extendida a ambos lados) ────────────────────────────
    ext = 1.2
    ax.plot([Ax - ux * ext, Bx + ux * ext],
            [Ay - uy * ext, By + uy * ext],
            color="#dee2e6", lw=1.2, ls="--", zorder=1)
    label(ax, Bx + ux * ext + 0.2, By + uy * ext + 0.1,
          "$n{-}n$", size=10, color="#adb5bd")

    # ── vector fuerza (sobre la recta de acción) ─────────────────────────────
    c = "#1a1a2e"
    arrow(ax, Ax, Ay, dx, dy, color=c, lw=2)

    ax.plot(Ax, Ay, "o", color=c, ms=7, zorder=4)
    label(ax, Ax - 0.25, Ay - 0.25, "$A$", size=12)

    ax.plot(Bx, By, "o", color=c, ms=5, mfc="white", zorder=4)
    label(ax, Bx + 0.15, By + 0.15, "$B$", size=12)

    label(ax, Ax + dx * 0.55 + 0.15, Ay + dy * 0.55 + 0.1,
          "$P$", size=14, color=c)

    # ── cota desplazada (paralela al vector, offset perpendicular) ───────────
    offset = 0.55
    ox, oy = nx * offset, ny * offset

    # líneas de referencia desde A y B hacia la cota
    for px, py in [(Ax, Ay), (Bx, By)]:
        ax.plot([px, px + ox * 1.25],
                [py, py + oy * 1.25],
                color="#457b9d", lw=0.8, ls=":", zorder=2)

    # flecha doble de cota
    cx0, cy0 = Ax + ox, Ay + oy
    cx1, cy1 = Bx + ox, By + oy
    ax.annotate("", xy=(cx1, cy1), xytext=(cx0, cy0),
                arrowprops=dict(arrowstyle="<->", color="#457b9d",
                                lw=1.4, mutation_scale=12))

    # etiqueta de cota (desplazada otro poco en la normal)
    mx, my = (cx0 + cx1) / 2 + ox * 0.7, (cy0 + cy1) / 2 + oy * 0.7
    label(ax, mx, my,
          "$|AB| = 3\\,\\mathrm{t}$\n$EF = 1\\,\\mathrm{t/cm}$",
          size=10, color="#457b9d")

    # ── leyenda ──────────────────────────────────────────────────────────────
    props = dict(boxstyle="round,pad=0.3", facecolor="white",
                 edgecolor="#dee2e6", alpha=0.9)
    ax.text(0.02, 0.97,
            "a) Módulo: $|AB|$\nb) Dirección: recta $n{-}n$\n"
            "c) Sentido: flecha\nd) Punto de aplicación: $A$",
            transform=ax.transAxes, va="top", ha="left",
            fontsize=9, color="#1a1a2e", bbox=props)

    save(fig, "01_fuerza_representacion")

# ── 02 · Clasificación de fuerzas ───────────────────────────────────────────


def fig_clasificacion():
    fig, axes = plt.subplots(2, 2, figsize=(10, 8))
    titles = ["Colineales", "Concurrentes", "No concurrentes", "Paralelas"]

    for ax, title in zip(axes.flat, titles):
        setup_ax(ax, (-1, 4), (-1, 4), title, grid=False)
        ax.set_facecolor("#f8f9fa")

    c = "#1a1a2e"

    # ── Colineales ───────────────────────────────────────────────────────────
    ax = axes[0, 0]
    ax.axhline(1.5, color="#dee2e6", lw=1, ls="--", zorder=0)
    arrow(ax, 0, 1.5, 1.5, 0, color=c, lw=2)
    arrow(ax, 2, 1.5, 1.5, 0, color=c, lw=2)
    label(ax, 0.7, 1.9, "$P_1$", size=12)
    label(ax, 2.7, 1.9, "$P_2$", size=12)

    # ── Concurrentes ─────────────────────────────────────────────────────────
    ax = axes[0, 1]
    O = (1.5, 1.5)
    forces = [(1.5, 0.8), (1.2, -0.8), (-1.2, 0.8), (0.8, -1.2)]
    lbls = ["$P_1$", "$P_2$", "$P_3$", "$P_4$"]
    for (dx, dy), lbl in zip(forces, lbls):
        arrow(ax, O[0], O[1], dx, dy, color=c, lw=1.8)
        label(ax, O[0] + dx + 0.15, O[1] + dy + 0.1, lbl, size=11)
    ax.plot(*O, "o", color=c, ms=7, zorder=5)
    label(ax, O[0] - 0.3, O[1] - 0.25, "$O$", size=11)

    # ── No concurrentes ──────────────────────────────────────────────────────
    ax = axes[1, 0]
    import numpy as np
    nc_forces = [
        (0.2,  0.3,  1.2,  1.0),
        (2.8,  0.2, -0.5,  1.6),
        (0.1,  2.8,  1.8, -0.4),
        (2.5,  3.2,  0.8, -1.8),
    ]
    nc_lbls = ["$P_1$", "$P_2$", "$P_3$", "$P_4$"]
    for (x0, y0, dx, dy), lbl in zip(nc_forces, nc_lbls):
        length = np.hypot(dx, dy)
        ux, uy = dx / length, dy / length
        ax.plot([x0 - ux * 0.3, x0 + dx + ux * 0.3],
                [y0 - uy * 0.3, y0 + dy + uy * 0.3],
                color="#dee2e6", lw=1, ls="--", zorder=1)
        arrow(ax, x0, y0, dx, dy, color=c, lw=1.8)
        label(ax, x0 + dx + 0.15, y0 + dy + 0.1, lbl, size=11)

    # ── Paralelas ────────────────────────────────────────────────────────────
    ax = axes[1, 1]
    xs = [0.5, 1.5, 2.8]
    for i, x in enumerate(xs):
        arrow(ax, x, 0.3, 0, 2.0, color=c, lw=2)
        label(ax, x + 0.2, 2.5, f"$P_{i+1}$", size=11)

    fig.suptitle("Clasificación de fuerzas según su recta de acción",
                 fontsize=13, color="#1a1a2e")
    fig.tight_layout()
    save(fig, "02_clasificacion_fuerzas")


# ── 03 · Principio del paralelogramo ────────────────────────────────────────
def fig_paralelogramo():
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.5))

    for ax in axes:
        setup_ax(ax, (-0.3, 4.5), (-0.3, 3.5), grid=False)

    # Paralelogramo completo
    ax = axes[0]
    ax.set_title("Principio del paralelogramo", fontsize=11,
                 color="#1a1a2e")
    O = (0.3, 0.3)
    P1 = (3.0, 0.0)
    P2 = (1.0, 2.5)
    R  = (P1[0] + P2[0], P1[1] + P2[1])

    # lados del paralelogramo
    ax.plot([O[0], O[0]+P1[0], O[0]+R[0], O[0]+P2[0], O[0]],
            [O[1], O[1]+P1[1], O[1]+R[1], O[1]+P2[1], O[1]],
            color="#dee2e6", lw=1.2, ls="--", zorder=1)

    arrow(ax, *O, *P1, color="#1a1a2e", lw=2)
    arrow(ax, *O, *P2, color="#1a1a2e", lw=2)
    arrow(ax, *O, *R,  color="#e63946", lw=2.5)

    label(ax, O[0]+P1[0]/2+0.1, O[1]+P1[1]/2-0.25, "$P_1$", size=12)
    label(ax, O[0]+P2[0]/2-0.3, O[1]+P2[1]/2,      "$P_2$", size=12)
    label(ax, O[0]+R[0]/2+0.2,  O[1]+R[1]/2+0.15,  "$R$",
          size=13, color="#e63946")
    ax.plot(*O, "o", color="#1a1a2e", ms=7, zorder=5)
    label(ax, O[0]-0.2, O[1]-0.2, "$A$", size=11)

    # Triángulo de fuerzas
    ax = axes[1]
    ax.set_title("Triángulo de fuerzas", fontsize=11, color="#1a1a2e")
    O2 = (0.3, 0.8)
    arrow(ax, *O2, *P1, color="#1a1a2e", lw=2)
    tip1 = (O2[0]+P1[0], O2[1]+P1[1])
    arrow(ax, *tip1, *P2, color="#1a1a2e", lw=2)
    arrow(ax, *O2, R[0], R[1], color="#e63946", lw=2.5)

    label(ax, O2[0]+P1[0]/2, O2[1]-0.25, "$P_1$", size=12)
    label(ax, tip1[0]+P2[0]/2+0.2, tip1[1]+P2[1]/2, "$P_2$", size=12)
    label(ax, O2[0]+R[0]/2-0.3, O2[1]+R[1]/2+0.15, "$R$",
          size=13, color="#e63946")

    fig.tight_layout()
    save(fig, "03_paralelogramo")

# ── 04 · Componentes cartesianas ────────────────────────────────────────────
def fig_componentes():
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.5))

    angles = [53, 130]
    titles = [f"$\\varphi = {a}°$ — Cuadrante {'I' if a < 90 else 'II'}"
              for a in angles]

    for ax, phi_deg, title in zip(axes, angles, titles):
        setup_ax(ax, (-3, 4), (-1, 4), title)
        phi = np.radians(phi_deg)
        P = 3.0
        Px = P * np.cos(phi)
        Py = P * np.sin(phi)

        # ejes
        ax.axhline(0, color="#1a1a2e", lw=1.0, zorder=2)
        ax.axvline(0, color="#1a1a2e", lw=1.0, zorder=2)
        label(ax,  3.7, 0.15, "$x$", size=11)
        label(ax,  0.2, 3.8,  "$y$", size=11)

        # componentes (líneas punteadas)
        ax.plot([0, Px], [0, 0],  color="#457b9d", lw=1.5,
                ls="--", zorder=2)
        ax.plot([Px, Px], [0, Py], color="#457b9d", lw=1.5,
                ls="--", zorder=2)
        ax.plot([0, 0], [0, Py],  color="#457b9d", lw=1.5,
                ls="--", zorder=2)
        ax.plot([0, Px], [Py, Py], color="#457b9d", lw=1.5,
                ls="--", zorder=2)

        # flechas componentes
        arrow(ax, 0, 0, Px, 0,  color="#457b9d", lw=2)
        arrow(ax, 0, 0, 0,  Py, color="#457b9d", lw=2)

        # fuerza resultante
        arrow(ax, 0, 0, Px, Py, color="#1a1a2e", lw=2.5)

        # ángulo arc
        arc = Arc((0, 0), 0.8, 0.8, angle=0,
                  theta1=0, theta2=phi_deg,
                  color="#2d6a4f", lw=1.5)
        ax.add_patch(arc)

        sign_x = "+" if Px >= 0 else "-"
        sign_y = "+"
        label(ax, Px/2, -0.35,
              f"$P_x = {sign_x}{abs(Px):.1f}\\,\\mathrm{{kN}}$",
              size=10, color="#457b9d")
        label(ax, -1.8 if Px < 0 else Px + 0.4, Py/2,
              f"$P_y = {sign_y}{abs(Py):.1f}\\,\\mathrm{{kN}}$",
              size=10, color="#457b9d")
        label(ax, Px/2 + 0.25, Py/2 + 0.25,
              f"$P = {P:.0f}\\,\\mathrm{{kN}}$",
              size=11, color="#1a1a2e")
        label(ax, 0.55, 0.22, f"$\\varphi={phi_deg}°$",
              size=9, color="#2d6a4f")

        ax.plot(0, 0, "o", color="#1a1a2e", ms=6, zorder=5)

    fig.suptitle("Representación analítica — componentes cartesianas",
                 fontsize=12, color="#1a1a2e")
    fig.tight_layout()
    save(fig, "04_componentes_cartesianas")

# ── 05 · Momento estático ────────────────────────────────────────────────────
def fig_momento():
    fig, ax = plt.subplots(figsize=(5, 7))
    setup_ax(ax, (-1, 6), (-1, 4.5), "Momento estático de una fuerza")

    # ── geometría base ────────────────────────────────────────────────────────
    phi = np.radians(25)
    Ax, Ay = 1.2, 0.8          # punto de aplicación A (más a la izquierda)
    Pmag = 3.5
    Px = Pmag * np.cos(phi)
    Py = -Pmag * np.sin(phi)   # apunta abajo-derecha
    Bx, By = Ax + Px, Ay + Py

    length = np.hypot(Px, Py)
    ux, uy = Px / length, Py / length    # unitario paralelo a P
    nx, ny = -uy,  ux                    # normal (hacia arriba-izquierda)

    # ── recta de acción extendida (pasa por A y B, se extiende a ambos lados) ─
    ext = 1.8
    ax.plot([Ax - ux * ext, Bx + ux * ext],
            [Ay - uy * ext, By + uy * ext],
            color="#dee2e6", lw=1.2, ls="--", zorder=1)

    # ── vector fuerza P (de A a B, sobre la recta de acción) ─────────────────
    arrow(ax, Ax, Ay, Px, Py, color="#1a1a2e", lw=2.2)

    ax.plot(Ax, Ay, "o", color="#1a1a2e", ms=7, zorder=5)
    label(ax, Ax - 0.28, Ay + 0.18, "$A$", size=12)

    ax.plot(Bx, By, "o", color="#1a1a2e", ms=5, mfc="white", zorder=5)
    label(ax, Bx + 0.15, By - 0.25, "$B$", size=12)

    label(ax, Ax + Px * 0.6 + 0.2, Ay + Py * 0.6 - 0.15,
          "$P$", size=14, color="#1a1a2e")

    # ── centro de momentos O ──────────────────────────────────────────────────
    Cx, Cy = 1.0, 3.2
    ax.plot(Cx, Cy, "s", color="#2d6a4f", ms=9, zorder=5)
    label(ax, Cx - 0.38, Cy + 0.18, "$O$", size=12, color="#2d6a4f")

    # ── pie de perpendicular (foot) sobre la recta de acción ──────────────────
    u = np.array([ux, uy])
    A_pt = np.array([Ax, Ay])
    C_pt = np.array([Cx, Cy])
    t_foot = np.dot(C_pt - A_pt, u)
    foot = A_pt + t_foot * u          # garantizado sobre la recta de acción

    # línea brazo d: de O al foot
    ax.plot([Cx, foot[0]], [Cy, foot[1]],
            color="#2d6a4f", lw=1.8, zorder=2)
    ax.plot(*foot, "o", color="#2d6a4f", ms=6, zorder=5)

    # ángulo recto en el foot
    s = 0.20
    n_vec = np.array([nx, ny])
    sq1 = foot + n_vec * s
    sq2 = foot + n_vec * s + u * s
    sq3 = foot + u * s
    ax.plot([sq1[0], sq2[0], sq3[0]],
            [sq1[1], sq2[1], sq3[1]],
            color="#2d6a4f", lw=1.2, zorder=3)

    # etiqueta d
    mid_d = (Cx + foot[0]) / 2, (Cy + foot[1]) / 2
    label(ax, mid_d[0] - 0.35, mid_d[1] + 0.1, "$d$", size=13,
          color="#2d6a4f")

    # ── arco de momento con flecha ────────────────────────────────────────────
    r = 0.78
    arc = Arc((Cx, Cy), r * 2, r * 2, angle=0,
              theta1=200, theta2=315,
              color="#2d6a4f", lw=2, zorder=4)
    ax.add_patch(arc)

    # flecha en theta=255° (lado izquierdo del arco)
    t_tip = np.radians(255)
    tip = np.array([Cx + r * np.cos(t_tip), Cy + r * np.sin(t_tip)])
    tang = np.array([-np.sin(t_tip), np.cos(t_tip)])   # tangente antihoraria
    before = tip - tang * 0.20
    ax.annotate("", xy=tuple(tip), xytext=tuple(before),
                arrowprops=dict(arrowstyle="-|>", color="#2d6a4f",
                                lw=1.5, mutation_scale=14),
                zorder=5)

    label(ax, Cx + 0.9, Cy - 0.6, "$(+)$", size=10, color="#2d6a4f")

    # ── fórmula ───────────────────────────────────────────────────────────────
    ax.text(3.2, 3.8, "$M = P \\times d$\n$[\\mathrm{kN \\cdot m}]$",
            fontsize=12, color="#2d6a4f",
            bbox=dict(boxstyle="round", facecolor="white",
                      edgecolor="#2d6a4f", alpha=0.9))

    save(fig, "05_momento_estatico")

# ── 06 · Teorema de Varignon ─────────────────────────────────────────────────
def fig_varignon():
    fig, ax = plt.subplots(figsize=STYLE["figsize"])
    setup_ax(ax, (-0.5, 6), (-0.5, 5),
             "Teorema de Varignon: $M_R^O = \\sum M_{P_i}^O$")

    # punto O
    Ox, Oy = 0.5, 4.0
    ax.plot(Ox, Oy, "s", color="#2d6a4f", ms=9, zorder=5)
    label(ax, Ox - 0.3, Oy + 0.2, "$O$", size=12,
          color="#2d6a4f")

    # punto de concurrencia A
    Ax, Ay = 2.5, 1.5
    ax.plot(Ax, Ay, "o", color="#1a1a2e", ms=7, zorder=5)
    label(ax, Ax - 0.25, Ay - 0.3, "$A$", size=11)

    # P1 y P2
    forces = [(2.0, 0.3), (1.0, 2.2)]
    colors_ = ["#1a1a2e", "#457b9d"]
    labels_ = ["$P_1$", "$P_2$"]
    R = (sum(f[0] for f in forces), sum(f[1] for f in forces))

    for (dx, dy), c, lbl in zip(forces, colors_, labels_):
        arrow(ax, Ax, Ay, dx, dy, color=c, lw=2)
        label(ax, Ax + dx + 0.2, Ay + dy + 0.1, lbl, size=12, color=c)

    # resultante
    arrow(ax, Ax, Ay, *R, color="#e63946", lw=2.5)
    label(ax, Ax + R[0]/2 + 0.2, Ay + R[1]/2 + 0.2, "$R$",
          size=13, color="#e63946")

    # brazos de palanca (líneas desde O a rectas de acción)
    for (dx, dy), c in zip(forces + [R], colors_ + ["#e63946"]):
        phi = np.arctan2(dy, dx)
        u = np.array([np.cos(phi), np.sin(phi)])
        n_vec = np.array([-np.sin(phi), np.cos(phi)])
        A_pt = np.array([Ax, Ay])
        C_pt = np.array([Ox, Oy])
        t_f = np.dot(C_pt - A_pt, u)
        foot = A_pt + t_f * u
        ax.plot([Ox, foot[0]], [Oy, foot[1]],
                color=c, lw=1.2, ls=":", zorder=2, alpha=0.7)

    # fórmula
    ax.text(3.8, 3.8,
            "$M_R^O = M_{P_1}^O + M_{P_2}^O$\n"
            "$R \\cdot d_R = P_1 d_1 + P_2 d_2$",
            fontsize=10, color="#1a1a2e",
            bbox=dict(boxstyle="round", facecolor="white",
                      edgecolor="#dee2e6", alpha=0.9))

    save(fig, "06_varignon")

# ── 07 · Par de fuerzas ──────────────────────────────────────────────────────
def fig_par():
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.5))

    # Par básico
    ax = axes[0]
    setup_ax(ax, (-0.5, 4), (-0.5, 4), "Par de fuerzas: $M = P \\times d$")
    x1, x2 = 0.8, 3.0
    y  = 1.8
    d  = x2 - x1

    ax.axvline(x1, color="#dee2e6", lw=1, ls="--", ymin=0.1, ymax=0.9)
    ax.axvline(x2, color="#dee2e6", lw=1, ls="--", ymin=0.1, ymax=0.9)

    arrow(ax, x1, 0.4, 0, 2.2,  color="#6a0572", lw=2)
    arrow(ax, x2, 2.9, 0, -2.2, color="#6a0572", lw=2)

    ax.plot(x1, 0.4, "o", color="#6a0572", ms=6, zorder=5)
    ax.plot(x2, 2.9, "o", color="#6a0572", ms=6, zorder=5)

    label(ax, x1 - 0.3, 1.5, "$P$", size=13, color="#6a0572")
    label(ax, x2 + 0.3, 1.5, "$P$", size=13, color="#6a0572")

    # brazo d
    ax.annotate("", xy=(x2, 0.2), xytext=(x1, 0.2),
                arrowprops=dict(arrowstyle="<->", color="#2d6a4f", lw=1.5))
    label(ax, (x1 + x2) / 2, -0.1, "$d$", size=12,
          color="#2d6a4f")

    # sentido de giro
    arc = Arc((1.9, 1.8), 1.0, 1.0, angle=0,
              theta1=300, theta2=60,
              color="#2d6a4f", lw=2)
    ax.add_patch(arc)

    # punta de flecha para giro horario
    t_tip = np.radians(60)
    tip = np.array([1.9 + 0.5 * np.cos(t_tip),
                    1.8 + 0.5 * np.sin(t_tip)])
    tang = np.array([np.sin(t_tip), -np.cos(t_tip)])  # tangente horario
    before = tip - tang * 0.18
    ax.annotate("", xy=tuple(tip), xytext=tuple(before),
                arrowprops=dict(arrowstyle="-|>", color="#2d6a4f",
                                lw=1.5, mutation_scale=14),
                zorder=5)

    label(ax, 1.9, 1.8, "$(-)$", size=10, color="#2d6a4f")

    ax.text(0.1, 3.5, "$M = P \\times d$", fontsize=12,
            color="#6a0572",
            bbox=dict(boxstyle="round", facecolor="white",
                      edgecolor="#6a0572", alpha=0.9))

    # Propiedad: mismo M, distintos P y d
    ax = axes[1]
    setup_ax(ax, (-0.5, 5), (-0.5, 4.5),
             "Propiedad: $M = P_1 d_1 = P_2 d_2$")

    pairs = [
        (0.6, 0.6 + 1.5, 1.8, 0.8, "#6a0572"),  # P1 mayor, d1 menor
        (0.6, 0.6 + 3.0, 0.9, 2.8, "#457b9d"),  # P2 menor, d2 mayor
    ]

    for i, (x1_, x2_, mag, yp, cp) in enumerate(pairs, start=1):
        arrow(ax, x1_, yp, 0, mag, color=cp, lw=2)
        arrow(ax, x2_, yp + mag, 0, -mag, color=cp, lw=2)

        ax.annotate("", xy=(x2_, yp - 0.15), xytext=(x1_, yp - 0.15),
                    arrowprops=dict(arrowstyle="<->", color=cp, lw=1.2))

        label(ax, (x1_ + x2_) / 2, yp - 0.35,
              f"$d_{{{i}}}$", size=11, color=cp)
        label(ax, x1_ - 0.35, yp + mag / 2,
              f"$P_{{{i}}}$", size=11, color=cp)

    ax.text(3.2, 1.5,
            "$P_1 d_1 = P_2 d_2$\n$M$ invariante",
            fontsize=10, color="#1a1a2e",
            bbox=dict(boxstyle="round", facecolor="white",
                      edgecolor="#dee2e6", alpha=0.9))

    fig.suptitle("Par de fuerzas", fontsize=12, color="#1a1a2e")
    fig.tight_layout()
    save(fig, "07_par_fuerzas")

# ── 08 · Traslación de fuerzas ───────────────────────────────────────────────
def fig_traslacion():
    fig, axes = plt.subplots(1, 3, figsize=(13, 4.5))
    titles = ["Sistema original",
              "Agregar sistema nulo en $B$",
              "Equivalente: $P'$ + par $M$"]

    Ay, By = 1.5, 1.5
    Ax, Bx = 0.8, 3.5
    Pmag = 2.0
    d = By - Ay  # horizontal distance used for M label

    for ax, title in zip(axes, titles):
        setup_ax(ax, (0, 5), (0, 4), title, grid=False)
        ax.set_facecolor("#f8f9fa")
        # puntos A y B
        ax.plot(Ax, Ay, "o", color="#1a1a2e", ms=7, zorder=5)
        ax.plot(Bx, By, "o", color="#1a1a2e", ms=7, zorder=5)
        label(ax, Ax - 0.2, Ay - 0.3, "$A$", size=11)
        label(ax, Bx + 0.1, By - 0.3, "$B$", size=11)
        # distancia d
        ax.annotate("", xy=(Bx, 0.4), xytext=(Ax, 0.4),
                    arrowprops=dict(arrowstyle="<->",
                                   color="#2d6a4f", lw=1.2))
        label(ax, (Ax + Bx) / 2, 0.15, "$d$", size=11,
              color="#2d6a4f")

    # Sistema original: P en A
    ax = axes[0]
    arrow(ax, Ax, Ay, 0, Pmag, color="#1a1a2e", lw=2.2)
    label(ax, Ax + 0.2, Ay + Pmag / 2, "$P$", size=13,
          color="#1a1a2e")

    # Sistema nulo en B
    ax = axes[1]
    arrow(ax, Ax, Ay, 0, Pmag,  color="#1a1a2e", lw=2.2)
    arrow(ax, Bx, By, 0, Pmag,  color="#457b9d", lw=2,
          head_width=0.1)
    arrow(ax, Bx, By + Pmag, 0, -Pmag, color="#6a0572", lw=2,
          head_width=0.1)
    label(ax, Ax + 0.2, Ay + Pmag/2, "$P$",  size=13,
          color="#1a1a2e")
    label(ax, Bx + 0.2, By + Pmag/2, "$P'$", size=13,
          color="#457b9d")
    label(ax, Bx - 0.4, By + Pmag*1.1, "$-P'$", size=11,
          color="#6a0572")
    # par indicado con llave
    ax.annotate("", xy=(Bx - 0.1, By), xytext=(Ax + 0.1, Ay + Pmag),
                arrowprops=dict(arrowstyle="-", color="#6a0572",
                                lw=1, ls="dotted"))

    # Equivalente
    ax = axes[2]
    arrow(ax, Bx, By, 0, Pmag, color="#457b9d", lw=2.2)
    label(ax, Bx + 0.2, By + Pmag/2, "$P'$", size=13,
          color="#457b9d")
    # par (arco)
    arc = Arc((Bx, By + Pmag/2), 0.9, 0.9, angle=0,
              theta1=60, theta2=300,
              color="#6a0572", lw=2.2)
    ax.add_patch(arc)
    label(ax, Bx - 0.7, By + Pmag/2, "$M = P\\!\\cdot\\!d$",
          size=10, color="#6a0572")

    fig.suptitle("Traslación de una fuerza a otro punto",
                 fontsize=12, color="#1a1a2e")
    fig.tight_layout()
    save(fig, "08_traslacion_fuerza")

# ── 09 · Polígono de fuerzas ─────────────────────────────────────────────────
def fig_poligono():
    fig, axes = plt.subplots(1, 2, figsize=(11, 5))

    forces = [
        np.array([2.0,  0.5]),
        np.array([0.5,  2.0]),
        np.array([-1.0, 1.0]),
        np.array([0.8, -1.5]),
    ]
    labels_ = ["$P_1$", "$P_2$", "$P_3$", "$P_4$"]
    cols = ["#1a1a2e", "#457b9d",
            "#6a0572", "#2d6a4f"]

    # Sistema de fuerzas concurrentes
    ax = axes[0]
    setup_ax(ax, (-2.5, 4), (-2, 4),
             "Sistema de fuerzas concurrentes", grid=False)
    O = np.array([0.5, 0.5])
    ax.plot(*O, "o", color="k", ms=8, zorder=5)
    label(ax, O[0] - 0.2, O[1] - 0.3, "$O$", size=11)
    R = sum(forces)
    for f, lbl, c in zip(forces, labels_, cols):
        arrow(ax, *O, *f, color=c, lw=2)
        label(ax, O[0] + f[0] + 0.2, O[1] + f[1] + 0.1, lbl,
              size=11, color=c)
    arrow(ax, *O, *R, color="#e63946", lw=2.5)
    label(ax, O[0] + R[0]/2 + 0.15, O[1] + R[1]/2 + 0.15,
          "$R$", size=13, color="#e63946")

    # Polígono de fuerzas
    ax = axes[1]
    setup_ax(ax, (-3, 4.5), (-2.5, 4.5), "Polígono de fuerzas", grid=False)
    start = np.array([-1.5, -1.5])
    cur = start.copy()
    for f, lbl, c in zip(forces, labels_, cols):
        arrow(ax, *cur, *f, color=c, lw=2)
        label(ax, cur[0] + f[0]/2 + 0.15, cur[1] + f[1]/2 + 0.1,
              lbl, size=11, color=c)
        cur = cur + f
    # resultante
    arrow(ax, *start, *(cur - start),
          color="#e63946", lw=2.5)
    label(ax, start[0] + R[0]/2 - 0.4, start[1] + R[1]/2,
          "$R$", size=13, color="#e63946")

    ax.text(0.02, 0.02,
            "Origen → extremo del último = $R$\n"
            "Si cierra → equilibrio",
            transform=ax.transAxes, fontsize=9,
            color="#1a1a2e",
            bbox=dict(boxstyle="round", facecolor="white",
                      edgecolor="#dee2e6", alpha=0.9))

    fig.suptitle("Reducción de fuerzas concurrentes — método gráfico",
                 fontsize=12, color="#1a1a2e")
    fig.tight_layout()
    save(fig, "09_poligono_fuerzas")

# ── 10 · Descomposición en dos direcciones ───────────────────────────────────
def fig_descomposicion():
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.5))

    P_mag = 3.5
    phi = np.radians(50)

    # Descomposición cartesiana
    ax = axes[0]
    setup_ax(ax, (-0.5, 4.5), (-0.5, 4),
             "Descomposición cartesiana ($\\varphi_1 \\perp \\varphi_2$)")
    Px = P_mag * np.cos(phi)
    Py = P_mag * np.sin(phi)
    ax.axhline(0, color="#1a1a2e", lw=1)
    ax.axvline(0, color="#1a1a2e", lw=1)
    ax.plot([Px, Px], [0, Py], color="#457b9d", lw=1.2, ls="--")
    ax.plot([0, Px], [Py, Py], color="#457b9d", lw=1.2, ls="--")
    arrow(ax, 0, 0, Px, 0,  color="#457b9d", lw=2)
    arrow(ax, 0, 0, 0,  Py, color="#457b9d", lw=2)
    arrow(ax, 0, 0, Px, Py, color="#1a1a2e", lw=2.5)
    label(ax, Px/2, -0.3, "$P_x = P\\cos\\varphi$", size=10,
          color="#457b9d")
    label(ax, -1.2, Py/2, "$P_y = P\\sin\\varphi$", size=10,
          color="#457b9d")
    label(ax, Px/2 + 0.3, Py/2 + 0.2, "$P$", size=13,
          color="#1a1a2e")
    arc = Arc((0, 0), 0.7, 0.7, theta1=0, theta2=np.degrees(phi),
              color="#2d6a4f", lw=1.5)
    ax.add_patch(arc)
    label(ax, 0.55, 0.18, "$\\varphi$", size=10,
          color="#2d6a4f")

    # Descomposición oblicua con la misma fuerza P
    ax = axes[1]
    setup_ax(ax, (-0.5, 5), (-0.5, 4.5),
             "Descomposición oblicua (regla del seno)")
    phi_P = phi
    phi_1 = np.radians(20)
    phi_2 = np.radians(110)
    alpha = phi_P - phi_1
    beta = phi_2 - phi_P
    denom = np.sin(alpha + beta)
    P1_mag = P_mag * np.sin(beta) / denom
    P2_mag = P_mag * np.sin(alpha) / denom

    Px_P = P_mag * np.cos(phi_P)
    Py_P = P_mag * np.sin(phi_P)
    Px_1 = P1_mag * np.cos(phi_1)
    Py_1 = P1_mag * np.sin(phi_1)
    Px_2 = P2_mag * np.cos(phi_2)
    Py_2 = P2_mag * np.sin(phi_2)

    O = np.array([0.5, 0.5])
    arrow(ax, *O, Px_P, Py_P,  color="#1a1a2e", lw=2.5)
    arrow(ax, *O, Px_1, Py_1,  color="#457b9d", lw=2)
    arrow(ax, *O, Px_2, Py_2,  color="#6a0572", lw=2)

    label(ax, O[0] + Px_P / 2 + 0.2, O[1] + Py_P / 2 + 0.15, "$P$",
          size=13, color="#1a1a2e")
    label(ax, O[0] + Px_1 + 0.2, O[1] + Py_1 + 0.1, "$P_1$",
          size=12, color="#457b9d")
    label(ax, O[0] + Px_2 - 0.4, O[1] + Py_2 + 0.1, "$P_2$",
          size=12, color="#6a0572")

    arc1 = Arc(tuple(O), 0.7, 0.7, theta1=np.degrees(phi_1),
               theta2=np.degrees(phi_P), color="#2d6a4f", lw=1.3)
    arc2 = Arc(tuple(O), 1.0, 1.0, theta1=np.degrees(phi_P),
               theta2=np.degrees(phi_2), color="#2d6a4f", lw=1.3)
    ax.add_patch(arc1)
    ax.add_patch(arc2)
    label(ax, O[0] + 0.6, O[1] + 0.35, "$\\alpha$", size=9,
          color="#2d6a4f")
    label(ax, O[0] + 0.3, O[1] + 0.8, "$\\beta$", size=9,
          color="#2d6a4f")

    ax.text(2.5, 0.1,
            "$\\dfrac{P}{\\sin(\\alpha+\\beta)} = "
            "\\dfrac{P_1}{\\sin\\beta} = \\dfrac{P_2}{\\sin\\alpha}$",
            fontsize=9, color="#1a1a2e",
            bbox=dict(boxstyle="round", facecolor="white",
                      edgecolor="#dee2e6", alpha=0.9))

    fig.suptitle("Descomposición de una fuerza",
                 fontsize=12, color="#1a1a2e")
    fig.tight_layout()
    save(fig, "10_descomposicion")

# ── 11 · Equilibrio de fuerzas concurrentes ──────────────────────────────────
def fig_equilibrio():
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.5))

    forces_open = [
        np.array([2.0,  0.5]),
        np.array([0.3,  2.0]),
        np.array([-1.5, 0.8]),
        np.array([0.5, -1.8]),
    ]
    forces_closed = forces_open.copy()
    R_open = sum(forces_open)
    # hacer que cierre: agregar fuerza de cierre
    forces_closed = forces_open + [-R_open]

    for ax, forces, title, closed in zip(
        axes,
        [forces_open, forces_closed],
        ["Polígono abierto → $R \\neq 0$ (no equilibrio)",
         "Polígono cerrado → $R = 0$ (equilibrio)"],
        [False, True]
    ):
        setup_ax(ax, (-3, 4), (-3, 4), title, grid=False)
        cols = ["#1a1a2e", "#457b9d",
                "#6a0572", "#2d6a4f",
                "#e63946"]
        start = np.array([-1.0, -2.0])
        cur = start.copy()
        for i, (f, c) in enumerate(zip(forces, cols)):
            arrow(ax, *cur, *f, color=c, lw=2)
            cur = cur + f
        if not closed:
            # resultante
            arrow(ax, *start, *(cur - start),
                  color="#e63946", lw=2.5)
            label(ax, start[0]+(cur[0]-start[0])/2+0.2,
                  start[1]+(cur[1]-start[1])/2,
                  "$R$", size=13, color="#e63946")
        else:
            ax.plot(*start, "o", color="#e63946",
                    ms=10, zorder=6)
            label(ax, start[0]+0.15, start[1]+0.2,
                  "Cierra ✓", size=10,
                  color="#e63946")

    fig.suptitle("Condición gráfica de equilibrio de fuerzas concurrentes",
                 fontsize=12, color="#1a1a2e")
    fig.tight_layout()
    save(fig, "11_equilibrio_concurrentes")

# ── 12 · Terna global vs. local ──────────────────────────────────────────────
def fig_terna():
    fig, ax = plt.subplots(figsize=STYLE["figsize"])
    setup_ax(ax, (-2, 5), (-1.5, 4.5),
             "Terna global $(x,y)$ y terna local $(x',y')$")

    # terna global
    arrow(ax, 0, 0, 3.5, 0,   color="#1a1a2e", lw=1.5)
    arrow(ax, 0, 0, 0,   3.5, color="#1a1a2e", lw=1.5)
    label(ax, 3.8, 0.1,  "$x$",  size=12)
    label(ax, 0.1, 3.8,  "$y$",  size=12)

    # terna local rotada theta
    theta = np.radians(35)
    L = 3.0
    arrow(ax, 0, 0, L*np.cos(theta), L*np.sin(theta),
          color="#457b9d", lw=1.8)
    arrow(ax, 0, 0, -L*np.sin(theta), L*np.cos(theta),
          color="#457b9d", lw=1.8)
    label(ax, L*np.cos(theta)+0.2, L*np.sin(theta),    "$x'$", size=12,
          color="#457b9d")
    label(ax, -L*np.sin(theta)-0.3, L*np.cos(theta)+0.1, "$y'$", size=12,
          color="#457b9d")

    # ángulo theta
    arc = Arc((0, 0), 1.0, 1.0, theta1=0, theta2=35,
              color="#2d6a4f", lw=1.5)
    ax.add_patch(arc)
    label(ax, 0.65, 0.18, "$\\theta$", size=11,
          color="#2d6a4f")

    # fuerza P
    phi_P = np.radians(70)
    Pmag  = 2.5
    Px = Pmag * np.cos(phi_P)
    Py = Pmag * np.sin(phi_P)
    arrow(ax, 0, 0, Px, Py, color="#1a1a2e", lw=2.5)
    label(ax, Px+0.2, Py+0.1, "$P$", size=13,
          color="#1a1a2e")

    # componentes globales
    ax.plot([Px, Px], [0, Py], color="#1a1a2e",
            lw=1, ls=":", alpha=0.6)
    ax.plot([0, Px], [0, 0],   color="#1a1a2e",
            lw=1, ls=":", alpha=0.6)

    # fórmula rotación
    ax.text(1.5, -0.9,
            "$P_{x'} = P_x\\cos\\theta + P_y\\sin\\theta$\n"
            "$P_{y'} = -P_x\\sin\\theta + P_y\\cos\\theta$",
            fontsize=9, color="#1a1a2e",
            bbox=dict(boxstyle="round", facecolor="white",
                      edgecolor="#dee2e6", alpha=0.9))

    ax.plot(0, 0, "o", color="k", ms=7, zorder=5)

    save(fig, "12_terna_global_local")

# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Generando figuras en clase1/img/...")
    fig_fuerza()
    fig_clasificacion()
    fig_paralelogramo()
    fig_componentes()
    fig_momento()
    fig_varignon()
    fig_par()
    fig_traslacion()
    fig_poligono()
    fig_descomposicion()
    fig_equilibrio()
    fig_terna()
    print(f"\nListo — {len(os.listdir(OUT_DIR))} archivos en {OUT_DIR}/")
