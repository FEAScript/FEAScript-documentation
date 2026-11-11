---
sidebar_position: 2
---

# Your first simulation

<img className="topic-logo" src="/assets/topics/first-simulation.svg" alt="" />

This page walks through a complete simulation: steady-state heat conduction in a 2D fin, solved in the browser and
plotted with Plotly. The same steps apply to every model.

## The problem

A $4 \times 2$ fin is heated at its bottom and right sides, cooled by convection at its top side, and symmetric
about its left side. The temperature $T$ satisfies $\nabla^2 T = 0$ (heat conduction with $k = 1$ and no heat
source), with:

| Side   | Boundary name | Condition                            |
| ------ | ------------- | ------------------------------------ |
| Bottom | `"bottom"`    | Constant temperature, $T = 200$      |
| Left   | `"left"`      | Symmetry (zero heat flux)            |
| Top    | `"top"`       | Convection, $h = 1$, $T_\infty = 20$ |
| Right  | `"right"`     | Constant temperature, $T = 200$      |

## The code

Save the following as an `.html` file and open it through a local web server (for example
`npx serve` in the same folder):

```html
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8" />
    <script src="https://cdnjs.cloudflare.com/ajax/libs/plotly.js/2.35.3/plotly.min.js"></script>
  </head>
  <body>
    <div id="resultsCanvas"></div>

    <script type="module">
      import { FEAScriptModel, plotSolution } from "https://core.feascript.com/dist/feascript.esm.js";

      // 1. Create the model and select the physics
      const model = new FEAScriptModel();
      model.setModelConfig("heatConductionScript");

      // 2. Define the geometry and the mesh: a 4 by 2 rectangle, 8 × 4 quadratic quadrilaterals
      model.setGeometry({ rectangle: [4, 2] });
      model.setMeshConfig({ elements: "quadrilaterals", elementOrder: "quadratic", divisions: [8, 4] });

      // 3. Apply the boundary conditions
      model.addBoundaryCondition("bottom", ["constantTemperature", 200]);
      model.addBoundaryCondition("left", ["symmetry"]);
      model.addBoundaryCondition("top", ["convection", 1, 20]);
      model.addBoundaryCondition("right", ["constantTemperature", 200]);

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
   configuration of the simulation. `setModelConfig` takes the model name and, optionally, its coefficients. Here the
   defaults of the [heat conduction](../models/heat-conduction.md) model are used ($k = 1$, $Q = 0$).
2. **Define the geometry and the mesh.** `setGeometry` describes the domain, here a rectangle, and
   `setMeshConfig` how it is meshed: quadrilaterals or triangles, their order and their size or number (see
   [Mesh](../fundamentals/mesh.md)). A mesh imported from Gmsh is given with `setMesh` instead.
3. **Apply the boundary conditions.** The sides of a rectangle are named `"bottom"`, `"right"`, `"top"` and
   `"left"`. See [Boundary conditions](../fundamentals/boundary-conditions.md) for the condition types of every
   model.
4. **Solve.** `setSolverMethod` is optional (the default is `"lusolve"`). `solve()` returns the
   `solutionVector` and the `nodesCoordinates` of the mesh (see [Solvers](../fundamentals/solvers.mdx)).
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
import { FEAScriptModel } from "feascript";

// 1. Create the model and select the physics
const model = new FEAScriptModel();
model.setModelConfig("heatConductionScript");

// 2. Define the geometry and the mesh
model.setGeometry({ rectangle: [4, 2] });
model.setMeshConfig({ elements: "quadrilaterals", elementOrder: "quadratic", divisions: [8, 4] });

// 3. Apply the boundary conditions
model.addBoundaryCondition("bottom", ["constantTemperature", 200]);
model.addBoundaryCondition("left", ["symmetry"]);
model.addBoundaryCondition("top", ["convection", 1, 20]);
model.addBoundaryCondition("right", ["constantTemperature", 200]);

// 4. Solve
const { solutionVector, nodesCoordinates } = model.solve();

// 5. Print the results
console.log(`Number of nodes: ${nodesCoordinates.nodesXCoordinates.length}`);
console.log("Temperature:", solutionVector);
```

Run it with `node fin.js` (with `"type": "module"` in your `package.json`, see
[Installation](./installation.md)).

## Next steps

- Read about the [physical models](../models/heat-conduction.md) and their equations.
- Mesh a polygon with holes with triangles (see [Mesh](../fundamentals/mesh.md#polygon-with-holes)), or import
  an unstructured mesh with [`importGmshMesh`](../api/gmsh-import.md).
- Run the simulation in a [web worker](../api/web-worker.md), or on the GPU with the
  [`"jacobi-gpu"` solver](../fundamentals/solvers.mdx#jacobi-method-on-the-gpu-jacobi-gpu).
- Explore the [tutorials](https://feascript.com/tutorials/) on the FEAScript website and the
  [examples](https://github.com/FEAScript/FEAScript-core/tree/main/examples) of FEAScript-core.
