"""Shared drawing helpers of the documentation figures.

Black line art on a transparent background (inverted in dark mode by src/css/custom.css), sans-serif 15 px labels,
boundary keys in grey 12 px, dashed dimension lines with arrows, and thin grey mesh edges.
"""

import math

DEFS = """  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" fill="#000"/>
    </marker>
  </defs>"""

HALO = 'stroke="#fff" stroke-width="4" stroke-linejoin="round" paint-order="stroke"'  # white outline behind labels

MESH_STYLE = 'fill="none" stroke="#000" stroke-width="0.6" stroke-opacity="0.45" stroke-linejoin="round"'


def fmt(value):
    return f"{value:.2f}".rstrip("0").rstrip(".")


def svg(width, height, body, comment):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" '
        f'font-family="sans-serif" font-size="15" fill="#000">\n  <!-- {comment} -->\n{DEFS}\n'
        + "\n".join("  " + line for line in body)
        + "\n</svg>\n"
    )


class Frame:
    """Maps model coordinates (y up) to SVG coordinates (y down)."""

    def __init__(self, x0, y0, scale):
        self.x0, self.y0, self.scale = x0, y0, scale

    def __call__(self, x, y):
        return self.x0 + self.scale * x, self.y0 - self.scale * y


def text(x, y, content, size=15, fill="#000", anchor="middle", rotate=None, weight=None):
    attributes = f'x="{fmt(x)}" y="{fmt(y)}"'
    if size != 15:
        attributes += f' font-size="{size}"'
    if fill != "#000":
        attributes += f' fill="{fill}"'
    if anchor != "start":
        attributes += f' text-anchor="{anchor}"'
    if weight:
        attributes += f' font-weight="{weight}"'
    if rotate is not None:
        attributes += f' transform="rotate({rotate} {fmt(x)} {fmt(y)})"'
    return f"<text {attributes}>{content}</text>"


def label(x, y, condition, key, side):
    """Boundary condition and its key, placed outside a domain edge (side: bottom, top, left or right)."""
    if side == "bottom":
        return [text(x, y + 22, condition), text(x, y + 38, key, 12, "#666")]
    if side == "top":
        return [text(x, y - 12, condition), text(x, y - 30, key, 12, "#666")]
    if side == "left":
        return [text(x - 14, y, condition, rotate=-90), text(x - 30, y, key, 12, "#666", rotate=-90)]
    return [text(x + 20, y, condition, rotate=90), text(x + 36, y, key, 12, "#666", rotate=90)]


def dimension(x1, y1, x2, y2, content, offset_x=0, offset_y=0, rotate=None):
    line = (
        f'<line x1="{fmt(x1)}" y1="{fmt(y1)}" x2="{fmt(x2)}" y2="{fmt(y2)}" stroke="#000" stroke-width="1" '
        'stroke-dasharray="4 3" marker-start="url(#arrow)" marker-end="url(#arrow)"/>'
    )
    return [line, text((x1 + x2) / 2 + offset_x, (y1 + y2) / 2 + offset_y, content, rotate=rotate)]


def outline(points, width=2):
    path = " ".join(f"{fmt(x)},{fmt(y)}" for x, y in points)
    return f'<polygon points="{path}" fill="none" stroke="#000" stroke-width="{width}" stroke-linejoin="round"/>'


def dot(x, y, radius=3, filled=True):
    fill = "#000" if filled else "#fff"
    return f'<circle cx="{fmt(x)}" cy="{fmt(y)}" r="{radius}" fill="{fill}" stroke="#000" stroke-width="1"/>'


def origin(frame):
    x, y = frame(0, 0)
    return [dot(x, y), text(x - 6, y + 20, "(0, 0)", 13)]


def italic(symbol):
    return f'<tspan font-style="italic">{symbol}</tspan>'


def sub(content):
    return f'<tspan dy="4" font-size="11">{content}</tspan><tspan dy="-4"></tspan>'


def structured_mesh(frame, width, height, nx, ny):
    lines = []
    for i in range(1, nx):
        x1, y1 = frame(width * i / nx, 0)
        x2, y2 = frame(width * i / nx, height)
        lines.append(f'<line x1="{fmt(x1)}" y1="{fmt(y1)}" x2="{fmt(x2)}" y2="{fmt(y2)}"/>')
    for j in range(1, ny):
        x1, y1 = frame(0, height * j / ny)
        x2, y2 = frame(width, height * j / ny)
        lines.append(f'<line x1="{fmt(x1)}" y1="{fmt(y1)}" x2="{fmt(x2)}" y2="{fmt(y2)}"/>')
    return [f"<g {MESH_STYLE}>"] + ["  " + line for line in lines] + ["</g>"]


