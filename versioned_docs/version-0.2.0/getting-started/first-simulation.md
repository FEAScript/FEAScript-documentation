---
sidebar_position: 2
---

# Your first simulation

This page walks through a complete simulation: steady-state heat conduction in a 2D fin, solved in the browser and
plotted with Plotly. The same steps apply to every model.

## The problem

A $4 \times 2$ fin is heated at its bottom and right sides, cooled by convection at its top side, and symmetric
about its left side. The temperature $T$ satisfies $\nabla^2 T = 0$ (heat conduction with $k = 1$ and no heat
source), with:

| Side   | Boundary key | Condition                            |
| ------ | ------------ | ------------------------------------ |
| Bottom | `"0"`        | Constant temperature, $T = 200$      |
| Left   | `"1"`        | Symmetry (zero heat flux)            |
| Top    | `"2"`        | Convection, $h = 1$, $T_\infty = 20$ |
| Right  | `"3"`        | Constant temperature, $T = 200$      |

## The code

Save the following as an `.html` file and open it through a local web server (for example
`npx serve` in the same folder):

```html
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8" />
    <script src="https://cdnjs.cloudflare.com/ajax/libs/mathjs/11.12.0/math.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/plotly.js/2.35.3/plotly.min.js"></script>
  </head>
  <body>
    <div id="resultsCanvas"></div>

    <script type="module">
      import {
        FEAScriptModel,
        plotSolution,
      } from "https://cdn.jsdelivr.net/npm/feascript@0.2.0/dist/feascript.esm.js";

      // 1. Create the model and select the physics
      const model = new FEAScriptModel();
      model.setModelConfig("heatConductionScript");

      // 2. Define the mesh: 8 × 4 quadratic quadrilaterals on 0 ≤ x ≤ 4, 0 ≤ y ≤ 2
      model.setMeshConfig({
        meshDimension: "2D",
        elementOrder: "quadratic",
        numElementsX: 8,
        numElementsY: 4,
        maxX: 4,
        maxY: 2,
      });

      // 3. Apply the boundary conditions
      model.addBoundaryCondition("0", ["constantTemp", 200]); // Bottom
      model.addBoundaryCondition("1", ["symmetry"]); // Left
      model.addBoundaryCondition("2", ["convection", 1, 20]); // Top
      model.addBoundaryCondition("3", ["constantTemp", 200]); // Right

      // 4. Solve
      model.setSolverMethod("lusolve");
      const result = model.solve();

      // 5. Plot the results
      plotSolution(model, result, "contour", "resultsCanvas");
    </script>
  </body>
</html>
```

## Step by step

1. **Create the model and select the physics.** [`FEAScriptModel`](../api/feascript-model.md) holds the whole
   configuration of the simulation. `setModelConfig` takes the name of the model, here
   [heat conduction](../models/heat-conduction.md).
2. **Define the mesh.** `setMeshConfig` generates a structured mesh from the size of the domain and the number of
   elements (see [Mesh](../fundamentals/mesh.md)), or uses a mesh imported from Gmsh.
3. **Apply the boundary conditions.** The sides of a structured 2D mesh have the keys `"0"` (bottom), `"1"`
   (left), `"2"` (top) and `"3"` (right). See [Boundary conditions](../fundamentals/boundary-conditions.md) for the
   condition types of every model.
4. **Solve.** `setSolverMethod` is optional (the default is `"lusolve"`). `solve()` returns the
   `solutionVector` and the `nodesCoordinates` of the mesh (see [Solvers](../fundamentals/solvers.md)).
5. **Plot the results.** [`plotSolution`](../api/visualization.md) draws the result in the `resultsCanvas` element.

## The result

`result.solutionVector` holds the temperature at every node, and `result.nodesCoordinates` the coordinates of the
nodes, in the same order:

```javascript
const { solutionVector, nodesCoordinates } = result;
const { nodesXCoordinates, nodesYCoordinates } = nodesCoordinates;

for (let i = 0; i < solutionVector.length; i++) {
  console.log(nodesXCoordinates[i], nodesYCoordinates[i], solutionVector[i]);
}
```

## The same simulation in Node.js

```javascript
import * as math from "mathjs";
global.math = math;

import { FEAScriptModel } from "feascript";

// 1. Create the model and select the physics
const model = new FEAScriptModel();
model.setModelConfig("heatConductionScript");

// 2. Define the mesh
model.setMeshConfig({
  meshDimension: "2D",
  elementOrder: "quadratic",
  numElementsX: 8,
  numElementsY: 4,
  maxX: 4,
  maxY: 2,
});

// 3. Apply the boundary conditions
model.addBoundaryCondition("0", ["constantTemp", 200]); // Bottom
model.addBoundaryCondition("1", ["symmetry"]); // Left
model.addBoundaryCondition("2", ["convection", 1, 20]); // Top
model.addBoundaryCondition("3", ["constantTemp", 200]); // Right

// 4. Solve
const { solutionVector, nodesCoordinates } = model.solve();

// 5. Print the results
console.log(`Number of nodes: ${nodesCoordinates.nodesXCoordinates.length}`);
console.log("Temperature:", solutionVector);
```

Run it with `node fin.js` (with `"type": "module"` in your `package.json`, and `feascript@0.2.0` and `mathjs`
installed, see [Installation](./installation.md)).

## Next steps

- Read about the [physical models](../models/heat-conduction.md) and their equations.
- Import an unstructured mesh with [`importGmshQuadTri`](../api/gmsh-import.md).
- Run the simulation in a [web worker](../api/web-worker.md), or on the GPU with the
  [`"jacobi-gpu"` solver](../fundamentals/solvers.md#jacobi-method-on-the-gpu-jacobi-gpu).
- Explore the [examples](https://github.com/FEAScript/FEAScript-core/tree/0.2.0/examples) of FEAScript-core 0.2.0.
