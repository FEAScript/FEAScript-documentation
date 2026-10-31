"""Generate the geometry and mesh figures of the verification pages.

The figures follow the style of the other figures in static/assets: black line art on a transparent background
(inverted in dark mode by src/css/custom.css), sans-serif 15 px labels, boundary keys in grey 12 px, dashed
dimension lines with arrows, and thin grey mesh edges.

Gmsh meshes are read from the tests of FEAScript-core, so the script expects both repositories side by side:

    python3 scripts/generate-verification-figures.py [path/to/FEAScript-core/tests/meshes]

The figures are written to static/assets/verification/.
"""

import math
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MESHES = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "..", "FEAScript-core", "tests", "meshes")
OUTPUT = os.path.join(ROOT, "static", "assets", "verification")

from figure_style import *  # noqa: F401,F403 (shared drawing helpers)


# ── Heat conduction ─────────────────────────────────────────────────────────


def nafems_t4():
    frame = Frame(240, 330, 260)
    x0, y0 = frame(0, 0)
    x1, y1 = frame(0.6, 1.0)
    xe, ye = frame(0.6, 0.2)
    xm = (x0 + x1) / 2
    body = [rectangle(frame, 0.6, 1.0)]
    body += label(xm, y0, f"{italic('T')} = 100 °C", 'boundary "0"', "bottom")
    body += label(x0, (y0 + y1) / 2, "Insulated", 'boundary "1" (unspecified)', "left")
    body += label(
        xm, y1, f"Convection, {italic('h')} = 750 W/(m²·K), {italic('T')}{sub('∞')} = 0 °C", 'boundary "2"', "top"
    )
    body += label(x1, (y0 + y1) / 2, "Convection", 'boundary "3"', "right")
    body += [text(xm, (y0 + y1) / 2 + 5, f"{italic('k')} = 52 W/(m·K)")]
    body += [dot(xe, ye, 4), text(xe - 10, ye + 5, "E", anchor="end"), text(xe - 10, ye + 21, "(0.6, 0.2)", 12, "#666", "end")]
    body += origin(frame)
    body += dimension(x0, y0 + 70, x1, y0 + 70, "0.6 m", offset_y=20)
    body += dimension(x0 - 70, y0, x0 - 70, y1, "1.0 m", offset_x=-10, rotate=-90)
    return svg(640, 440, body, "NAFEMS T4: 0.6 m x 1.0 m plate, point E at (0.6, 0.2)")


def nafems_t4_mesh():
    frame = Frame(240, 330, 260)
    x0, y0 = frame(0, 0)
    x1, _ = frame(0.6, 1.0)
    body = structured_mesh(frame, 0.6, 1.0, 12, 20) + [rectangle(frame, 0.6, 1.0)]
    xe, ye = frame(0.6, 0.2)
    body += [dot(xe, ye, 4), text(xe + 10, ye + 5, "E", anchor="start")]
    body += [text((x0 + x1) / 2, y0 + 26, "12 × 20 quadratic quadrilaterals (25 × 41 nodes)")]
    return svg(640, 380, body, "NAFEMS T4: 12 x 20 structured quadratic mesh")


TPLP302_POINTS = [
    ("E", 0.05, 0.05),
    ("F", 0.05, 0.10),
    ("G", 0.05, 0.15),
    ("H", 0.10, 0.05),
    ("I", 0.10, 0.10),
    ("J", 0.10, 0.15),
    ("K", 0.10, 0.20),
]


def strip_frame():
    """The 0.2 m x 2 m strip, drawn at 1000 px/m up to y = 0.3 m, broken, and closed by the top edge at y = 2 m."""
    frame = Frame(220, 450, 1000)
    x0, y0 = frame(0, 0)
    x1, y_cut = frame(0.2, 0.3)
    y_resume, y_top = y_cut - 30, y_cut - 70
    return frame, x0, y0, x1, y_cut, y_resume, y_top


