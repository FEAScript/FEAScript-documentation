"""Generate the geometry, mesh and result figures of the example pages.

Run scripts/export-example-results.mjs first: it runs the Node.js examples of FEAScript-core and records each mesh
and solution in scripts/.example-results/. This script reads those records and writes the figures to
static/assets/examples/, in the style of the other figures (see figure_style.py).

    node scripts/export-example-results.mjs
    python3 scripts/generate-example-figures.py
"""

import json
import math
import os

from figure_style import *  # noqa: F401,F403 (shared drawing helpers)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS = os.path.join(ROOT, "scripts", ".example-results")
OUTPUT = os.path.join(ROOT, "static", "assets", "examples")

HALO = 'stroke="#fff" stroke-width="4" stroke-linejoin="round" paint-order="stroke"'


def load(name):
    with open(os.path.join(RESULTS, f"{name}-0.json")) as handle:
        return json.load(handle)


# ── Mesh topology ───────────────────────────────────────────────────────────


def element_layout(nodes_per_element, shape):
    """Outline (in order around the element) and linear sub-triangles, as local node indices.

    FEAScript numbers quadrilateral nodes on a ksi-major grid (node = i * n + j), and triangle nodes as
    0 (0,0), 1 (0,1), 2 (1,0) for linear and 0 (0,0), 1 (0,1/2), 2 (0,1), 3 (1/2,0), 4 (1/2,1/2), 5 (1,0) for quadratic.
    """
    if shape == "triangle" and nodes_per_element == 3:
        return [0, 2, 1], [(0, 2, 1)]
    if shape == "triangle":
        return [0, 3, 5, 4, 2, 1], [(0, 3, 1), (3, 4, 1), (3, 5, 4), (1, 4, 2)]
    n = 2 if nodes_per_element == 4 else 3

    def grid(i, j):
        return i * n + j

    outline_nodes = [grid(i, 0) for i in range(n)] + [grid(n - 1, j) for j in range(1, n)]
    outline_nodes += [grid(i, n - 1) for i in range(n - 2, -1, -1)] + [grid(0, j) for j in range(n - 2, 0, -1)]
    triangles = []
    for i in range(n - 1):
        for j in range(n - 1):
            a, b, c, d = grid(i, j), grid(i + 1, j), grid(i + 1, j + 1), grid(i, j + 1)
            triangles += [(a, b, c), (a, c, d)]
    return outline_nodes, triangles


def elements(record):
    for element in record["nop"]:
        outline_nodes, triangles = element_layout(len(element), record["elementShape"])
        yield [element[k] - 1 for k in outline_nodes], [tuple(element[k] - 1 for k in t) for t in triangles]


def boundary_edges(record):
    """Element outline edges used by a single element: the boundary of the domain."""
    count = {}
    for outline_nodes, _ in elements(record):
        for a, b in zip(outline_nodes, outline_nodes[1:] + outline_nodes[:1]):
            key = (min(a, b), max(a, b))
            count[key] = count.get(key, 0) + 1
    return [edge for edge, used in count.items() if used == 1]


class Fit:
    """Scales a 2D mesh into the drawing area, with the given margins around it."""

    def __init__(self, record, width=520, height=300, left=110, top=70):
        xs, ys = record["x"], record["y"]
        self.x_min, self.x_max, self.y_min, self.y_max = min(xs), max(xs), min(ys), max(ys)
        self.scale = min(width / (self.x_max - self.x_min), height / (self.y_max - self.y_min))
        self.left, self.top = left, top
        self.width = self.scale * (self.x_max - self.x_min)
        self.height = self.scale * (self.y_max - self.y_min)

    def __call__(self, x, y):
        return self.left + self.scale * (x - self.x_min), self.top + self.scale * (self.y_max - y)


def mesh_body(record, fit):
    xs, ys = record["x"], record["y"]
    body = [f"<g {MESH_STYLE}>"]
    for outline_nodes, _ in elements(record):
        points = " ".join(f"{fmt(px)},{fmt(py)}" for px, py in (fit(xs[k], ys[k]) for k in outline_nodes))
        body.append(f'  <polygon points="{points}"/>')
    body.append("</g>")
    return body + domain_outline(record, fit)


def domain_outline(record, fit):
    xs, ys = record["x"], record["y"]
    segments = " ".join(
        f"M{fmt(fit(xs[a], ys[a])[0])},{fmt(fit(xs[a], ys[a])[1])} L{fmt(fit(xs[b], ys[b])[0])},{fmt(fit(xs[b], ys[b])[1])}"
        for a, b in boundary_edges(record)
    )
    return [f'<path d="{segments}" fill="none" stroke="#000" stroke-width="2" stroke-linecap="round"/>']


def slanted_label(px, py, condition, key, angle, normal):
    """Condition and key along a slanted edge, offset outward along the unit normal (SVG coordinates)."""
    nx, ny = normal
    return [
        text(px + 22 * nx, py + 22 * ny, condition, rotate=angle),
        text(px + 40 * nx, py + 40 * ny, key, 12, "#666", rotate=angle),
    ]


