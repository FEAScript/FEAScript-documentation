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
element has angles of at least `minAngle` and an area of at most `maxArea`.

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