def zigzag(x0, x1, y):
    step = (x1 - x0) / 8
    points = " ".join(f"{fmt(x0 + i * step)},{fmt(y + (4 if i % 2 else -4))}" for i in range(9))
    return f'<polyline points="{points}" fill="none" stroke="#000" stroke-width="1"/>'


def strip_outline(x0, y0, x1, y_cut, y_resume, y_top):
    return [
        f'<polyline points="{fmt(x0)},{fmt(y_cut)} {fmt(x0)},{fmt(y0)} {fmt(x1)},{fmt(y0)} {fmt(x1)},{fmt(y_cut)}" '
        'fill="none" stroke="#000" stroke-width="2" stroke-linejoin="round"/>',
        f'<polyline points="{fmt(x0)},{fmt(y_resume)} {fmt(x0)},{fmt(y_top)} {fmt(x1)},{fmt(y_top)} {fmt(x1)},{fmt(y_resume)}" '
        'fill="none" stroke="#000" stroke-width="2" stroke-linejoin="round"/>',
        zigzag(x0 - 6, x1 + 6, y_cut),
        zigzag(x0 - 6, x1 + 6, y_resume),
    ]


def tplp302():
    frame, x0, y0, x1, y_cut, y_resume, y_top = strip_frame()
    xm = (x0 + x1) / 2
    body = strip_outline(x0, y0, x1, y_cut, y_resume, y_top)
    body += label(xm, y0, f"{italic('T')} = 100 °C", 'boundary "0"', "bottom")
    body += label(x0, (y0 + y_cut) / 2, f"{italic('T')} = 0 °C", 'boundary "1"', "left")
    body += label(xm, y_top, "Insulated", 'boundary "2" (unspecified)', "top")
    body += label(x1, (y0 + y_cut) / 2, f"{italic('T')} = 0 °C", 'boundary "3"', "right")
    for name, x, y in TPLP302_POINTS:
        px, py = frame(x, y)
        body += [dot(px, py), text(px + 7, py - 5, name, 13, anchor="start")]
    body += origin(frame)
    body += dimension(x0, y0 + 70, x1, y0 + 70, "0.2 m", offset_y=20)
    body += dimension(x0 - 70, y0, x0 - 70, y_top, "2 m", offset_x=-10, rotate=-90)
    body += [text(x1 + 70, (y_cut + y_resume) / 2 + 5, "not to scale", 12, "#666", "start")]
    return svg(640, 560, body, "Code_Aster TPLP302: 0.2 m x 2 m strip, broken above y = 0.3 m, points E to K")


def tplp302_mesh():
    frame, x0, y0, x1, y_cut, y_resume, y_top = strip_frame()
    lines = []
    for i in range(1, 8):
        x, _ = frame(0.025 * i, 0)
        lines.append(f'<line x1="{fmt(x)}" y1="{fmt(y0)}" x2="{fmt(x)}" y2="{fmt(y_cut)}"/>')
        lines.append(f'<line x1="{fmt(x)}" y1="{fmt(y_resume)}" x2="{fmt(x)}" y2="{fmt(y_top)}"/>')
    for j in range(1, 12):
        _, y = frame(0, 0.025 * j)
        lines.append(f'<line x1="{fmt(x0)}" y1="{fmt(y)}" x2="{fmt(x1)}" y2="{fmt(y)}"/>')
    lines.append(f'<line x1="{fmt(x0)}" y1="{fmt(y_top + 25)}" x2="{fmt(x1)}" y2="{fmt(y_top + 25)}"/>')
    body = [f"<g {MESH_STYLE}>"] + ["  " + line for line in lines] + ["</g>"]
    body += strip_outline(x0, y0, x1, y_cut, y_resume, y_top)
    for name, x, y in TPLP302_POINTS:
        px, py = frame(x, y)
        body += [dot(px, py)]
    body += [text((x0 + x1) / 2, y0 + 26, "8 × 80 quadratic quadrilaterals, element size 0.025 m")]
    return svg(640, 500, body, "Code_Aster TPLP302: 8 x 80 structured quadratic mesh, broken above y = 0.3 m")