RHOMBOID_LEFT = (-63.43, (-2 / math.sqrt(5), -1 / math.sqrt(5)))
RHOMBOID_RIGHT = (-63.43, (2 / math.sqrt(5), 1 / math.sqrt(5)))


def side_labels(fit, sides):
    """sides: list of (x, y, name, key, side) in model coordinates; side is a name or (angle, normal)."""
    body = []
    for x, y, name, key, side in sides:
        px, py = fit(x, y)
        if isinstance(side, tuple):
            body += slanted_label(px, py, name, f'boundary "{key}"', *side)
        else:
            body += label(px, py, name, f'boundary "{key}"', side)
    return body


def mesh_figure(record, sides, caption, comment):
    fit = Fit(record)
    body = mesh_body(record, fit) + side_labels(fit, sides)
    body += [dot(*fit(0, 0)), text(fit(0, 0)[0] - 8, fit(0, 0)[1] + 20, "(0, 0)", 13, anchor="end")]
    bottom = fit.top + fit.height
    body += [text(fit.left + fit.width / 2, bottom + 70, caption, 13, "#666")]
    return svg(fit.left + fit.width + 110, int(bottom + 90), body, comment)


# ── Contours ────────────────────────────────────────────────────────────────


def nice_levels(low, high, count=8):
    raw = (high - low) / count
    magnitude = 10 ** math.floor(math.log10(raw))
    step = min((m * magnitude for m in (1, 2, 2.5, 5, 10) if m * magnitude >= raw), default=raw)
    first = math.ceil(low / step + 1e-9) * step
    levels = []
    value = first
    while value < high - 1e-9 * abs(high):
        levels.append(round(value, 10))
        value += step
    return levels


def shape_functions(nodes_per_element, shape, ksi, eta):
    """Shape functions of FEAScript elements at (ksi, eta), in the local node order of the element."""
    if shape == "triangle":
        l1 = 1 - ksi - eta
        if nodes_per_element == 3:
            return [l1, eta, ksi]
        return [l1 * (2 * l1 - 1), 4 * l1 * eta, eta * (2 * eta - 1), 4 * l1 * ksi, 4 * ksi * eta, ksi * (2 * ksi - 1)]
    if nodes_per_element == 4:
        lagrange = [lambda t: 1 - t, lambda t: t]
    else:
        lagrange = [lambda t: 2 * (t - 0.5) * (t - 1), lambda t: -4 * t * (t - 1), lambda t: 2 * t * (t - 0.5)]
    return [li(ksi) * lj(eta) for li in lagrange for lj in lagrange]


def sampled_triangles(record, values, divisions=8):
    """Each element split into small triangles, with the coordinates and the field evaluated by the element's
    shape functions (isoparametric), so that the contours follow the finite element solution inside elements."""
    xs, ys, shape = record["x"], record["y"], record["elementShape"]
    for element in record["nop"]:
        nodes = [k - 1 for k in element]
        n = divisions

        def sample(ksi, eta):
            weights = shape_functions(len(nodes), shape, ksi, eta)
            return tuple(sum(w * c[k] for w, k in zip(weights, nodes)) for c in (xs, ys, values))

        if shape == "triangle":
            grid = {(i, j): sample(i / n, j / n) for i in range(n + 1) for j in range(n + 1 - i)}
            for i in range(n):
                for j in range(n - i):
                    yield grid[i, j], grid[i + 1, j], grid[i, j + 1]
                    if i + j < n - 1:
                        yield grid[i + 1, j], grid[i + 1, j + 1], grid[i, j + 1]
        else:
            grid = {(i, j): sample(i / n, j / n) for i in range(n + 1) for j in range(n + 1)}
            for i in range(n):
                for j in range(n):
                    yield grid[i, j], grid[i + 1, j], grid[i + 1, j + 1]
                    yield grid[i, j], grid[i + 1, j + 1], grid[i, j + 1]


def field_extremes(record, values):
    """Lowest and highest value of the finite element solution, sampled inside the elements: (value, x, y)."""
    points = [vertex for triangle in sampled_triangles(record, values) for vertex in triangle]
    low = min(points, key=lambda p: p[2])
    high = max(points, key=lambda p: p[2])
    return (low[2], low[0], low[1]), (high[2], high[0], high[1])


def contour_segments(record, values, level):
    segments = []
    for triangle in sampled_triangles(record, values):
        points = []
        for a, b in ((triangle[0], triangle[1]), (triangle[1], triangle[2]), (triangle[2], triangle[0])):
            va, vb = a[2] - level, b[2] - level
            if (va < 0) != (vb < 0):
                t = va / (va - vb)
                points.append((a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1])))
        if len(points) == 2:
            segments.append(points)
    return segments


def format_level(value):
    return f"{value:g}"