def read_gmsh(path):
    """Nodes and 2D elements of a Gmsh 4.1 ASCII mesh, as polygons through all element edge nodes."""
    with open(path) as handle:
        lines = [line.strip() for line in handle]
    nodes, polygons = {}, []
    index = lines.index("$Nodes") + 1
    blocks = int(lines[index].split()[0])
    index += 1
    for _ in range(blocks):
        count = int(lines[index].split()[3])
        tags = [int(lines[index + 1 + k]) for k in range(count)]
        for k, tag in enumerate(tags):
            x, y, _ = map(float, lines[index + 1 + count + k].split())
            nodes[tag] = (x, y)
        index += 1 + 2 * count
    # Node order around each element: corners interleaved with edge nodes (Gmsh numbering)
    orders = {2: [0, 1, 2], 3: [0, 1, 2, 3], 9: [0, 3, 1, 4, 2, 5], 10: [0, 4, 1, 5, 2, 6, 3, 7]}
    index = lines.index("$Elements") + 1
    blocks = int(lines[index].split()[0])
    index += 1
    for _ in range(blocks):
        dim, _, element_type, count = map(int, lines[index].split())
        for k in range(count):
            if dim == 2 and element_type in orders:
                element = list(map(int, lines[index + 1 + k].split()))[1:]
                polygons.append([nodes[element[i]] for i in orders[element_type]])
        index += 1 + count
    return polygons


def gmsh_mesh(frame, polygons):
    body = [f"<g {MESH_STYLE}>"]
    for polygon in polygons:
        points = " ".join(f"{fmt(px)},{fmt(py)}" for px, py in (frame(x, y) for x, y in polygon))
        body.append(f'  <polygon points="{points}"/>')
    return body + ["</g>"]


def rectangle(frame, width, height):
    return outline([frame(0, 0), frame(width, 0), frame(width, height), frame(0, height)])


def log_plot(series, x_label, y_label, comment, width=640, height=360, padding=0.25):
    """Log-log plot with a legend in the top left corner.

    Gridlines and ticks are at the decades, labelled as powers of ten; an axis that spans less than two decades
    gets ticks at 1, 2 and 5 times the decades instead, labelled as plain numbers.

    series: list of (name, points), at most three. The first is a solid line with open circles, the second a
    dashed line with filled circles, as in the line plots of the example pages, and the third a dotted line with
    open squares.
    """
    left, right, top, bottom = 90, width - 40, 30, height - 60
    xs = [math.log10(x) for _, points in series for x, _ in points]
    ys = [math.log10(y) for _, points in series for _, y in points]
    x_min, x_max = min(xs) - padding, max(xs) + padding
    y_min, y_max = min(ys) - padding, max(ys) + padding

    def px(x):
        return left + (math.log10(x) - x_min) / (x_max - x_min) * (right - left)

    def py(y):
        return bottom - (math.log10(y) - y_min) / (y_max - y_min) * (bottom - top)

    def power(value):
        e = round(math.log10(value))
        if e == 0:
            return "1"
        if e == 1:
            return "10"
        return f'10<tspan dy="-6" font-size="10">{str(e).replace("-", "−")}</tspan>'

    def ticks(low, high):
        """Tick values and their labels between 10**low and 10**high."""
        decades = range(math.floor(low), math.ceil(high) + 1)
        if sum(1 for e in decades if low <= e <= high) >= 2:
            return [(10**e, power(10**e)) for e in decades if low <= e <= high]
        values = [m * 10**e for e in decades for m in (1, 2, 5)]
        return [(v, f"{v:g}") for v in values if low <= math.log10(v) <= high]

    x_ticks, y_ticks = ticks(x_min, x_max), ticks(y_min, y_max)
    body = ['<g stroke="#000" stroke-width="0.6" stroke-opacity="0.25">']
    body += [f'  <line x1="{fmt(px(v))}" y1="{top}" x2="{fmt(px(v))}" y2="{bottom}"/>' for v, _ in x_ticks]
    body += [f'  <line x1="{left}" y1="{fmt(py(v))}" x2="{right}" y2="{fmt(py(v))}"/>' for v, _ in y_ticks]
    body += ["</g>"]
    body += [f'<line x1="{left}" y1="{bottom}" x2="{right}" y2="{bottom}" stroke="#000" stroke-width="1"/>']
    body += [f'<line x1="{left}" y1="{top}" x2="{left}" y2="{bottom}" stroke="#000" stroke-width="1"/>']
    body += [text(px(v), bottom + 20, label, 13) for v, label in x_ticks]
    body += [text(left - 8, py(v) + 4, label, 13, anchor="end") for v, label in y_ticks]
    body += [text((left + right) / 2, height - 14, x_label)]
    body += [text(24, (top + bottom) / 2, y_label, rotate=-90)]
    def marker(k, x, y):
        if k == 2:  # Open square
            return f'<rect x="{fmt(x - 3.5)}" y="{fmt(y - 3.5)}" width="7" height="7" fill="#fff" stroke="#000" stroke-width="1"/>'
        return dot(x, y, 3.5, filled=k == 1)

    for k, (name, points) in enumerate(series):
        dash = ["", ' stroke-dasharray="5 4"', ' stroke-dasharray="1.5 3"'][k]
        path = " ".join(f"{fmt(px(x))},{fmt(py(y))}" for x, y in points)
        body.append(f'<polyline points="{path}" fill="none" stroke="#000" stroke-width="1.5"{dash}/>')
        body += [marker(k, px(x), py(y)) for x, y in points]
        ly = top + 18 + 22 * k
        body.append(f'<line x1="{left + 18}" y1="{ly}" x2="{left + 50}" y2="{ly}" stroke="#000" stroke-width="1.5"{dash}/>')
        body.append(marker(k, left + 34, ly))
        body.append(f'<text x="{left + 60}" y="{ly + 4}" font-size="13" {HALO}>{name}</text>')
    return svg(width, height, body, comment)