LSHAPE = [(0, 0), (0.4, 0), (0.4, 0.4), (0.8, 0.4), (0.8, 0.8), (0, 0.8)]
TPLP01_POINTS = [(0.2, y) for y in (0, 0.2, 0.4, 0.6, 0.8)] + [(0.4, y) for y in (0, 0.2, 0.4, 0.6, 0.8)]
TPLP01_POINTS += [(0.6, y) for y in (0.4, 0.6, 0.8)]


def tplp01():
    frame = Frame(170, 400, 400)
    body = [outline([frame(x, y) for x, y in LSHAPE])]
    body += label(*frame(0, 0.4), f"{italic('T')} = 10 °C", 'boundary "0"', "left")
    body += label(*frame(0.8, 0.6), f"{italic('T')} = 0 °C", 'boundary "1"', "right")
    body += label(*frame(0.4, 0.8), "Insulated", 'boundary "2"', "top")
    body += label(*frame(0.2, 0), "Insulated", 'boundary "2"', "bottom")
    bx, by = frame(0.4, 0.2)
    body += [text(bx + 14, by + 5, "Insulated", anchor="start"), text(bx + 14, by + 21, 'boundary "2"', 12, "#666", "start")]
    for x, y in TPLP01_POINTS:
        body += [dot(*frame(x, y))]
    for name, (x, y), (dx, dy) in [
        ("A", (0, 0), (-12, 16)),
        ("B", (0.4, 0), (12, 16)),
        ("C", (0.4, 0.4), (12, 16)),
        ("D", (0.8, 0.4), (12, 16)),
        ("E", (0.8, 0.8), (12, -6)),
        ("F", (0, 0.8), (-12, -6)),
    ]:
        px, py = frame(x, y)
        body += [text(px + dx, py + dy, name, 13, "#666")]
    body += dimension(*frame(0, 0)[:1], frame(0, 0)[1] + 70, frame(0.8, 0)[0], frame(0, 0)[1] + 70, "0.8 m", offset_y=20)
    body += dimension(frame(0.8, 0)[0] + 80, frame(0, 0.4)[1], frame(0.8, 0)[0] + 80, frame(0, 0.8)[1], "0.4 m", offset_x=14, rotate=90)
    return svg(680, 520, body, "Code_Aster TPLP01: L-shaped domain, re-entrant corner C, 13 reference points")


def tplp01_meshes():
    body = []
    for x0, file_name, title in [
        (40, "lshape_triang_quadratic.msh", "618 quadratic triangles"),
        (360, "lshape_quad_quadratic.msh", "321 quadratic quadrilaterals"),
    ]:
        frame = Frame(x0, 320, 300)
        body += gmsh_mesh(frame, read_gmsh(os.path.join(MESHES, file_name)))
        body += [outline([frame(x, y) for x, y in LSHAPE])]
        body += [text(x0 + 120, 352, title)]
        body += [text(x0 + 120, 370, file_name, 12, "#666")]
    return svg(680, 390, body, "Code_Aster TPLP01: Gmsh meshes read from lshape_triang_quadratic.msh and lshape_quad_quadratic.msh")


