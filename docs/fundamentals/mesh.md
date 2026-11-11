---
sidebar_position: 2
---

# Mesh

<img className="topic-logo" src="/assets/topics/mesh.svg" alt="" />

A domain is set up in two steps: `model.setGeometry(geometry)` describes the domain and names its boundaries,
and `model.setMeshConfig(meshConfig)` says how to mesh it, with quadrilateral or triangle elements of a given
order and size. The mesh is generated at the first solve. A mesh made elsewhere, imported from
[Gmsh](https://gmsh.info/) or generated with the [mesh generators](../api/mesh-generators.md), is given directly
with `model.setMesh(mesh)`.

```javascript
// A 4 by 2 rectangle, meshed with 8 × 4 quadratic quadrilaterals
model.setGeometry({ rectangle: [4, 2] });
model.setMeshConfig({ elements: "quadrilaterals", elementOrder: "quadratic", divisions: [8, 4] });
model.addBoundaryCondition("top", { type: "convection", h: 1, ambientTemperature: 20 });
```

The boundary conditions are keyed by the names of the boundaries, which the geometry defines.

## Geometry

### Line

`{ line: length }` is a 1D domain from $x = 0$ to $x = length$. Its boundaries are `"left"` ($x = 0$) and
`"right"` ($x = length$).

```javascript
model.setGeometry({ line: 0.15 });
model.setMeshConfig({ elementOrder: "quadratic", divisions: 20 }); // 20 quadratic elements
```

### Rectangle

`{ rectangle: [width, height] }` is the rectangle $0 \le x \le width$, $0 \le y \le height$. Its boundaries are
`"bottom"` ($y = 0$), `"right"` ($x = width$), `"top"` ($y = height$) and `"left"` ($x = 0$).

![Boundary names of the line and the rectangle](/assets/mesh-boundaries.svg)

### Polygon with holes

`{ shape, holes: [polygon, ...], points: [[x, y], ...] }` is any 2D domain. The shape is written as a **path**: a
`start` point and the list of its boundaries, each running from where the previous one ended to its `to` point.
The last boundary may leave out `to`: it then closes the shape back to `start`. Every corner is written once.

```javascript
// An L-shaped domain: a 2 by 2 square without its top right quarter
model.setGeometry({
  shape: {
    start: [0, 0],
    boundaries: [
      { name: "bottom", to: [2, 0] },
      { name: "right", to: [2, 1] },
      { name: "step", to: [1, 1] },
      { name: "step", to: [1, 2] }, // The same name: one boundary of two segments
      { name: "top", to: [0, 2] },
      { name: "left" }, // No "to": closes the shape back to [0, 0]
    ],
  },
});
model.setMeshConfig({ elements: "triangles", elementOrder: "quadratic", size: 0.1 });
```

- Boundaries with the same name form one boundary of the model, so a side made of several segments, or two
  sides with the same condition, share a name. A `to` may also be a list of points, a polyline, for a side with
  many points (`to: [[2, 1], [1, 1], [1, 2]]`).
- A polygon whose edges all have one name is written `{ name, points: [[x, y], ...] }`; this is the usual form
  of a hole. A plain list of `[x, y]` points is a polygon in the boundary `"boundary"` (a shape) or `"hole"` (a
  hole). The points may run in either direction around the domain.
- `holes` are polygons inside the shape. A hole must lie inside the shape and not inside another hole;
  otherwise `setGeometry` throws a `FEAScriptError` of code `"INVALID_INPUT"` that says which point is outside.
- `points` are points inside the domain, or on its boundary, that must become nodes, for example where a result
  is read. A point outside the domain is an error.
- The polygons must be simple: an edge that crosses or touches another one, a repeated edge, or a path that does
  not end at its start, stop `setGeometry` with an `"INVALID_INPUT"` error listing every problem.
- The domain is one shape in this version. Several shapes, meeting edge to edge as blocks, come in 0.5.0 with
  a key of their own, and other kinds of boundary segments (arcs, for example) can be added to a boundary later;
  the path form stays the same.

A plate with a circular hole, approximated by 32 segments:

```javascript
const circle = (cx, cy, r, n) =>
  Array.from({ length: n }, (_, i) => [
    cx + r * Math.cos((2 * Math.PI * i) / n),
    cy + r * Math.sin((2 * Math.PI * i) / n),
  ]);
model.setGeometry({ rectangle: [2, 1], holes: [{ name: "hole", points: circle(1, 0.5, 0.2, 32) }] });
```

### Boundary names

The boundary conditions are keyed by name, for every kind of geometry and mesh:

| Geometry or mesh          | Boundary names                                                              |
| ------------------------- | --------------------------------------------------------------------------- |
| `{ line }`                | `"left"`, `"right"`                                                         |
| `{ rectangle }`           | `"bottom"`, `"right"`, `"top"`, `"left"`                                    |
| `{ shape, holes }`        | The names given to the boundaries (`"boundary"` and `"hole"` without names) |
| [Gmsh mesh](#gmsh-meshes) | The names of the 1D physical groups                                         |

:::note
The [Euler–Bernoulli beam](../models/euler-bernoulli-beam.md) model does not use these names: its boundary
conditions are keyed by node number, so that supports and loads can also be placed at interior nodes.
:::

The numeric keys of FEAScript 0.3 keep working as aliases, with a deprecation warning: `"0"` and `"1"` for the
ends of a line, `"0"` (bottom), `"1"` (left), `"2"` (top) and `"3"` (right) for a rectangle, and the physical tag
minus one for a Gmsh mesh. They are removed in a later release; use the names.

## Mesh configuration

`setMeshConfig` takes how the geometry is meshed:

| Property       | Type                   | Description                                                                                                                                          |
| -------------- | ---------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| `elements`     | `string`               | `"quadrilaterals"` (default) or `"triangles"`. A line has 1D elements, whatever the value                                                            |
| `elementOrder` | `string`               | `"linear"` (default) or `"quadratic"`                                                                                                                |
| `size`         | `number` or `function` | The length of an element side. For triangles, also a function `(x, y)` of position, for a mesh size that varies                                      |
| `divisions`    | `number` or `number[]` | Instead of `size`: the number of elements of a line, or `[nx, ny]` along the bottom and the left side of a quadrilateral, for an exact element count |
| `minAngle`     | `number`               | Triangles: the smallest angle of the elements, in degrees (default `20`)                                                                             |
| `maxNodes`     | `number`               | Triangles: the limit on the number of vertices before the refinement stops with a `"MESH_TOO_FINE"` error (default `100000`)                         |

### Quadrilateral elements

`elements: "quadrilaterals"` meshes a rectangle, or any convex shape of exactly four points, with a grid of
`nx × ny` elements mapped onto the shape by its corners (a bilinear map): the rows of nodes run from the bottom
side to the top side, and the columns from the left side to the right side. Each side is divided into
`round(length / size)` elements, the longer of two opposite sides deciding, or into the `divisions` given. A
shape with more than four points, with holes or with embedded points cannot be meshed with quadrilaterals in
this version; use triangles, or split the domain into blocks (0.5.0).

A trapezoid, or any convex four-sided shape, is a polygon of four points:

```javascript
// A trapezoid of base 4 and height 2, whose sides lean at 60° and 75° to the base
model.setGeometry({
  shape: {
    start: [0, 0],
    boundaries: [
      { name: "bottom", to: [4, 0] },
      { name: "right", to: [3.464, 2] },
      { name: "top", to: [1.155, 2] },
      { name: "left" },
    ],
  },
});
model.setMeshConfig({ elements: "quadrilaterals", elementOrder: "linear", divisions: [6, 4] });
```

![A 6 by 4 mesh of quadrilaterals mapped onto a trapezoid](/assets/skewed-mesh.svg)

#### Node numbering

The nodes of a quadrilateral mesh are numbered column by column: along the left side first, then towards the
right side. The node in column $i$ and row $j$ (both starting from zero) has the index

$$
\text{index} = i \cdot n_y + j,
$$

where $n_y$ is the number of nodes along the left side ($n_y = ny + 1$ for linear elements and
$n_y = 2 \cdot ny + 1$ for quadratic elements). In 1D, the nodes are numbered from left to right. This is also
the order of the entries of the solution vector returned by `solve()`.

### Triangle elements

`elements: "triangles"` meshes any shape, with holes and embedded points, by Delaunay refinement: the points of
the geometry are triangulated, and vertices are inserted until every element has angles of at least `minAngle`
and an area of at most that of the equilateral triangle of side `size`. A function of position grades the mesh,
for example towards a corner where the solution varies fast:

```javascript
// Element side 0.01 at the re-entrant corner (1, 1), growing to 0.05 away from it
model.setMeshConfig({
  elements: "triangles",
  elementOrder: "quadratic",
  size: (x, y) => Math.min(0.05, 0.01 + 0.2 * Math.hypot(x - 1, y - 1)),
  minAngle: 30,
});
```

The refinement always ends for a `minAngle` below 20.7 degrees, and in practice up to about 33. A larger
angle, or a very small `size`, can make it pass `maxNodes` (default 100,000 vertices), which stops it with a
`FEAScriptError` of code `"MESH_TOO_FINE"`. The node and element counts are logged at the `"basic"` level.

#### How the mesh is built

The generator starts from the points given, triangulates them (a constrained Delaunay triangulation, with the
edges of the shape and of the holes forced in) and then inserts vertices one pass at a time: a boundary edge
is split at its midpoint when a vertex lies inside its diametral circle, and a triangle that is too skinny or
too large gets a vertex near its short edge (its off-center). The triangulation is rebuilt after each pass, so
the result is always a proper triangulation: every edge is shared by two triangles, or by one on the boundary,
and no vertex lies in the middle of another triangle's edge. The algorithm, the software it uses and the
references are on the [mesh generators](../api/mesh-generators.md#algorithm-and-software) page.

Because the boundary edges are split at their midpoints, a rectangle given by its four corners is meshed with
a symmetric pattern of right triangles, built from halves and quarters of its sides: a valid mesh, with all
angles at 45 or 90 degrees, but a very regular one. For a mesh of well-shaped triangles of varied orientation,
give the boundaries points along the sides at about the element size; the refinement then starts from a boundary
that already has the right size:

```javascript
// The 4 by 2 rectangle with a point every 0.5 along its sides
const along = (from, to, count) =>
  Array.from({ length: count + 1 }, (_, i) => [
    from[0] + ((to[0] - from[0]) * i) / count,
    from[1] + ((to[1] - from[1]) * i) / count,
  ]);
model.setGeometry({
  shape: {
    start: [0, 0],
    boundaries: [
      { name: "bottom", to: along([0, 0], [4, 0], 8).slice(1) },
      { name: "right", to: along([4, 0], [4, 2], 4).slice(1) },
      { name: "top", to: along([4, 2], [0, 2], 8).slice(1) },
      { name: "left", to: along([0, 2], [0, 0], 4).slice(1) },
    ],
  },
});
model.setMeshConfig({ elements: "triangles", size: 0.5, minAngle: 30 });
```

For a rectangle or a four-sided shape, quadrilaterals are the simpler choice; the triangle generator is for the
shapes a grid cannot cover.

The nodes of a triangle mesh are numbered in the order the generator creates them. This is the order of the
entries of the solution vector; the coordinates of the nodes are in `nodesCoordinates`.

## Gmsh meshes

Unstructured 2D meshes made with Gmsh are read with [`importGmshMesh`](../api/gmsh-import.md) and given to the
model with `setMesh`:

```javascript
const mesh = await importGmshMesh(meshFile);
model.setMesh(mesh);
```

The mesh dimension and the element order are detected from the file. Supported Gmsh meshes:

- `.msh` file format version 4.1, ASCII
- 2D meshes only
- Quadrilaterals or triangles, linear or quadratic:

  | Gmsh element      | Gmsh type | FEAScript element        |
  | ----------------- | --------- | ------------------------ |
  | 3-node triangle   | 2         | Triangle, linear         |
  | 4-node quadrangle | 3         | Quadrilateral, linear    |
  | 6-node triangle   | 9         | Triangle, quadratic      |
  | 9-node quadrangle | 10        | Quadrilateral, quadratic |

- All elements of a mesh must have the same shape and the same order (mixed meshes are not supported).

### Boundaries of a Gmsh mesh

Boundaries are taken from the **1D physical groups** (`Physical Curve` or `Physical Line` in a `.geo` file),
and keyed by their names. 2D physical groups (for example a `Physical Surface`) do not define boundaries, but
one is needed: once any physical group is defined, Gmsh saves only the elements that belong to one, so without a
`Physical Surface` the file has no 2D elements (unless `Mesh.SaveAll = 1`). For a rectangle whose lines 1, 2, 3,
4 are the bottom, right, top and left sides:

```
Physical Line("bottom") = {1};
Physical Line("right") = {2};
Physical Line("top") = {3};
Physical Line("left") = {4};
Physical Surface("domain") = {1};
```

```javascript
model.setMesh(mesh);
model.addBoundaryCondition("bottom", { type: "constantTemperature", temperature: 200 });
model.addBoundaryCondition("top", { type: "convection", h: 1, ambientTemperature: 20 });
```

A group without a name is keyed by its tag minus one. The tag minus one is also kept as a deprecated alias of
every name, the key of FEAScript 0.3.

Generate the mesh in the supported format with:

```bash
gmsh rect.geo -2 -format msh41 -o rect.msh
```

Add `Recombine Surface{1};` in the `.geo` file for quadrilaterals, and `Mesh.ElementOrder = 2;` for quadratic
elements.

## Meshes as objects

`importGmshMesh`, [`generateTriangleMesh` and `generateQuadrilateralMesh`](../api/mesh-generators.md) all return
a mesh object, and `setMesh` takes one. The object holds the nodes (`nodesXCoordinates`, `nodesYCoordinates`),
the elements (`nodalNumbering`, the node numbers of each element, from 1), the element sides on each boundary
(`boundaryElements`, keyed by name), the aliases of the names, and `meshDimension`, `elementOrder` and
`elementShape`. A model's own mesh is available through `model.getMesh()`, which generates it from the geometry
and the mesh configuration if needed, so a mesh can be inspected, plotted or reused in another model.

## Mesh settings of FEAScript 0.3

`setMeshConfig({ meshDimension, elementOrder, numElementsX, maxX, numElementsY, maxY, angleLeft, angleRight })`
of FEAScript 0.3 keeps working with a deprecation warning: it is translated into a line, a rectangle or a
four-point shape (the trapezoid of `angleLeft` and `angleRight`) with `divisions`, and its numeric boundary keys
stay as aliases. `setMeshConfig({ parsedMesh })` is translated into `setMesh(parsedMesh)`. Both forms are
removed in 0.7.0 at the earliest.
