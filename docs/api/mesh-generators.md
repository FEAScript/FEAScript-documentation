---
sidebar_position: 3
---

# Mesh generators

<img className="topic-logo" src="/assets/topics/mesh.svg" alt="" />

```javascript
const mesh = generateTriangleMesh(geometry, { size, minAngle, elementOrder, maxNodes });
const mesh = generateQuadrilateralMesh(geometry, { size, divisions, elementOrder });
model.setMesh(mesh);
```

The two generators behind `setGeometry` and `setMeshConfig`, exported for a mesh that is inspected, plotted or
reused before it is solved on. Both take a geometry, in the form of [`setGeometry`](../fundamentals/mesh.md#geometry)
(`{ rectangle }` or `{ shape, holes, points }`), and return a [mesh object](../fundamentals/mesh.md#meshes-as-objects),
the same as [`importGmshMesh`](./gmsh-import.md), for `model.setMesh(mesh)`. The boundaries of the mesh are keyed
by the names of the geometry.

Both throw a [`FEAScriptError`](./feascript-model.md#error-handling) with the code `"INVALID_INPUT"` for a
polygon that is not simple (its edges cross), a hole outside the shape or inside another hole, a point outside
the domain, a path that does not end at its start, or a setting out of range, listing every problem found.

## `generateTriangleMesh(geometry, options)`

Meshes a polygon, with or without holes, with triangles: a constrained Delaunay triangulation of the input
points, refined by Ruppert's algorithm until every element has angles of at least `minAngle` and an area of at
most that of the equilateral triangle of side `size`. See [Algorithm and software](#algorithm-and-software).

| Option         | Type                   | Description                                                                                                                                                                    |
| -------------- | ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `size`         | `number` or `function` | The length of an element side, as a number, or as a function `(x, y)` of the element center for a mesh size that varies. Without it, only the angles are refined               |
| `minAngle`     | `number`               | The smallest angle of the elements, in degrees (default `20`). The refinement always stops below 20.7 degrees, and usually up to about 33; above that, it may reach `maxNodes` |
| `elementOrder` | `string`               | `"linear"` (3-node triangles, default) or `"quadratic"` (6-node triangles)                                                                                                     |
| `maxNodes`     | `number`               | The limit on the number of vertices (the corner nodes of the elements) before the refinement stops with a `"MESH_TOO_FINE"` error (default `100000`)                           |

### Example

A rectangular plate with a square hole, quadratic elements of side 0.15 at most:

```javascript
import { FEAScriptModel, generateTriangleMesh } from "feascript";

const mesh = generateTriangleMesh(
  {
    rectangle: [2, 1],
    holes: [
      {
        name: "hole",
        points: [
          [0.8, 0.4],
          [1.2, 0.4],
          [1.2, 0.6],
          [0.8, 0.6],
        ],
      },
    ],
  },
  { size: 0.15, minAngle: 25, elementOrder: "quadratic" },
);

const model = new FEAScriptModel();
model.setModelConfig("heatConduction", { coefficientFunctions: { thermalConductivity: 1 } });
model.setMesh(mesh);
model.addBoundaryCondition("bottom", { type: "constantTemperature", temperature: 100 });
model.addBoundaryCondition("right", { type: "symmetry" });
model.addBoundaryCondition("top", { type: "constantTemperature", temperature: 0 });
model.addBoundaryCondition("left", { type: "symmetry" });
model.addBoundaryCondition("hole", { type: "convection", h: 1, ambientTemperature: 20 });
const { solutionVector, nodesCoordinates } = model.solve();
```

The function works the same in the browser and in Node.js; it reads no files.

## `generateQuadrilateralMesh(geometry, options)`

Meshes a rectangle, or any convex shape of exactly four points without holes or embedded points, with a grid of
quadrilateral elements mapped onto the shape by its corners (a bilinear map). The rows of nodes run from the
bottom side (the first edge of the shape) to the top side, and the columns from the left side to the right
side; the nodes are numbered column by column, as in
[Node numbering](../fundamentals/mesh.md#node-numbering).

| Option         | Type       | Description                                                                                                                                      |
| -------------- | ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| `size`         | `number`   | The length of an element side: each side of the shape is divided into `round(length / size)` elements, the longer of two opposite sides deciding |
| `divisions`    | `number[]` | `[nx, ny]`, the number of elements along the bottom and the left side, instead of `size`                                                         |
| `elementOrder` | `string`   | `"linear"` (4-node elements, default) or `"quadratic"` (9-node elements)                                                                         |

A shape with more than four points, a non-convex one, holes, embedded points, or a `size` function throw
`"INVALID_INPUT"`; triangles cover those cases.

```javascript
import { generateQuadrilateralMesh } from "feascript";

const mesh = generateQuadrilateralMesh(
  { rectangle: [4, 2] },
  { elementOrder: "quadratic", divisions: [8, 4] },
);
console.log(mesh.nodesXCoordinates.length); // 153 nodes
```

## Algorithm and software

The triangle generator works in two stages:

1. **Constrained Delaunay triangulation** of the input points. The Delaunay triangulation is computed with
   [Delaunator](https://github.com/mapbox/delaunator) (ISC license), and the edges of the shape and of the
   holes are then forced into it with [Constrainautor](https://github.com/kninnug/Constrainautor) (ISC
   license), by flipping the edges that cross them. Triangles outside the shape or inside a hole are removed.
2. **Delaunay refinement**, Ruppert's algorithm [1]: a boundary edge that has a vertex inside its diametral
   circle is split at its midpoint, and a triangle that is too skinny or too large gets a new vertex. The
   new vertex is the off-center of the triangle [2], which lies closer to its short edge than the
   circumcenter and gives fewer vertices; a vertex that would fall inside the diametral circle of a boundary
   edge splits that edge instead, as in Triangle [3]. Where two edges of the input meet at a small angle, they
   are split at the same distances from the corner, in powers of two, and the skinny triangles between them
   are accepted, so that the refinement ends [4]. The vertices are inserted in passes, and the triangulation is
   rebuilt after each pass.

The orientation and in-circle tests use the exact, adaptive-precision predicates of Shewchuk [5], through
[robust-predicates](https://github.com/mourner/robust-predicates) (Unlicense), so a point exactly on an edge
or on a circle is decided correctly. The same predicates check the geometry (edges that cross, holes and points
inside the shape) for both generators. The libraries are listed with their licenses in the
[NOTICE](https://github.com/FEAScript/FEAScript-core/blob/main/NOTICE.md) file of FEAScript-core.

The quality guarantees are those of the algorithm: the refinement always ends for a `minAngle` below 20.7
degrees, and usually up to about 33, apart from the triangles at the small input angles, which keep their
angles.

The quadrilateral generator is the transfinite (bilinear) map of a grid onto the four corners, the mapped mesh
of the finite element textbooks [6]; it needs no external software.

### References

1. J. Ruppert, "A Delaunay refinement algorithm for quality 2-dimensional mesh generation," _Journal of
   Algorithms_, vol. 18, no. 3, pp. 548–585, 1995.
2. A. Üngör, "Off-centers: A new type of Steiner points for computing size-optimal quality-guaranteed
   Delaunay triangulations," in _LATIN 2004: Theoretical Informatics_, Lecture Notes in Computer Science,
   vol. 2976, pp. 152–161, 2004.
3. J. R. Shewchuk, "Delaunay refinement algorithms for triangular mesh generation," _Computational Geometry:
   Theory and Applications_, vol. 22, no. 1–3, pp. 21–74, 2002.
4. G. L. Miller, S. E. Pav and N. J. Walkington, "When and why Ruppert's algorithm works," in _Proceedings of
   the 12th International Meshing Roundtable_, pp. 91–102, 2003.
5. J. R. Shewchuk, "Adaptive precision floating-point arithmetic and fast robust geometric predicates,"
   _Discrete & Computational Geometry_, vol. 18, no. 3, pp. 305–363, 1997.
6. W. J. Gordon and C. A. Hall, "Construction of curvilinear co-ordinate systems and applications to mesh
   generation," _International Journal for Numerical Methods in Engineering_, vol. 7, no. 4, pp. 461–477, 1973.
