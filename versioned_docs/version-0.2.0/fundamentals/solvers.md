---
sidebar_position: 4
---

# Solvers

The linear system solver is selected with `model.setSolverMethod(solverMethod)`. If it is not set, FEAScript uses
`"lusolve"`.

```javascript
model.setSolverMethod("frontal");
```

| `solverMethod` | Method                                                                | Called with          |
| -------------- | --------------------------------------------------------------------- | -------------------- |
| `"lusolve"`    | Sparse LU decomposition (direct, from [math.js](https://mathjs.org/)) | `solve()`            |
| `"jacobi"`     | Jacobi iteration on the CPU                                           | `solve()`            |
| `"frontal"`    | Frontal solver (direct, element by element)                           | `solve()`            |
| `"jacobi-gpu"` | Jacobi iteration on the GPU with WebGPU                               | `await solveAsync()` |

In version 0.2.0 the system matrix is assembled as a dense array, so the memory use of `"lusolve"` and `"jacobi"`
grows with the square of the number of nodes. The frontal solver avoids this, since it never builds the whole
matrix.

## Supported combinations

| Model                    | `"lusolve"` | `"jacobi"` | `"frontal"` | `"jacobi-gpu"` |
| ------------------------ | :---------: | :--------: | :---------: | :------------: |
| `heatConductionScript`   |      ✓      |     ✓      |      ✓      |       ✓        |
| `generalFormPDEScript`   |      ✓      |     ✓      |             |                |
| `frontPropagationScript` |      ✓      |     ✓      |      ✓      |                |
| `creepingFlowScript`     |      ✓      |            |             |                |

For the nonlinear `frontPropagationScript` model, the selected method solves the linear system of each
Newton–Raphson iteration.

The creeping flow system has zero diagonal entries in its pressure rows, so the Jacobi method cannot be applied
to it; use `"lusolve"`.

## LU decomposition (`"lusolve"`)

The default method. The assembled matrix is converted to a math.js sparse matrix, factorized with the sparse LU
decomposition of math.js (with partial pivoting) and the system is solved directly. It works for every model and
needs no tuning, so it is a good first choice. It requires the global `math` object (see
[Installation](../getting-started/installation.md)).

## Frontal solver (`"frontal"`)

The frontal solver assembles and eliminates the equations element by element, so only the equations of the
active "front" are kept in memory instead of the whole matrix. Dirichlet conditions and, for heat conduction,
convection conditions are applied during the assembly of each element.

## Jacobi method (`"jacobi"`)

An iterative method: at each iteration, every unknown is updated from the values of the previous iteration,

$$
u_i^{(m+1)} = \frac{1}{\mathcal{J}_{ii}} \left( R_i - \sum_{j \ne i} \mathcal{J}_{ij} \, u_j^{(m)} \right),
$$

starting from $\bar{u}^{(0)} = 0$. The iterations stop when the largest absolute change between two iterations,
$\max_i \lvert u_i^{(m+1)} - u_i^{(m)} \rvert$, is smaller than the tolerance.

The Jacobi method converges only for suitable matrices, for example diagonally dominant ones. Linear elements
usually give such matrices; quadratic elements usually do not. If the method does not converge, FEAScript logs
an error and returns the last iterate.

| Option          | Default | Description                                 |
| --------------- | ------- | ------------------------------------------- |
| `maxIterations` | `10000` | Maximum number of Jacobi iterations         |
| `tolerance`     | `1e-4`  | Convergence tolerance on the largest change |

These options can be passed to `solve()` or `setModelConfig()` (see
[`FEAScriptModel`](../api/feascript-model.md)):

```javascript
model.setSolverMethod("jacobi");
const result = model.solve({ maxIterations: 200000, tolerance: 1e-8 });
```

## Jacobi method on the GPU (`"jacobi-gpu"`)

The same Jacobi iteration, run on the GPU with [WebGPU](https://developer.mozilla.org/en-US/docs/Web/API/WebGPU_API)
through [taichi.js](https://taichi-js.com/), in a separate web worker. It is used through the asynchronous
`solveAsync` method and is available for `heatConductionScript` only:

```javascript
import { FEAScriptModel } from "https://cdn.jsdelivr.net/npm/feascript@0.2.0/src/index.js";

model.setModelConfig("heatConductionScript");
// ...mesh and boundary conditions...
model.setSolverMethod("jacobi-gpu");
const result = await model.solveAsync();
```

:::caution
`"jacobi-gpu"` runs only in browsers that support WebGPU. Its web worker script is not part of the bundled build of
version 0.2.0, so import FEAScript from `src/index.js`, as above (see
[Installation](../getting-started/installation.md#in-the-browser)). The GPU kernel works on a **dense** copy of the
system matrix.
:::

The GPU computations use single precision (32-bit) floats. The `maxIterations` (default `10000`) and
`tolerance` (default `1e-4`) options have the same meaning as for `"jacobi"`, but the stopping criterion is the
largest absolute residual, $\max_i \lvert R_i - \sum_j \mathcal{J}_{ij} u_j \rvert$, which is checked every few
iterations.

## Newton–Raphson method

The nonlinear [front propagation](../models/front-propagation.md) model is solved with the Newton–Raphson method
(see [Finite element method](./finite-element-method.md#linear-and-nonlinear-systems)). It stops when
$\lVert \Delta \bar{u} \rVert_2$ is smaller than or equal to the tolerance. If the norm of an increment exceeds
$10^2$, the iterations are stopped and an error is logged.

| Option          | Default | Description                                   |
| --------------- | ------- | --------------------------------------------- |
| `maxIterations` | `100`   | Maximum number of Newton–Raphson iterations   |
| `tolerance`     | `1e-4`  | Tolerance on $\lVert \Delta \bar{u} \rVert_2$ |

These options apply to the Newton–Raphson iterations; the linear system of each iteration uses the defaults of the
selected method. See the [model page](../models/front-propagation.md#solution-procedure) for the solution
procedure.