def varying_coefficients():
    body = [text(40, 40, "1D", 16, anchor="start", weight="bold")]
    frame = Frame(60, 150, 260)
    xa, y = frame(0, 0)
    xb, _ = frame(1, 0)
    body += [f'<line x1="{fmt(xa)}" y1="{fmt(y)}" x2="{fmt(xb)}" y2="{fmt(y)}" stroke="#000" stroke-width="2"/>']
    body += [dot(frame(i / 8, 0)[0], y, 4, filled=False) for i in range(9)]
    body += [text(xa, y - 25, f"{italic('T')}(0)"), text(xa, y - 43, 'boundary "0"', 12, "#666")]
    body += [text(xb, y - 25, f"{italic('T')}(1)"), text(xb, y - 43, 'boundary "1"', 12, "#666")]
    body += dimension(xa, y + 35, xb, y + 35, "1", offset_y=20)
    body += [text((xa + xb) / 2, y + 85, "8 elements", 13, "#666")]

    body += [text(400, 40, "2D", 16, anchor="start", weight="bold")]
    frame = Frame(450, 230, 160)
    body += structured_mesh(frame, 1, 1, 4, 3) + [rectangle(frame, 1, 1)]
    x0, y0 = frame(0, 0)
    x1, y1 = frame(1, 1)
    body += label(x0, (y0 + y1) / 2, f"{italic('T')} = 0", 'boundary "1"', "left")
    body += label(x1, (y0 + y1) / 2, f"{italic('T')} = 1", 'boundary "3"', "right")
    body += label((x0 + x1) / 2, y0, "Insulated", 'boundary "0"', "bottom")
    body += label((x0 + x1) / 2, y1, "Insulated", 'boundary "2"', "top")
    body += [text((x0 + x1) / 2, y0 + 70, "4 × 3 quadratic quadrilaterals, case 1", 13, "#666")]
    return svg(720, 320, body, "Spatially varying coefficients: 1D domain [0, 1] and 2D unit square, case 1")


# ── Creeping flow ───────────────────────────────────────────────────────────


def couette():
    frame = Frame(150, 290, 100)
    x0, y0 = frame(0, 0)
    x1, y1 = frame(4, 2)
    body = [rectangle(frame, 4, 2)]
    body += [f'<line x1="{fmt(x0)}" y1="{fmt(y1)}" x2="{fmt(x1)}" y2="{fmt(y1)}" stroke="#000" stroke-width="4"/>']
    body += ['<g stroke="#000" stroke-width="1">']
    body += [f'  <line x1="{fmt(x)}" y1="{fmt(y0)}" x2="{fmt(x - 12)}" y2="{fmt(y0 + 12)}"/>' for x in range(int(x0) + 12, int(x1) + 1, 16)]
    body += ["</g>"]
    body += [f'<line x1="{fmt(x1 - 120)}" y1="{fmt(y1 - 34)}" x2="{fmt(x1 - 20)}" y2="{fmt(y1 - 34)}" stroke="#000" stroke-width="2" marker-end="url(#arrow)"/>']
    body += label((x0 + x1) / 2, y1, f"Moving wall, {italic('u')} = 1, {italic('v')} = 0", 'boundary "2"', "top")
    body += [text((x0 + x1) / 2, y0 + 30, f"Fixed wall, {italic('u')} = {italic('v')} = 0"), text((x0 + x1) / 2, y0 + 46, 'boundary "0"', 12, "#666")]
    body += label(x0, (y0 + y1) / 2, "Stress-free", 'boundary "1"', "left")
    body += label(x1, (y0 + y1) / 2, "Stress-free", 'boundary "3"', "right")
    xp, _ = frame(1.2, 0)
    body += [f'<line x1="{fmt(xp)}" y1="{fmt(y0)}" x2="{fmt(xp)}" y2="{fmt(y1)}" stroke="#000" stroke-width="1"/>']
    body += [f'<line x1="{fmt(xp)}" y1="{fmt(y0)}" x2="{fmt(xp + 100)}" y2="{fmt(y1)}" stroke="#000" stroke-width="1" stroke-dasharray="4 3"/>']
    for k in range(1, 5):
        y_model = 0.4 * k
        _, py = frame(0, y_model)
        length = 100 * y_model / 2
        if length > 8:
            body += [f'<line x1="{fmt(xp)}" y1="{fmt(py)}" x2="{fmt(xp + length)}" y2="{fmt(py)}" stroke="#000" stroke-width="1.5" marker-end="url(#arrow)"/>']
    body += [text(xp + 140, (y0 + y1) / 2 + 5, f"{italic('u')} = {italic('y')} / 2", anchor="start")]
    body += [text(xp + 140, (y0 + y1) / 2 + 25, f"{italic('μ')} = 1", anchor="start")]
    body += dimension(x0, y0 + 80, x1, y0 + 80, "4 m", offset_y=20)
    body += dimension(x0 - 80, y0, x0 - 80, y1, "2 m", offset_x=-10, rotate=-90)
    return svg(720, 420, body, "Couette flow: 4 m x 2 m channel with a moving top wall")


