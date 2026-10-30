---
sidebar_position: 4
---

# FEAScriptWorker

`FEAScriptWorker` runs a `FEAScriptModel` in a [web worker](https://developer.mozilla.org/en-US/docs/Web/API/Web_Workers_API),
so a long simulation does not block the page. It has the same configuration methods as `FEAScriptModel`, but every
method is asynchronous and returns a `Promise`.

:::note
`FEAScriptWorker` is available in the browser only. In version 0.2.0 the worker script is not part of the bundled
build, so import FEAScript from `src/index.js`, as below. The worker loads its own copy of math.js from a CDN.
:::

```javascript
import { FEAScriptWorker, plotSolution } from "https://cdn.jsdelivr.net/npm/feascript@0.2.0/src/index.js";

// 1. Create the model in a web worker and select the physics
const model = new FEAScriptWorker();
await model.ping(); // Wait until the worker is ready
await model.setModelConfig("frontPropagationScript");

// 2. Define the mesh
await model.setMeshConfig({
  meshDimension: "2D",
  elementOrder: "quadratic",
  numElementsX: 12,
  numElementsY: 8,
  maxX: 4,
  maxY: 2,
});

// 3. Apply the boundary conditions
await model.addBoundaryCondition("0", ["constantValue", 0]); // Bottom: initial front
await model.addBoundaryCondition("1", ["constantValue", 0]); // Left: initial front
await model.addBoundaryCondition("2", ["zeroGradient"]); // Top
await model.addBoundaryCondition("3", ["constantValue", 0]); // Right: initial front

// 4. Solve
await model.setSolverMethod("lusolve");
const result = await model.solve();

// 5. Plot the results in the main thread
const modelInfo = await model.getModelInfo();
plotSolution(modelInfo, result, "contour", "resultsCanvas");

// 6. Terminate the worker
model.terminate();
```

## Methods

| Method                                         | Returns            | Description                                                      |
| ---------------------------------------------- | ------------------ | ---------------------------------------------------------------- |
| `setModelConfig(modelConfig)`                  | `Promise<boolean>` | Selects the model (no options, see below)                        |
| `setMeshConfig(meshConfig)`                    | `Promise<boolean>` | Sets the mesh, as `FEAScriptModel.setMeshConfig`                 |
| `addBoundaryCondition(boundaryKey, condition)` | `Promise<boolean>` | Adds a boundary condition                                        |
| `setSolverMethod(solverMethod)`                | `Promise<boolean>` | Selects the solver method                                        |
| `solve()`                                      | `Promise<object>`  | Solves the model in the worker                                   |
| `getModelInfo()`                               | `Promise<object>`  | `{ solverConfig, meshConfig, boundaryConditions, solverMethod }` |
| `ping()`                                       | `Promise<boolean>` | Resolves to `true` when the worker is ready                      |
| `terminate()`                                  | –                  | Stops the worker                                                 |

`solve()` resolves to `{ solutionVector, nodesCoordinates, solverConfig, meshDimension }`. The object returned by
`getModelInfo()` can be passed as the `model` argument of the [plotting functions](./visualization.md).

## Limitations

- `setModelConfig` takes the model name only, and `solve()` takes no options. Model options
  (`coefficientFunctions`, `maxIterations`, `tolerance`) cannot be set through the worker, so the
  [general form PDE](../models/general-form-pde.md) model, which needs coefficient functions, cannot run in it.
  Version 0.3.0 added the model options to `FEAScriptWorker`.
- The worker does not expose `model._creepingFlowMetadata`. For the creeping flow model, compute the number of
  velocity nodes from the coordinates instead: `result.nodesCoordinates.nodesXCoordinates.length`.
- `solveAsync` and the `"jacobi-gpu"` method are not available through the worker.
