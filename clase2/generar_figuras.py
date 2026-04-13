"""
generar_figuras_clase2.py
Genera las figuras PNG nuevas para clase2/img/
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, FancyArrowPatch
import os

OUT_DIR = "clase2/img"
os.makedirs(OUT_DIR, exist_ok=True)

STYLE = {
    "force":     "#1a1a2e",
    "resultant": "#e63946",
    "component": "#457b9d",
    "moment":    "#2d6a4f",
    "pair":      "#6a0572",
    "aux":       "#6c757d",
    "bg":        "#f8f9fa",
    "grid":      "#dee2e6",
    "fontsize":  11,
    "dpi":       150,
}

def save(fig, name):
    path = os.path.join(OUT_DIR, f"{name}.png")
    fig.savefig(path, dpi=STYLE["dpi"], bbox_inches="tight",
                facecolor=STYLE["bg"])
    plt.close(fig)
    print(f"  ✓ {path}")

def arrow(ax, x0, y0, dx, dy, color="#1a1a2e", lw=2.0, **kwargs):
    ax.arrow(x0, y0, dx, dy,
             head_width=0.12, head_length=0.16,
             length_includes_head=True,
             fc=color, ec=color, lw=lw, zorder=3, **kwargs)

def label(ax, x, y, txt, size=None, color=None, ha="center", va="center"):
    ax.text(x, y, txt, ha=ha, va=va,
            fontsize=size or STYLE["fontsize"],
            color=color or STYLE["force"],
            fontfamily="DejaVu Sans")

def setup_ax(ax, xlim, ylim, title="", grid=True):
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect("equal")
    ax.set_facecolor(STYLE["bg"])
    if grid:
        ax.grid(True, color=STYLE["grid"], lw=0.6, zorder=0)
    ax.set_axisbelow(True)
    if title:
        ax.set_title(title, fontsize=STYLE["fontsize"] + 1,
                     color=STYLE["force"], pad=8)
    ax.tick_params(left=False, bottom=False,
                   labelleft=False, labelbottom=False)
    for spine in ax.spines.values():
        spine.set_visible(False)

# ── 13 · Polígono funicular ───────────────────────────────────────────────────
def fig_funicular():
    fig, axes = plt.subplots(1, 2, figsize=(12, 5.5))

    # ── fuerzas del sistema ───────────────────────────────────────────────────
    # 4 fuerzas verticales no concurrentes sobre una línea horizontal
    forces_x = [0.5, 2.0, 3.5, 5.0]   # posiciones x
    forces_y = [0.0, 0.0, 0.0, 0.0]   # todas sobre y=0
    forces_dy = [1.8, 2.4, -1.2, 1.5] # magnitudes (+ hacia arriba, - hacia abajo)
    colors_f = [STYLE["force"], STYLE["component"],
                STYLE["pair"], STYLE["moment"]]
    lbls = ["$P_1$", "$P_2$", "$P_3$", "$P_4$"]

    # ── panel izquierdo: sistema de fuerzas ───────────────────────────────────
    ax = axes[0]
    setup_ax(ax, (-0.5, 6.5), (-2.5, 3.5), "Sistema de fuerzas", grid=False)

    # línea base (viga)
    ax.axhline(0, color=STYLE["grid"], lw=1.5, zorder=1)

    for x, dy, c, lbl in zip(forces_x, forces_dy, colors_f, lbls):
        arrow(ax, x, 0, 0, dy, color=c, lw=2)
        ylab = dy + 0.2 if dy > 0 else dy - 0.3
        label(ax, x + 0.2, ylab, lbl, color=c, size=11)
        ax.plot(x, 0, "o", color=c, ms=6, zorder=5)

    # resultante
    R_dy = sum(forces_dy)
    R_x  = sum(x * dy for x, dy in zip(forces_x, forces_dy)) / R_dy
    arrow(ax, R_x, 0, 0, R_dy, color=STYLE["resultant"], lw=2.5)
    label(ax, R_x + 0.3, R_dy / 2, "$R$",
          color=STYLE["resultant"], size=13)
    ax.plot(R_x, 0, "o", color=STYLE["resultant"], ms=8, zorder=5)

    ax.annotate("", xy=(R_x, -0.4), xytext=(0, -0.4),
                arrowprops=dict(arrowstyle="<->", color=STYLE["moment"], lw=1.2))
    label(ax, R_x / 2, -0.7, "$x_R$", color=STYLE["moment"], size=10)

    # ── panel derecho: polígono funicular ─────────────────────────────────────
    ax = axes[1]
    setup_ax(ax, (-1.0, 7.5), (-3.0, 4.0),
             "Polígono funicular", grid=False)

    # línea base
    ax.axhline(0, color=STYLE["grid"], lw=1.5, zorder=1)

    # dibujar fuerzas
    for x, dy, c, lbl in zip(forces_x, forces_dy, colors_f, lbls):
        arrow(ax, x, 0, 0, dy, color=c, lw=1.8)
        ylab = dy + 0.2 if dy > 0 else dy - 0.3
        label(ax, x + 0.18, ylab, lbl, color=c, size=10)

    # polígono de fuerzas (a la derecha)
    pf_x0, pf_y0 = 5.8, -1.0
    cum_dy = 0
    vertices = [(pf_x0, pf_y0)]
    for dy, c in zip(forces_dy, colors_f):
        arrow(ax, pf_x0, pf_y0 + cum_dy, 0, dy, color=c, lw=1.8)
        cum_dy += dy
        vertices.append((pf_x0, pf_y0 + cum_dy))

    # polo O
    pole = np.array([pf_x0 + 1.2, pf_y0 + cum_dy / 2])
    ax.plot(*pole, "s", color=STYLE["moment"], ms=8, zorder=6)
    label(ax, pole[0] + 0.25, pole[1], "$O$",
          color=STYLE["moment"], size=11)

    # rayos polares
    ray_colors = colors_f + [STYLE["resultant"]]
    for i, v in enumerate(vertices):
        ax.plot([pole[0], v[0]], [pole[1], v[1]],
                color=ray_colors[min(i, len(ray_colors)-1)],
                lw=0.9, ls="--", zorder=2, alpha=0.7)
        label(ax, (pole[0] + v[0]) / 2 + 0.15,
              (pole[1] + v[1]) / 2,
              str(i + 1), size=8,
              color=ray_colors[min(i, len(ray_colors)-1)])

    # lados del funicular (paralelos a los rayos, sobre el sistema)
    # construir funicular
    start_pt = np.array([forces_x[0] - 0.3, 0.0])
    funicular_pts = [start_pt.copy()]
    cur = start_pt.copy()

    for i in range(len(forces_x)):
        # rayo i va del polo al vértice i del polígono de fuerzas
        v_start = np.array(vertices[i])
        v_end   = np.array(vertices[i + 1])
        ray_dir = pole - v_start
        ray_dir_norm = ray_dir / np.linalg.norm(ray_dir)

        # siguiente intersección: con la recta de acción de la siguiente fuerza
        if i < len(forces_x) - 1:
            next_x = forces_x[i + 1]
        else:
            next_x = forces_x[-1] + 1.0

        # calcular punto donde el lado del funicular llega a next_x
        if abs(ray_dir_norm[0]) > 1e-9:
            t = (next_x - cur[0]) / ray_dir_norm[0]
        else:
            t = 2.0
        next_pt = cur + t * ray_dir_norm
        funicular_pts.append(next_pt.copy())
        cur = next_pt.copy()

    # último lado (rayo desde vértice final al polo)
    last_ray = pole - np.array(vertices[-1])
    last_ray_norm = last_ray / np.linalg.norm(last_ray)
    last_end = cur + last_ray_norm * 1.5
    funicular_pts.append(last_end)

    # dibujar lados del funicular
    f_cols = colors_f + [STYLE["resultant"]]
    for i in range(len(funicular_pts) - 1):
        p1 = funicular_pts[i]
        p2 = funicular_pts[i + 1]
        ax.plot([p1[0], p2[0]], [p1[1], p2[1]],
                color=f_cols[min(i, len(f_cols)-1)],
                lw=1.4, zorder=3)
        # etiqueta de lado
        mx, my = (p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2
        roman = ["I", "II", "III", "IV", "V"][i]
        label(ax, mx - 0.2, my, roman, size=8,
              color=f_cols[min(i, len(f_cols)-1)])

    # intersección primer y último lado → recta de acción de R
    p_first = funicular_pts[0]
    d_first = funicular_pts[1] - funicular_pts[0]
    p_last  = funicular_pts[-2]
    d_last  = funicular_pts[-1] - funicular_pts[-2]

    # resolver intersección
    A_mat = np.column_stack([d_first, -d_last])
    if abs(np.linalg.det(A_mat)) > 1e-9:
        b_vec = p_last - p_first
        t_vec = np.linalg.solve(A_mat, b_vec)
        inter = p_first + t_vec[0] * d_first
        ax.plot(*inter, "*", color=STYLE["resultant"], ms=12, zorder=7)
        ax.axvline(inter[0], color=STYLE["resultant"],
                   lw=1.5, ls=":", zorder=2, alpha=0.8)
        label(ax, inter[0] + 0.25, inter[1] + 0.3,
              "Recta de\nacción de $R$",
              color=STYLE["resultant"], size=9)

    fig.suptitle("Reducción gráfica de fuerzas no concurrentes — polígono funicular",
                 fontsize=12, color=STYLE["force"])
    fig.tight_layout()
    save(fig, "13_poligono_funicular")


# ── 14 · Fuerzas distribuidas ─────────────────────────────────────────────────
def fig_distribuidas():
    fig, axes = plt.subplots(1, 2, figsize=(11, 5))

    # ── Carga uniforme ────────────────────────────────────────────────────────
    ax = axes[0]
    setup_ax(ax, (-0.5, 6), (-1.0, 3.5), "Carga uniforme: $q = \\mathrm{cte}$",
             grid=False)

    L = 5.0
    q = 1.2   # altura del diagrama

    # viga
    ax.plot([0, L], [0, 0], color=STYLE["force"], lw=3, zorder=3)
    ax.plot([0, 0], [-0.15, 0.15], color=STYLE["force"], lw=2, zorder=3)
    ax.plot([L, L], [-0.15, 0.15], color=STYLE["force"], lw=2, zorder=3)

    # diagrama de carga (rectángulo relleno)
    rect_x = [0, L, L, 0, 0]
    rect_y = [0, 0, q, q, 0]
    ax.fill(rect_x, rect_y, color=STYLE["component"], alpha=0.25, zorder=1)
    ax.plot(rect_x, rect_y, color=STYLE["component"], lw=1.2, zorder=2)

    # flechitas distribuidas
    for x in np.linspace(0.3, L - 0.3, 8):
        arrow(ax, x, q, 0, -q + 0.08,
              color=STYLE["component"], lw=1.2)

    # etiqueta q
    label(ax, L + 0.4, q / 2, "$q$", color=STYLE["component"], size=12)

    # resultante R = q·L en el centro
    xR = L / 2
    R_mag = 1.8
    arrow(ax, xR, -0.3, 0, -R_mag, color=STYLE["resultant"], lw=2.5)
    label(ax, xR + 0.4, -0.3 - R_mag / 2, "$R = q \\cdot L$",
          color=STYLE["resultant"], size=11)

    # posición xR
    ax.annotate("", xy=(xR, -0.55), xytext=(0, -0.55),
                arrowprops=dict(arrowstyle="<->", color=STYLE["moment"], lw=1.2))
    label(ax, xR / 2, -0.78, "$L/2$", color=STYLE["moment"], size=10)

    ax.annotate("", xy=(L, -0.55), xytext=(xR, -0.55),
                arrowprops=dict(arrowstyle="<->", color=STYLE["moment"], lw=1.2))
    label(ax, (xR + L) / 2, -0.78, "$L/2$", color=STYLE["moment"], size=10)

    ax.text(0.1, 3.2,
            "$R = q \\cdot L$\n$x_R = L/2$",
            fontsize=10, color=STYLE["resultant"],
            bbox=dict(boxstyle="round", facecolor="white",
                      edgecolor=STYLE["resultant"], alpha=0.9))

    # ── Carga triangular ──────────────────────────────────────────────────────
    ax = axes[1]
    setup_ax(ax, (-0.5, 6), (-1.0, 3.5),
             "Carga triangular: $q(x) = q_0 \\cdot x/L$", grid=False)

    # viga
    ax.plot([0, L], [0, 0], color=STYLE["force"], lw=3, zorder=3)
    ax.plot([0, 0], [-0.15, 0.15], color=STYLE["force"], lw=2, zorder=3)
    ax.plot([L, L], [-0.15, 0.15], color=STYLE["force"], lw=2, zorder=3)

    # diagrama triangular relleno
    tri_x = [0, L, L, 0]
    tri_y = [0, 0, q, 0]
    ax.fill(tri_x, tri_y, color=STYLE["pair"], alpha=0.2, zorder=1)
    ax.plot([0, L, L, 0], [0, 0, q, 0], color=STYLE["pair"], lw=1.2, zorder=2)

    # flechitas proporcionales
    xs_arr = np.linspace(0.4, L - 0.2, 7)
    for x in xs_arr:
        h = q * x / L
        if h > 0.08:
            arrow(ax, x, h, 0, -h + 0.08,
                  color=STYLE["pair"], lw=1.2)

    # etiqueta q0
    label(ax, L + 0.4, q / 2, "$q_0$", color=STYLE["pair"], size=12)

    # resultante R = q0·L/2 en 2L/3
    xR2 = 2 * L / 3
    arrow(ax, xR2, -0.3, 0, -R_mag, color=STYLE["resultant"], lw=2.5)
    label(ax, xR2 + 0.55, -0.3 - R_mag / 2,
          "$R = \\frac{q_0 L}{2}$",
          color=STYLE["resultant"], size=11)

    # posición 2L/3
    ax.annotate("", xy=(xR2, -0.55), xytext=(0, -0.55),
                arrowprops=dict(arrowstyle="<->", color=STYLE["moment"], lw=1.2))
    label(ax, xR2 / 2, -0.78, "$2L/3$", color=STYLE["moment"], size=10)

    ax.annotate("", xy=(L, -0.55), xytext=(xR2, -0.55),
                arrowprops=dict(arrowstyle="<->", color=STYLE["moment"], lw=1.2))
    label(ax, (xR2 + L) / 2, -0.78, "$L/3$", color=STYLE["moment"], size=10)

    ax.text(0.1, 3.2,
            "$R = q_0 \\cdot L / 2$\n$x_R = 2L/3$",
            fontsize=10, color=STYLE["resultant"],
            bbox=dict(boxstyle="round", facecolor="white",
                      edgecolor=STYLE["resultant"], alpha=0.9))

    fig.suptitle("Fuerzas distribuidas — resultante y posición",
                 fontsize=12, color=STYLE["force"])
    fig.tight_layout()
    save(fig, "14_fuerzas_distribuidas")


# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Generando figuras en clase2/img/...")
    fig_funicular()
    fig_distribuidas()
    print(f"\nListo — {len(os.listdir(OUT_DIR))} archivos en {OUT_DIR}/")