def mesh_panels(panels, columns, comment, panel_width=190, scale=45):
    rows = math.ceil(len(panels) / columns)
    gap_x, panel_height = 40, 2 * scale + 60
    width = columns * panel_width + (columns + 1) * gap_x - columns * (panel_width - 4 * scale)
    width = 40 + columns * (4 * scale + gap_x)
    body = []
    for index, (title, subtitle, mesh) in enumerate(panels):
        row, column = divmod(index, columns)
        x0 = 40 + column * (4 * scale + gap_x)
        y0 = 30 + row * panel_height + 2 * scale
        frame = Frame(x0, y0, scale)
        if isinstance(mesh, tuple):
            body += structured_mesh(frame, 4, 2, *mesh)
        else:
            body += gmsh_mesh(frame, read_gmsh(os.path.join(MESHES, mesh)))
        body += [rectangle(frame, 4, 2)]
        body += [text(x0 + 2 * scale, y0 + 22, title, 13)]
        body += [text(x0 + 2 * scale, y0 + 38, subtitle, 12, "#666")]
    return svg(width, 30 + rows * panel_height, body, comment)


def couette_meshes():
    return mesh_panels(
        [
            ("4 × 2 Q2-Q1 quadrilaterals", "structured", (4, 2)),
            ("Q2-Q1 quadrilaterals", "rect_quad_quadratic.msh", "rect_quad_quadratic.msh"),
            ("P2-P1 triangles", "rect_triang_quadratic.msh", "rect_triang_quadratic.msh"),
        ],
        3,
        "Couette flow meshes: structured 4 x 2, and Gmsh rect_quad_quadratic.msh and rect_triang_quadratic.msh",
    )


# ── Front propagation ───────────────────────────────────────────────────────


def planar_front():
    body = [text(40, 40, "1D", 16, anchor="start", weight="bold")]
    frame = Frame(60, 150, 130)
    xa, y = frame(0, 0)
    xb, _ = frame(2, 0)
    body += [f'<line x1="{fmt(xa)}" y1="{fmt(y)}" x2="{fmt(xb)}" y2="{fmt(y)}" stroke="#000" stroke-width="2"/>']
    body += [dot(xa, y, 4, filled=False), dot(xb, y, 4, filled=False)]
    body += [text(xa, y - 25, f"{italic('u')} = 0"), text(xa, y - 43, 'boundary "0"', 12, "#666")]
    body += [text(xb, y - 25, "Zero gradient"), text(xb, y - 43, 'boundary "1"', 12, "#666")]
    body += [f'<line x1="{fmt(xa + 40)}" y1="{fmt(y + 25)}" x2="{fmt(xa + 120)}" y2="{fmt(y + 25)}" stroke="#000" stroke-width="1.5" marker-end="url(#arrow)"/>']
    body += [text(xa + 80, y + 45, "front", 13, "#666")]
    body += dimension(xa, y + 75, xb, y + 75, "2", offset_y=20)

    body += [text(400, 40, "2D", 16, anchor="start", weight="bold")]
    frame = Frame(440, 250, 60)
    x0, y0 = frame(0, 0)
    x1, y1 = frame(4, 2)
    body += [rectangle(frame, 4, 2)]
    body += [f'<rect x="{fmt(x0)}" y="{fmt(y1)}" width="{fmt(x1 - x0)}" height="12" fill="#000" fill-opacity="0.12"/>']
    body += [text(x1 - 6, y1 + 26, "boundary layer", 12, "#666", "end")]
    body += label((x0 + x1) / 2, y0, f"{italic('u')} = 0", 'boundary "0"', "bottom")
    body += label(x0, (y0 + y1) / 2, "Zero gradient", 'boundary "1"', "left")
    body += label((x0 + x1) / 2, y1, "Zero gradient", 'boundary "2"', "top")
    body += label(x1, (y0 + y1) / 2, "Zero gradient", 'boundary "3"', "right")
    for x in (1, 2, 3):
        px, _ = frame(x, 0)
        body += [f'<line x1="{fmt(px)}" y1="{fmt(y0 - 15)}" x2="{fmt(px)}" y2="{fmt(y0 - 60)}" stroke="#000" stroke-width="1.5" marker-end="url(#arrow)"/>']
    body += dimension(x0, y0 + 70, x1, y0 + 70, "4", offset_y=20)
    body += dimension(x1 + 70, y0, x1 + 70, y1, "2", offset_x=14, rotate=90)
    return svg(800, 370, body, "Planar front: 1D domain [0, 2] and 2D 4 x 2 domain, front starting at the bottom")


