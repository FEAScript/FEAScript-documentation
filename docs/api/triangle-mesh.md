---
sidebar_position: 3
---

# generateTriangleMesh

<img className="topic-logo" src="/assets/topics/mesh.svg" alt="" />

```javascript
const parsedMesh = generateTriangleMesh({
  polygon,
  holes,
  points,
  maxArea,
  minAngle,
  elementOrder,
  maxNodes,
});
```

Meshes a polygon, with or without holes, with triangles, and returns the mesh in the form that `setMeshConfig`
expects through its `parsedMesh` property, the same as [`importGmshMesh`](./gmsh-import.md). See
[Mesh](../fundamentals/mesh.md#generated-triangle-meshes) for how the boundaries are named and for examples.

The mesh is a constrained Delaunay triangulation of the input points, refined by Ruppert's algorithm until every
element has angles of at least `minAngle` and an area of at most `maxArea`. See
[Algorithm and software](#algorithm-and-software) below.

| Parameter      | Type                   | Required | Description                                                                                                                                                                                                                                                                                               |
| -------------- | ---------------------- | -------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `polygon`      | `array` or `object`    | Yes      | The outer boundary: the points `[x, y]` of a polygon, or `{ points, boundaries }`, where `boundaries` is one name for all the edges or one name per edge (edge $i$ goes from point $i$ to point $i + 1$, and the last edge closes the polygon). Without names, every edge is in the boundary `"boundary"` |
| `holes`        | `array`                | No       | The holes, each a polygon in the same form. The default name of their edges is `"hole"`                                                                                                                                                                                                                   |
| `points`       | `array`                | No       | Points `[x, y]` inside the domain, or on its boundary, that become nodes                                                                                                                                                                                                                                  |
| `maxArea`      | `number` or `function` | No       | The largest element area, as a number, or as a function `(x, y)` of the element center for a mesh size that varies. Without it, only the angles are refined                                                                                                                                               |
| `minAngle`     | `number`               | No       | The smallest angle of the elements, in degrees (default `20`). The refinement always stops below 20.7 degrees, and usually up to about 33; above that, it may reach `maxNodes`                                                                                                                            |
| `elementOrder` | `string`               | No       | `"linear"` (3-node triangles, default) or `"quadratic"` (6-node triangles)                                                                                                                                                                                                                                |
| `maxNodes`     | `number`               | No       | The limit on the number of vertices (the corner nodes of the elements) before the refinement stops with an error (default `100000`)                                                                                                                                                                       |

Returns the mesh, with `meshDimension` (`"2D"`) and `elementOrder` set, so that `setMeshConfig` needs nothing
else. The boundaries are numbered in the order their names first appear, the outer polygon first and then the
holes, and get the keys `"0"`, `"1"`, `"2"`, ... in that order.

Throws a [`FEAScriptError`](./feascript-model.md#error-handling) with the code `"INVALID_INPUT"` for a polygon
that is not simple (its edges cross), a hole or a point outside the domain, a list of names that does not match
the edges, or a setting out of range, and `"MESH_TOO_FINE"` when the refinement passes `maxNodes`.

## Example

A rectangular plate with a square hole, quadratic elements of area 0.01 at most:

```javascript
import { FEAScriptModel, generateTriangleMesh } from "feascript";

const parsedMesh = generateTriangleMesh({
  polygon: {
    points: [
      [0, 0],
      [2, 0],
      [2, 1],
      [0, 1],
    ],
    boundaries: ["bottom", "right", "top", "left"],
  },
  holes: [
    {
      points: [
        [0.8, 0.4],
        [1.2, 0.4],
        [1.2, 0.6],
        [0.8, 0.6],
      ],
      boundaries: "hole",
    },
  ],
  maxArea: 0.01,
  minAngle: 25,
  elementOrder: "quadratic",
});

const model = new FEAScriptModel();
model.setModelConfig("heatConductionScript", { coefficientFunctions: { thermalConductivity: 1 } });
model.setMeshConfig({ parsedMesh });
model.addBoundaryCondition("0", ["constantTemperature", 100]); // bottom
model.addBoundaryCondition("1", ["symmetry"]); // right
model.addBoundaryCondition("2", ["constantTemperature", 0]); // top
model.addBoundaryCondition("3", ["symmetry"]); // left
model.addBoundaryCondition("4", ["convection", 1, 20]); // hole
const { solutionVector, nodesCoordinates } = model.solve();
```

The function works the same in the browser and in Node.js; it reads no files.

## Algorithm and software

The generator works in two stages:

1. **Constrained Delaunay triangulation** of the input points. The Delaunay triangulation is computed with
   [Delaunator](https://github.com/mapbox/delaunator) (ISC license), and the edges of the polygon and of the
   holes are then forced into it with [Constrainautor](https://github.com/kninnug/Constrainautor) (ISC
   license), by flipping the edges that cross them. Triangles outside the polygon or inside a hole are
   removed.
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
or on a circle is decided correctly. The libraries are listed with their licenses in the
[NOTICE](https://github.com/FEAScript/FEAScript-core/blob/main/NOTICE.md) file of FEAScript-core.

The quality guarantees are those of the algorithm: the refinement always ends for a `minAngle` below 20.7
degrees, and usually up to about 33, apart from the triangles at the small input angles, which keep their
angles.

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
