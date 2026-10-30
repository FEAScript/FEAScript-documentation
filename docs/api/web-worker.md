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
| `setModelConfig(modelConfig, options)`         | `Promise<boolean>` | Selects the model and its options, as `FEAScriptModel`           |
| `setMeshConfig(meshConfig)`                    | `Promise<boolean>` | Sets the mesh, as `FEAScriptModel.setMeshConfig`                 |
| `addBoundaryCondition(boundaryKey, condition)` | `Promise<boolean>` | Adds a boundary condition                                        |
| `setSolverMethod(solverMethod)`                | `Promise<boolean>` | Selects the solver method                                        |
| `solve(options)`                               | `Promise<object>`  | Solves the model in the worker (`maxIterations`, `tolerance`)    |
| `getModelInfo()`                               | `Promise<object>`  | `{ solverConfig, meshConfig, boundaryConditions, solverMethod }` |
| `ping()`                                       | `Promise<boolean>` | Resolves to `true` when the worker is ready                      |
| `terminate()`                                  | –                  | Stops the worker                                                 |

`solve()` resolves to `{ solutionVector, nodesCoordinates, solverConfig, meshDimension }`, plus `fields` for the
creeping flow and Euler–Bernoulli beam models (see [Visualization](./visualization.md)). The object returned by
`getModelInfo()` can be passed as the `model` argument of the [plotting functions](./visualization.md).

## Model options

`setModelConfig` and `solve` take the same options as in `FEAScriptModel`, including `coefficientFunctions`,
`nonlinear`, `maxIterations` and `tolerance`:

```javascript
await model.setModelConfig("generalFormPDEScript", {
  coefficientFunctions: {
    A: (x) => 1, // Diffusion coefficient
    B: (x) => -10, // Advection coefficient
    C: (x) => 0, // Reaction coefficient
    D: (x) => 10 * Math.exp(-200 * Math.pow(x - 0.5, 2)), // Source term
  },
});
```

Functions cannot be sent to a web worker, so `FEAScriptWorker` sends each coefficient function as its source code
and rebuilds it in the worker. A rebuilt function does not have access to the variables around it, so write the
values into the function:

```javascript
const Da = 0.5;

// Does not work in the worker: Da is not defined there
D: (x, u) => Da * u ** 2,

// Works in the worker
D: (x, u) => 0.5 * u ** 2,
```

Use functions defined in your own code: built-in functions such as `Math.sin` must be wrapped, e.g.
`(x) => Math.sin(x)`. Rebuilding the functions requires `eval`, so a page with a
[Content Security Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP) must allow `'unsafe-eval'`.

## Limitations

- `solveAsync` and the `"jacobi-gpu"` method are not available through the worker.

## Examples

- [Solidification front in 2D with a web worker](https://feascript.com/tutorials/solidification-front-2d-worker.html)
- [Lid-driven cavity creeping flow in 2D with a web worker](https://feascript.com/tutorials/lid-driven-cavity-2d-creeping-flow-worker.html)
- [Heat conduction in a 2D fin with a web worker](https://feascript.com/tutorials/heat-conduction-2d-fin-worker.html)
