---
sidebar_position: 2
---

# Mesh

The mesh is defined with `model.setMeshConfig(meshConfig)`. FEAScript can either generate a structured mesh
from a few geometric parameters, or use an unstructured 2D mesh imported from [Gmsh](https://gmsh.info/).

## Structured meshes

A structured mesh covers a line ($0 \le x \le maxX$) in 1D, or a rectangle
($0 \le x \le maxX$, $0 \le y \le maxY$) in 2D, which can optionally be skewed into a trapezoid. 2D structured
meshes always consist of quadrilateral elements.

```javascript
// 1D: 20 quadratic elements on 0 ≤ x ≤ 0.15
model.setMeshConfig({
  meshDimension: "1D",
  elementOrder: "quadratic",
  numElementsX: 20,
  maxX: 0.15,
});

// 2D: 8 × 4 quadratic quadrilaterals on 0 ≤ x ≤ 4, 0 ≤ y ≤ 2
model.setMeshConfig({
  meshDimension: "2D",
  elementOrder: "quadratic",
  numElementsX: 8,
  numElementsY: 4,
  maxX: 4,
  maxY: 2,
});
```

| Property        | Type     | Required     | Description                                                   |
| --------------- | -------- | ------------ | ------------------------------------------------------------- |
| `meshDimension` | `string` | Yes          | `"1D"` or `"2D"`                                              |
| `elementOrder`  | `string` | No           | `"linear"` (default) or `"quadratic"`                         |
| `numElementsX`  | `number` | Yes          | Number of elements along $x$                                  |
| `maxX`          | `number` | Yes          | Length of the domain along $x$ (the domain starts at $x = 0$) |
| `numElementsY`  | `number` | 2D only      | Number of elements along $y$                                  |
| `maxY`          | `number` | 2D only      | Height of the domain along $y$ (the domain starts at $y = 0$) |
| `angleLeft`     | `number` | No (2D only) | Interior angle of the left side in degrees (default `90`)     |
| `angleRight`    | `number` | No (2D only) | Interior angle of the right side in degrees (default `90`)    |

### Boundaries of a structured mesh

The boundaries of a structured mesh are identified by the following keys, which are the first argument of
`addBoundaryCondition`:

![Boundary keys of the structured 1D and 2D meshes](/assets/mesh-boundaries.svg)

| Mesh | Key   | Boundary              |
| ---- | ----- | --------------------- |
| 1D   | `"0"` | Left end, $x = 0$     |
| 1D   | `"1"` | Right end, $x = maxX$ |
| 2D   | `"0"` | Bottom side, $y = 0$  |
| 2D   | `"1"` | Left side             |
| 2D   | `"2"` | Top side, $y = maxY$  |
| 2D   | `"3"` | Right side            |

:::note
The [Euler–Bernoulli beam](../models/euler-bernoulli-beam.md) model does not use these keys: its boundary
conditions are keyed by node number, so that supports and loads can also be placed at interior nodes.
:::

### Skewed (trapezoidal) domains

`angleLeft` and `angleRight` turn the rectangle into a trapezoid. Both angles are measured inside the domain,
from the bottom side, so `90` keeps the side vertical, a smaller angle leans the side towards the inside of the
domain and a larger one leans it outwards. The bottom side always spans $0 \le x \le maxX$, and the nodes of
every row are spaced uniformly between the left and right sides.

![Skewed 2D structured mesh defined by angleLeft and angleRight](/assets/skewed-mesh.svg)

```javascript
model.setMeshConfig({
  meshDimension: "2D",
  elementOrder: "linear",
  numElementsX: 6,
  numElementsY: 4,
  maxX: 4,
  maxY: 2,
  angleLeft: 60,
  angleRight: 75,
});
```

### Node numbering

The nodes of a structured mesh are numbered column by column: along $y$ first (bottom to top), then along
$x$ (left to right). In 2D, the node in column $i$ and row $j$ (both starting from zero) has the index

$$
\text{index} = i \cdot n_y + j,
$$

where $n_y$ is the number of nodes along $y$ ($n_y = numElementsY + 1$ for linear elements and
$n_y = 2 \cdot numElementsY + 1$ for quadratic elements). In 1D, the nodes are numbered from left to right.
This is also the order of the entries of the solution vector returned by `solve()`.

## Gmsh meshes

Unstructured 2D meshes made with Gmsh are read with [`importGmshMesh`](../api/gmsh-import.md) and passed to the
model through the `parsedMesh` property:

```javascript
const parsedMesh = await importGmshMesh(meshFile);
model.setMeshConfig({ parsedMesh });
```

The mesh dimension and the element order are detected from the file, so `meshDimension` and `elementOrder` can
be omitted. If they are given and differ from the mesh, FEAScript logs an error.

Supported Gmsh meshes:

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

Boundaries are taken from the **1D physical groups** (`Physical Curve` or `Physical Line` in a `.geo` file).
They are numbered in increasing order of their physical tag, starting from key `"0"`. When the physical curves
have the tags `1`, `2`, ..., the boundary key is the tag minus one. 2D physical groups (for example a
`Physical Surface`) do not define boundaries.

For example, with the following `.geo` definitions:

```
Physical Line("bottom") = {1}; // tag 1 → boundary key "0"
Physical Line("right")  = {2}; // tag 2 → boundary key "1"
Physical Line("top")    = {3}; // tag 3 → boundary key "2"
Physical Line("left")   = {4}; // tag 4 → boundary key "3"
Physical Surface("domain") = {1};
```

Generate the mesh in the supported format with:

```bash
gmsh rect.geo -2 -format msh41 -o rect.msh
```

Add `Recombine Surface{1};` in the `.geo` file for quadrilaterals, and `Mesh.ElementOrder = 2;` for quadratic
elements.