def planar_front_meshes():
    return mesh_panels(
        [
            ("12 × 8 linear quadrilaterals", "structured", (12, 8)),
            ("Linear quadrilaterals", "rect_quad_linear.msh", "rect_quad_linear.msh"),
            ("Quadratic quadrilaterals", "rect_quad_quadratic.msh", "rect_quad_quadratic.msh"),
            ("Linear triangles", "rect_triang_linear.msh", "rect_triang_linear.msh"),
            ("Quadratic triangles", "rect_triang_quadratic.msh", "rect_triang_quadratic.msh"),
            ("80 × 40 linear quadrilaterals", "structured, interior check", (80, 40)),
        ],
        3,
        "Planar front 2D meshes: structured 12 x 8 and 80 x 40, and the four Gmsh rect meshes",
    )


# ── Euler–Bernoulli beam ────────────────────────────────────────────────────


def cantilever():
    body = ['<rect x="100" y="115" width="400" height="10" fill="#fff" stroke="#000" stroke-width="2"/>']
    body += ['<line x1="100" y1="65" x2="100" y2="175" stroke="#000" stroke-width="2"/>', '<g stroke="#000" stroke-width="1">']
    body += [f'  <line x1="100" y1="{71 + 14 * k}" x2="88" y2="{83 + 14 * k}"/>' for k in range(8)]
    body += ["</g>", dot(100, 120), dot(500, 120)]
    body += ['<line x1="500" y1="40" x2="500" y2="110" stroke="#000" stroke-width="2" marker-end="url(#arrow)"/>']
    body += [text(512, 58, f"{italic('P')} = −1000", anchor="start"), text(512, 76, 'node "2"', 12, "#666", "start")]
    body += [text(100, 196, "Clamped"), text(100, 212, 'node "1"', 12, "#666")]
    body += [text(300, 90, f"{italic('EI')} = 10<tspan dy=\"-6\" font-size=\"11\">5</tspan><tspan dy=\"6\">, one element</tspan>")]
    body += dimension(100, 160, 500, 160, f"{italic('L')} = 4", offset_y=20)
    return svg(600, 240, body, "Cantilever beam: one cubic Hermite element, tip load P")


FIGURES = {
    "nafems-t4-geometry.svg": nafems_t4,
    "nafems-t4-mesh.svg": nafems_t4_mesh,
    "tplp302-geometry.svg": tplp302,
    "tplp302-mesh.svg": tplp302_mesh,
    "tplp01-geometry.svg": tplp01,
    "tplp01-meshes.svg": tplp01_meshes,
    "varying-coefficients.svg": varying_coefficients,
    "couette-geometry.svg": couette,
    "couette-meshes.svg": couette_meshes,
    "planar-front-geometry.svg": planar_front,
    "planar-front-meshes.svg": planar_front_meshes,
    "cantilever-geometry.svg": cantilever,
}

if __name__ == "__main__":
    os.makedirs(OUTPUT, exist_ok=True)
    for file_name, draw in FIGURES.items():
        with open(os.path.join(OUTPUT, file_name), "w") as handle:
            handle.write(draw())
        print(f"Wrote static/assets/verification/{file_name}")