def contour_figure(record, values, levels, title, comment, markers=(), extra=None):
    """Contour lines of a nodal field, labeled with their values, on the outline of the domain."""
    fit = Fit(record, top=60)
    body = [text(fit.left + fit.width / 2, 30, title)]
    if extra:
        body += extra(fit)
    placed = []
    for level in levels:
        segments = contour_segments(record, values, level)
        if not segments:
            continue
        path = " ".join(
            f"M{fmt(fit(*p)[0])},{fmt(fit(*p)[1])} L{fmt(fit(*q)[0])},{fmt(fit(*q)[1])}" for p, q in segments
        )
        body.append(f'<path d="{path}" fill="none" stroke="#000" stroke-width="1" stroke-linecap="round"/>')
        # Label the segment nearest the middle of the contour line, away from earlier labels and the outline
        midpoints = sorted(((p[0] + q[0]) / 2, (p[1] + q[1]) / 2) for p, q in segments)
        for candidate in midpoints[len(midpoints) // 2 :] + midpoints[: len(midpoints) // 2][::-1]:
            px, py = fit(*candidate)
            inside = fit.left + 18 < px < fit.left + fit.width - 18 and fit.top + 10 < py < fit.top + fit.height - 8
            if inside and all(math.hypot(px - qx, py - qy) > 45 for qx, qy in placed):
                placed.append((px, py))
                body.append(
                    f'<text x="{fmt(px)}" y="{fmt(py + 4)}" font-size="12" text-anchor="middle" {HALO}>'
                    f"{format_level(level)}</text>"
                )
                break
    body += domain_outline(record, fit)
    for x, y, name, anchor in markers:
        px, py = fit(x, y)
        body += [dot(px, py, 4), text(px + (10 if anchor == "start" else -10), py + 5, name, 13, anchor=anchor)]
    return svg(fit.left + fit.width + 110, int(fit.top + fit.height + 40), body, comment)


def velocity_arrows(record, spacing=1, length_per_speed=0.8):
    """Velocity vectors at every other element corner node, as an extra layer of a contour figure."""

    def draw(fit):
        xs, ys, u, v = record["x"], record["y"], record["fields"]["u"], record["fields"]["v"]
        nx, ny = record["meshConfig"]["numElementsX"], record["meshConfig"]["numElementsY"]
        dx, dy = record["meshConfig"]["maxX"] / nx, record["meshConfig"]["maxY"] / ny
        lines = []
        for k in range(len(xs)):
            i, j = round(xs[k] / dx), round(ys[k] / dy)
            on_corner = abs(xs[k] - i * dx) < 1e-9 and abs(ys[k] - j * dy) < 1e-9
            if not on_corner or i % spacing or j % spacing or j == ny:
                continue
            px, py = fit(xs[k], ys[k])
            length = length_per_speed * fit.scale * math.hypot(u[k], v[k])
            if length < 3:
                continue
            ex, ey = px + length_per_speed * fit.scale * u[k], py - length_per_speed * fit.scale * v[k]
            lines.append(
                f'<line x1="{fmt(px)}" y1="{fmt(py)}" x2="{fmt(ex)}" y2="{fmt(ey)}" stroke="#000" '
                'stroke-width="1" stroke-opacity="0.6" marker-end="url(#arrow-small)"/>'
            )
        marker = (
            '<defs><marker id="arrow-small" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" '
            'orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#000" fill-opacity="0.6"/></marker></defs>'
        )
        return [marker] + lines

    return draw


# ── Line plots ──────────────────────────────────────────────────────────────


def line_plot(series, x_label, y_label, x_ticks, y_ticks, comment, width=640, height=360, legend=()):
    """series: list of (points, dashed, markers, name, name_at); points None draws markers only.

    legend: list of (dashed, marker, name), drawn in the top left corner of the plot.
    """
    left, right, top, bottom = 90, width - 40, 30, height - 60
    x_min, x_max, y_min, y_max = x_ticks[0], x_ticks[-1], y_ticks[0], y_ticks[-1]

    def px(x):
        return left + (x - x_min) / (x_max - x_min) * (right - left)

    def py(y):
        return bottom - (y - y_min) / (y_max - y_min) * (bottom - top)

    body = [f'<g stroke="#000" stroke-width="0.6" stroke-opacity="0.25">']
    body += [f'  <line x1="{fmt(px(t))}" y1="{top}" x2="{fmt(px(t))}" y2="{bottom}"/>' for t in x_ticks]
    body += [f'  <line x1="{left}" y1="{fmt(py(t))}" x2="{right}" y2="{fmt(py(t))}"/>' for t in y_ticks]
    body += ["</g>"]
    body += [f'<line x1="{left}" y1="{bottom}" x2="{right}" y2="{bottom}" stroke="#000" stroke-width="1"/>']
    body += [f'<line x1="{left}" y1="{top}" x2="{left}" y2="{bottom}" stroke="#000" stroke-width="1"/>']
    body += [text(px(t), bottom + 20, format_level(t), 13) for t in x_ticks]
    body += [text(left - 8, py(t) + 4, format_level(t), 13, anchor="end") for t in y_ticks]
    body += [text((left + right) / 2, height - 14, x_label)]
    body += [text(24, (top + bottom) / 2, y_label, rotate=-90)]
    for points, dashed, markers, name, name_at in series:
        dash = ' stroke-dasharray="5 4"' if dashed else ""
        if points:
            path = " ".join(f"{fmt(px(x))},{fmt(py(y))}" for x, y in points)
            body.append(f'<polyline points="{path}" fill="none" stroke="#000" stroke-width="1.5"{dash}/>')
        if markers:
            body += [dot(px(x), py(y), 3.5, filled=False) for x, y in markers]
        if name:
            x, y = points[name_at]
            body.append(f'<text x="{fmt(px(x) + 8)}" y="{fmt(py(y) - 8)}" font-size="13" {HALO}>{name}</text>')
    for k, (dashed, marker, name) in enumerate(legend):
        ly = top + 18 + 22 * k
        if marker:
            body.append(dot(left + 34, ly, 3.5, filled=False))
        else:
            dash = ' stroke-dasharray="5 4"' if dashed else ""
            body.append(f'<line x1="{left + 18}" y1="{ly}" x2="{left + 50}" y2="{ly}" stroke="#000" stroke-width="1.5"{dash}/>')
        body.append(f'<text x="{left + 60}" y="{ly + 4}" font-size="13" {HALO}>{name}</text>')
    return svg(width, height, body, comment)


def nodal_series(record, values=None):
    values = values if values is not None else record["solution"]
    return sorted(zip(record["x"], values))


def hermite_deflection(record, samples=20):
    """Deflection between the nodes from the cubic Hermite shape functions of each element."""
    xs, w, theta = record["x"], record["fields"]["w"], record["fields"]["theta"]
    points = []
    for e in range(len(xs) - 1):
        h = xs[e + 1] - xs[e]
        for s in range(samples + (e == len(xs) - 2)):
            ksi = s / samples
            n1, n2 = 2 * ksi**3 - 3 * ksi**2 + 1, h * (ksi**3 - 2 * ksi**2 + ksi)
            n3, n4 = -2 * ksi**3 + 3 * ksi**2, h * (ksi**3 - ksi**2)
            points.append((xs[e] + ksi * h, n1 * w[e] + n2 * theta[e] + n3 * w[e + 1] + n4 * theta[e + 1]))
    return points


# ── 1D domains ──────────────────────────────────────────────────────────────


def domain_1d(record, left, right, length_label, comment, regions=None, title=None):
    """1D mesh: element end nodes as open circles, midside nodes of quadratic elements as dots."""
    x0, x1, y = 80, 500, 130
    xs = record["x"]
    span = xs[-1] - xs[0]

    def px(x):
        return x0 + (x1 - x0) * (x - xs[0]) / span

    body = [text((x0 + x1) / 2, 30, title)] if title else []
    if regions:
        for start, end, name in regions:
            body += [text((px(start) + px(end)) / 2, y + 30, name, 13, "#666")]
            if start > xs[0]:
                body += [f'<line x1="{fmt(px(start))}" y1="{y - 14}" x2="{fmt(px(start))}" y2="{y + 14}" stroke="#000" stroke-width="1" stroke-dasharray="3 2"/>']
    body += [f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="#000" stroke-width="2"/>']
    quadratic = record["elementOrder"] == "quadratic"
    for k, x in enumerate(xs):
        if quadratic and k % 2:
            body.append(f'<circle cx="{fmt(px(x))}" cy="{y}" r="2"/>')
        else:
            body.append(dot(px(x), y, 4, filled=False))
    body += [text(x0, y - 26, left), text(x0, y - 44, 'boundary "0"', 12, "#666")]
    body += [text(x1, y - 26, right), text(x1, y - 44, 'boundary "1"', 12, "#666")]
    body += dimension(x0, y + 55, x1, y + 55, length_label, offset_y=20)
    return svg(580, y + 105, body, comment)


# ── Geometries ──────────────────────────────────────────────────────────────


def rect_geometry(width, height, sides, inside, comment, scale=None, extra=None):
    """A width x height rectangle with a condition on each side: sides = (bottom, left, top, right)."""
    scale = scale or min(320 / width, 200 / height)
    frame = Frame(160, 80 + scale * height, scale)
    x0, y0 = frame(0, 0)
    x1, y1 = frame(width, height)
    xm, ym = (x0 + x1) / 2, (y0 + y1) / 2
    body = [rectangle(frame, width, height)]
    if extra:
        body += extra(frame)
    for (condition, key), side, (x, y) in zip(
        sides, ("bottom", "left", "top", "right"), ((xm, y0), (x0, ym), (xm, y1), (x1, ym))
    ):
        body += label(x, y, condition, f'boundary "{key}"', side)
    for content, (x, y) in inside:
        px, py = frame(x, y)
        body.append(text(px, py, content))
    body += origin(frame)
    body += dimension(x0, y0 + 70, x1, y0 + 70, f"{fmt(width)} m", offset_y=20)
    body += dimension(x0 - 80, y0, x0 - 80, y1, f"{fmt(height)} m", offset_x=-10, rotate=-90)
    return svg(int(x1 + 120), int(y0 + 110), body, comment)


T = italic("T")
H_CONV = f"Convection, {italic('h')} = 1 W/(m²·K), {T}{sub('∞')} = 20 °C"
FIN_SIDES = ((f"{T} = 200 °C", 0), ("Symmetry", 1), (H_CONV, 2), (f"{T} = 200 °C", 3))


def fin_geometry():
    return rect_geometry(4, 2, FIN_SIDES, [(f"∇<tspan dy=\"-6\" font-size=\"11\">2</tspan><tspan dy=\"6\">{T}(<tspan font-style=\"italic\">x</tspan>, <tspan font-style=\"italic\">y</tspan>) = 0</tspan>", (2, 1))], "2D fin: 4 m x 2 m")


def fin_varying_geometry():
    def regions(frame):
        x_mid, y_bottom = frame(2, 0)
        _, y_top = frame(2, 2)
        x_left, y_strip = frame(0, 1.5)
        x_right, _ = frame(4, 1.5)
        return [
            f'<rect x="{fmt(x_left)}" y="{fmt(y_top)}" width="{fmt(x_right - x_left)}" height="{fmt(y_strip - y_top)}" fill="#000" fill-opacity="0.1"/>',
            f'<line x1="{fmt(x_mid)}" y1="{fmt(y_bottom)}" x2="{fmt(x_mid)}" y2="{fmt(y_strip)}" stroke="#000" stroke-width="1" stroke-dasharray="5 4"/>',
        ]

    inside = [
        (f"{italic('k')} = 10 W/(m·K)", (1, 0.75)),
        (f"{italic('k')} = 1 W/(m·K)", (3, 0.75)),
        (f"{italic('Q')} = 500 W/m³ (y &gt; 1.5 m)", (2, 1.68)),
    ]
    return rect_geometry(4, 2, FIN_SIDES, inside, "2D fin with spatially varying k and Q", extra=regions)


def rhomboid_geometry():
    frame = Frame(140, 260, 80)
    corners = [(0, 0), (4, 0), (5, 2), (1, 2)]
    body = [outline([frame(x, y) for x, y in corners])]
    body += label(*frame(2, 0), f"{T} = 200 °C", 'boundary "0"', "bottom")
    body += label(*frame(3, 2), H_CONV, 'boundary "2"', "top")
    body += slanted_label(*frame(0.5, 1), "Symmetry", 'boundary "1"', *RHOMBOID_LEFT)
    body += slanted_label(*frame(4.5, 1), f"{T} = 200 °C", 'boundary "3"', *RHOMBOID_RIGHT)
    body += origin(frame)
    body += dimension(*frame(0, 0)[:1], frame(0, 0)[1] + 70, frame(4, 0)[0], frame(0, 0)[1] + 70, "4 m", offset_y=20)
    body += dimension(frame(5, 0)[0] + 60, frame(0, 0)[1], frame(5, 0)[0] + 60, frame(0, 2)[1], "2 m", offset_x=14, rotate=90)
    body += [text(*frame(2.5, 1), f"∇<tspan dy=\"-6\" font-size=\"11\">2</tspan><tspan dy=\"6\">{T} = 0</tspan>")]
    return svg(640, 370, body, "2D rhomboid fin: bottom 4 m, top shifted by 1 m, height 2 m")


def cavity_geometry():
    sides = (
        (f"No slip, {italic('u')} = {italic('v')} = 0", 0),
        (f"No slip, {italic('u')} = {italic('v')} = 0", 1),
        (f"Moving lid, {italic('u')} = 1, {italic('v')} = 0", 2),
        (f"No slip, {italic('u')} = {italic('v')} = 0", 3),
    )

    def lid(frame):
        x0, y1 = frame(0, 2)
        x1, _ = frame(4, 2)
        return [f'<line x1="{fmt(x1 - 120)}" y1="{fmt(y1 - 48)}" x2="{fmt(x1 - 20)}" y2="{fmt(y1 - 48)}" stroke="#000" stroke-width="2" marker-end="url(#arrow)"/>']

    inside = [(f"−{italic('μ')}∇<tspan dy=\"-6\" font-size=\"11\">2</tspan><tspan dy=\"6\"><tspan font-weight=\"bold\">u</tspan> + ∇{italic('p')} = 0</tspan>", (2, 1.1)), ("∇·<tspan font-weight=\"bold\">u</tspan> = 0", (2, 0.8))]
    return rect_geometry(4, 2, sides, inside, "Lid-driven cavity: 4 m x 2 m", extra=lid)


def solidification_geometry():
    sides = (
        (f"Initial front, {italic('u')} = 0", 0),
        (f"Initial front, {italic('u')} = 0", 1),
        (f"Zero gradient, ∂{italic('u')}/∂{italic('n')} = 0", 2),
        (f"Initial front, {italic('u')} = 0", 3),
    )
    return rect_geometry(4, 2, sides, [(f"|∇{italic('u')}| = 1", (2, 1))], "Solidification front: 4 m x 2 m")


def wall_geometry(name, left, right, regions, comment):
    """A wall of width 0.15 m, hatched, with its left and right conditions."""
    x0, x1, y0, y1 = 210, 350, 50, 230
    body = []
    for start, end, hatch in regions:
        a, b = x0 + (x1 - x0) * start / 0.15, x0 + (x1 - x0) * end / 0.15
        body.append(f'<clipPath id="{name}-{start}"><rect x="{fmt(a)}" y="{y0}" width="{fmt(b - a)}" height="{y1 - y0}"/></clipPath>')
        step = 14 if hatch == "dense" else 28
        lines = "".join(
            f'<line x1="{fmt(a + k)}" y1="{y1}" x2="{fmt(a + k + (y1 - y0))}" y2="{y0}"/>'
            for k in range(-(y1 - y0), int(b - a) + 1, step)
        )
        body.append(f'<g clip-path="url(#{name}-{start})" stroke="#000" stroke-width="1">{lines}</g>')
        if start > 0:
            body.append(f'<line x1="{fmt(a)}" y1="{y0}" x2="{fmt(a)}" y2="{y1}" stroke="#000" stroke-width="1" stroke-dasharray="5 4"/>')
    body.append(f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}" fill="none" stroke="#000" stroke-width="2"/>')
    for k, content in enumerate(left):
        body.append(text(x0 - 16, 115 + 21 * k, content, anchor="end"))
    body.append(text(x0 - 16, 115 + 21 * len(left), 'boundary "0"', 12, "#666", "end"))
    for k, content in enumerate(right):
        body.append(text(x1 + 16, 125 + 21 * k, content, anchor="start"))
    body.append(text(x1 + 16, 125 + 21 * len(right), 'boundary "1"', 12, "#666", "start"))
    for start, end, hatch in regions:
        if len(regions) > 1:
            a, b = x0 + (x1 - x0) * start / 0.15, x0 + (x1 - x0) * end / 0.15
            k_value = "10" if hatch == "dense" else "1"
            body.append(text((a + b) / 2, y0 - 12, f"{italic('k')} = {k_value}", 13))
    body += dimension(x0, y1 + 30, x1, y1 + 30, "0.15 m", offset_y=20)
    body += [dot(x0, y1 + 80), f'<line x1="{x0}" y1="{y1 + 80}" x2="{x0 + 50}" y2="{y1 + 80}" stroke="#000" stroke-width="1" marker-end="url(#arrow)"/>']
    body += [text(x0 + 58, y1 + 85, italic("x"), anchor="start"), text(x0, y1 + 98, f"{italic('x')} = 0", 12)]
    return svg(580, y1 + 110, body, comment)


def line_domain_geometry(length_label, left, right, equation, comment, source=None):
    x0, x1, y = 80, 500, 190 if source else 100
    body = [text((x0 + x1) / 2, 40, equation, 18)]
    body += [f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="#000" stroke-width="2"/>', dot(x0, y, 4, filled=False), dot(x1, y, 4, filled=False)]
    if source:
        body += source(x0, x1, y)
    body += [text(x0, y + 28, left), text(x0, y + 44, 'boundary "0"', 12, "#666")]
    body += [text(x1, y + 28, right), text(x1, y + 44, 'boundary "1"', 12, "#666")]
    body += dimension(x0, y + 75, x1, y + 75, length_label, offset_y=20)
    return svg(580, y + 115, body, comment)


def gaussian_source(x0, x1, y):
    curve = " ".join(f"{fmt(x0 + (x1 - x0) * k / 200)},{fmt(y - 12 - 90 * math.exp(-200 * (k / 200 - 0.5) ** 2))}" for k in range(201))
    return [
        f'<polyline points="{curve}" fill="none" stroke="#000" stroke-width="1.5"/>',
        text((x0 + x1) / 2 + 34, y - 90, f"Source {italic('D')}({italic('x')})", anchor="start"),
        f'<line x1="{fmt(x0 + 0.15 * (x1 - x0))}" y1="{y - 40}" x2="{fmt(x0 + 0.32 * (x1 - x0))}" y2="{y - 40}" stroke="#000" stroke-width="1.5" marker-end="url(#arrow)"/>',
        text(x0 + 0.235 * (x1 - x0), y - 50, "Advection", 13, "#666"),
    ]


def second_derivative(variable="u"):
    return f"d<tspan dy=\"-6\" font-size=\"11\">2</tspan><tspan dy=\"6\">{italic(variable)}/d{italic('x')}</tspan><tspan dy=\"-6\" font-size=\"11\">2</tspan><tspan dy=\"6\">"


def cantilever_geometry():
    body = ['<rect x="100" y="115" width="400" height="10" fill="#fff" stroke="#000" stroke-width="2"/>']
    body += ['<line x1="100" y1="65" x2="100" y2="175" stroke="#000" stroke-width="2"/>', '<g stroke="#000" stroke-width="1">']
    body += [f'  <line x1="100" y1="{71 + 14 * k}" x2="88" y2="{83 + 14 * k}"/>' for k in range(8)]
    body += ["</g>"] + [dot(100 + 100 * k, 120) for k in range(5)]
    body += ['<line x1="500" y1="40" x2="500" y2="110" stroke="#000" stroke-width="2" marker-end="url(#arrow)"/>']
    body += [text(512, 58, f"{italic('P')} = −1000 N", anchor="start"), text(512, 76, 'node "5"', 12, "#666", "start")]
    body += [text(100, 196, "Clamped"), text(100, 212, 'node "1"', 12, "#666")]
    body += [text(300, 90, f"{italic('EI')} = 10<tspan dy=\"-6\" font-size=\"11\">5</tspan><tspan dy=\"6\">&#160;N·m²</tspan>")]
    body += dimension(100, 160, 500, 160, f"{italic('L')} = 4 m", offset_y=20)
    return svg(600, 240, body, "Cantilever beam: 4 elements, clamped at node 1, tip load at node 5")


# ── Figures ─────────────────────────────────────────────────────────────────

RECT_SIDES = [(2, 0, "bottom", 0, "bottom"), (0, 1, "left", 1, "left"), (2, 2, "top", 2, "top"), (4, 1, "right", 3, "right")]


def figures():
    out = {}
    wall = load("heatConduction1DWall")
    out["wall-geometry"] = wall_geometry("wall", ["Convection", f"{italic('h')} = 1 W/(m²·K)", f"{T}{sub('∞')} = 25 °C"], ["Constant temperature", f"{T} = 5 °C"], [(0, 0.15, "sparse")], "1D wall, 0.15 m")
    out["wall-mesh"] = domain_1d(wall, "Convection", f"{T} = 5 °C", "0.15 m", "1D wall: 10 linear elements")
    out["wall-results"] = line_plot([(nodal_series(wall), False, nodal_series(wall), None, 0)], f"{italic('x')} (m)", f"{T} (°C)", [0, 0.05, 0.1, 0.15], [5, 6, 7, 8], "1D wall: temperature")

    varying_k = load("heatConduction1DVaryingK")
    out["wall-varying-k-geometry"] = wall_geometry("bimaterial", ["Convection", f"{italic('h')} = 25 W/(m²·K)", f"{T}{sub('∞')} = 5 °C"], ["Constant temperature", f"{T} = 20 °C"], [(0, 0.075, "dense"), (0.075, 0.15, "sparse")], "1D bi-material wall, interface at x = 0.075 m")
    out["wall-varying-k-mesh"] = domain_1d(varying_k, "Convection", f"{T} = 20 °C", "0.15 m", "1D bi-material wall: 20 linear elements", regions=[(0, 0.075, f"{italic('k')} = 10"), (0.075, 0.15, f"{italic('k')} = 1")])
    out["wall-varying-k-results"] = line_plot([(nodal_series(varying_k), False, nodal_series(varying_k), None, 0)], f"{italic('x')} (m)", f"{T} (°C)", [0, 0.05, 0.1, 0.15], [8, 12, 16, 20], "1D bi-material wall: temperature")

    fin = load("heatConduction2DFin")
    out["fin-geometry"] = fin_geometry()
    out["fin-mesh"] = mesh_figure(fin, RECT_SIDES, "8 × 4 quadratic quadrilaterals, 153 nodes", "2D fin: structured mesh")
    out["fin-results"] = contour_figure(fin, fin["solution"], nice_levels(80, 200, 12), f"Temperature {T} (°C)", "2D fin: temperature contours")

    fin_gmsh = load("heatConduction2DFinGmsh")
    out["fin-gmsh-mesh"] = mesh_figure(fin_gmsh, RECT_SIDES, "30 quadratic quadrilaterals, 141 nodes (rect_quad.msh)", "2D fin: Gmsh mesh rect_quad.msh")
    out["fin-gmsh-results"] = contour_figure(fin_gmsh, fin_gmsh["solution"], nice_levels(80, 200, 12), f"Temperature {T} (°C)", "2D fin, Gmsh mesh: temperature contours")

    rhomboid = load("heatConduction2DRhomFinGmsh")
    out["rhomboid-fin-geometry"] = rhomboid_geometry()
    rhomboid_sides = [(2, 0, "bottom", 0, "bottom"), (0.5, 1, "left", 1, RHOMBOID_LEFT), (3, 2, "top", 2, "top"), (4.5, 1, "right", 3, RHOMBOID_RIGHT)]
    out["rhomboid-fin-mesh"] = mesh_figure(rhomboid, rhomboid_sides, "24 quadratic quadrilaterals, 117 nodes (rhom_quad.msh)", "2D rhomboid fin: Gmsh mesh rhom_quad.msh")
    out["rhomboid-fin-results"] = contour_figure(rhomboid, rhomboid["solution"], nice_levels(85, 200, 12), f"Temperature {T} (°C)", "2D rhomboid fin: temperature contours")

    fin_varying = load("heatConduction2DVaryingKQ")
    out["fin-varying-geometry"] = fin_varying_geometry()
    out["fin-varying-results"] = contour_figure(fin_varying, fin_varying["solution"], nice_levels(190, 240, 10), f"Temperature {T} (°C)", "2D fin with varying k and Q: temperature contours")


    advection = load("advectionDiffusion1D")
    out["advection-diffusion-geometry"] = line_domain_geometry("1", f"{italic('u')}(0) = 1", f"d{italic('u')}/d{italic('x')} = 0", f"{second_derivative()}&#160;− 10 d{italic('u')}/d{italic('x')} = {italic('D')}({italic('x')})</tspan>", "Advection-diffusion in 1D", source=gaussian_source)
    out["advection-diffusion-mesh"] = domain_1d(advection, f"{italic('u')}(0) = 1", f"d{italic('u')}/d{italic('x')} = 0", "1", "Advection-diffusion: 20 quadratic elements")
    out["advection-diffusion-results"] = line_plot([(nodal_series(advection), False, nodal_series(advection)[::2], None, 0)], italic("x"), italic("u"), [0, 0.2, 0.4, 0.6, 0.8, 1], [0.85, 0.9, 0.95, 1], "Advection-diffusion: solution")

    reaction = load("nonlinearReactionDiffusion1D")
    out["reaction-diffusion-geometry"] = line_domain_geometry("10", f"{italic('u')}(0) = 1", f"d{italic('u')}/d{italic('x')} = 0", f"{second_derivative()}&#160;− {italic('u')}<tspan dy=\"-6\" font-size=\"11\">2</tspan><tspan dy=\"6\">&#160;= 0</tspan></tspan>", "Nonlinear reaction-diffusion in 1D")
    out["reaction-diffusion-mesh"] = domain_1d(reaction, f"{italic('u')}(0) = 1", f"d{italic('u')}/d{italic('x')} = 0", "10", "Nonlinear reaction-diffusion: 20 linear elements")
    out["reaction-diffusion-results"] = line_plot([(nodal_series(reaction), False, nodal_series(reaction), None, 0)], italic("x"), italic("u"), [0, 2, 4, 6, 8, 10], [0, 0.25, 0.5, 0.75, 1], "Nonlinear reaction-diffusion: solution")

    front = load("solidificationFront2D")
    out["solidification-geometry"] = solidification_geometry()
    out["solidification-mesh"] = mesh_figure(front, RECT_SIDES, "12 × 8 quadratic quadrilaterals, 425 nodes", "Solidification front: structured mesh")
    out["solidification-results"] = contour_figure(front, front["solution"], [0.25 * k for k in range(1, 8)], f"Front arrival {italic('u')} (distance from the initial front)", "Solidification front: contours of u")

    cavity = load("lidDrivenCavity2DCreepingFlow")
    out["cavity-geometry"] = cavity_geometry()
    out["cavity-mesh"] = mesh_figure(cavity, RECT_SIDES, "12 × 6 Q2-Q1 quadrilaterals, 325 velocity nodes, 91 pressure nodes", "Lid-driven cavity: structured mesh")
    out["cavity-results"] = contour_figure(cavity, cavity["fields"]["velocityMagnitude"], [], "Velocity vectors at the element corners (the lid moves at 1 m/s)", "Lid-driven cavity: velocity vectors", extra=velocity_arrows(cavity))

    couette = load("couetteFlow2DCreepingFlow")
    out["couette-mesh"] = mesh_figure(couette, RECT_SIDES, "4 × 2 Q2-Q1 quadrilaterals, 45 velocity nodes", "Couette flow: structured mesh")
    left_end = sorted((y, u) for x, y, u in zip(couette["x"], couette["y"], couette["fields"]["u"]) if abs(x) < 1e-9)
    out["couette-results"] = line_plot(
        [([(0, 0), (1, 2)], True, None, None, 0), (None, False, [(u, y) for y, u in left_end], None, 0)],
        f"{italic('u')} (m/s)", f"{italic('y')} (m)", [0, 0.25, 0.5, 0.75, 1], [0, 0.5, 1, 1.5, 2], "Couette flow: velocity profile at x = 0",
        legend=[(False, True, "FEAScript, nodes at x = 0"), (True, False, f"Exact, {italic('u')} = {italic('y')} / 2")],
    )

    cantilever = load("cantileverBeam1D")
    out["cantilever-geometry"] = cantilever_geometry()
    out["cantilever-results"] = line_plot(
        [(hermite_deflection(cantilever), False, list(zip(cantilever["x"], cantilever["fields"]["w"])), None, 0)],
        f"{italic('x')} (m)", f"Deflection {italic('w')} (m)", [0, 1, 2, 3, 4], [-0.25, -0.2, -0.15, -0.1, -0.05, 0], "Cantilever beam: deflection",
    )

    clamped = load("clampedSpringSupportedBeam1D")
    out["clamped-spring-beam-results"] = line_plot(
        [(hermite_deflection(clamped), False, list(zip(clamped["x"], clamped["fields"]["w"])), None, 0)],
        f"{italic('x')} (m)", f"Deflection {italic('w')} (m)", [0, 2, 4, 6, 8, 10], [-0.1, -0.08, -0.06, -0.04, -0.02, 0, 0.02], "Clamped and spring-supported beam: deflection",
    )
    return out


if __name__ == "__main__":
    for name in ["heatConduction2DFin", "heatConduction2DFinGmsh", "heatConduction2DRhomFinGmsh", "heatConduction2DVaryingKQ", "solidificationFront2D"]:
        record = load(name)
        (low, lx, ly), (high, hx, hy) = field_extremes(record, record["solution"])
        print(f"{name}: lowest {low:.4f} at ({lx:.3f}, {ly:.3f}), highest {high:.4f} at ({hx:.3f}, {hy:.3f})")
    os.makedirs(OUTPUT, exist_ok=True)
    for name, content in figures().items():
        with open(os.path.join(OUTPUT, f"{name}.svg"), "w") as handle:
            handle.write(content)
        print(f"Wrote static/assets/examples/{name}.svg")
