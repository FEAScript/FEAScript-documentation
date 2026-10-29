---
sidebar_position: 4
---

# FEAScriptWorker

`FEAScriptWorker` runs a `FEAScriptModel` in a [web worker](https://developer.mozilla.org/en-US/docs/Web/API/Web_Workers_API),
so a long simulation does not block the page. It has the same configuration methods as `FEAScriptModel`, but every
method is asynchronous and returns a `Promise`.

:::note
`FEAScriptWorker` is available in the browser only. It loads `feascript-worker.esm.js` from the same folder as
`feascript.esm.js`, so keep the two files together when you host the library yourself.
:::

```javascript
import { FEAScriptWorker, plotSolution } from "https://core.feascript.com/dist/feascript.esm.js";

const model = new FEAScriptWorker();
await model.ping(); // Wait until the worker is ready

await model.setModelConfig("frontPropagationScript");
await model.setMeshConfig({
  meshDimension: "2D",
  elementOrder: "quadratic",
  numElementsX: 12,
  numElementsY: 8,
  maxX: 4,
  maxY: 2,
});
await model.addBoundaryCondition("0", ["constantValue", 0]);
await model.addBoundaryCondition("1", ["constantValue", 0]);
await model.addBoundaryCondition("2", ["zeroGradient"]);
await model.addBoundaryCondition("3", ["constantValue", 0]);
await model.setSolverMethod("lusolve");

const result = await model.solve();

// Plot in the main thread
const modelInfo = await model.getModelInfo();
plotSolution(modelInfo, result, "contour", "resultsCanvas");

model.terminate();
```

## Methods

| Method                                         | Returns            | Description                                                      |
| ---------------------------------------------- | ------------------ | ---------------------------------------------------------------- |
| `setModelConfig(modelConfig)`                  | `Promise<boolean>` | Selects the model (name only, see the note below)                |
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

- `setModelConfig` takes only the model name: model options such as `coefficientFunctions`, `nonlinear`,
  `maxIterations` and `tolerance` cannot be passed to the worker (functions cannot be sent to a web worker). Models
  that need coefficient functions (the general form PDE and the Euler–Bernoulli beam) can therefore not run in
  the worker yet, and heat conduction runs with the default coefficients ($k = 1$, $Q = 0$).
- `solve()` takes no options, so the solvers run with their default `maxIterations` and `tolerance`.
- `solveAsync` and the `"jacobi-gpu"` method are not available through the worker.

## Examples

- [Solidification front in 2D with a web worker](https://feascript.com/tutorials/solidification-front-2d-worker.html)
- [Lid-driven cavity creeping flow in 2D with a web worker](https://feascript.com/tutorials/lid-driven-cavity-2d-creeping-flow-worker.html)
- [Heat conduction in a 2D fin with a web worker](https://feascript.com/tutorials/heat-conduction-2d-fin-worker.html)
