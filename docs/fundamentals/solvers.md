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

## Supported combinations

| Model                             | `"lusolve"` | `"jacobi"` | `"frontal"` | `"jacobi-gpu"` |
| --------------------------------- | :---------: | :--------: | :---------: | :------------: |
| `heatConductionScript`            |      ✓      |     ✓      |      ✓      |       ✓        |
| `generalFormPDEScript`, linear    |      ✓      |     ✓      |      ✓      |                |
| `generalFormPDEScript`, nonlinear |      ✓      |     ✓      |             |                |
| `frontPropagationScript`          |      ✓      |     ✓      |      ✓      |                |
| `creepingFlowScript`              |      ✓      |            |             |                |
| `eulerBernoulliBeamScript`        |      ✓      |     ✓      |             |                |

For the nonlinear models (`frontPropagationScript`, and `generalFormPDEScript` with `nonlinear: true`), the
selected method solves the linear system of each Newton–Raphson iteration.

The creeping flow system has zero diagonal entries in its pressure rows, so the Jacobi method cannot be applied
to it; use `"lusolve"`.

## LU decomposition (`"lusolve"`)

The default method. The assembled sparse matrix is factorized with the sparse LU decomposition of math.js
(with partial pivoting) and the system is solved directly. It works for every model and needs no tuning, so it
is a good first choice.

## Frontal solver (`"frontal"`)

The frontal solver assembles and eliminates the equations element by element, so only the equations of the
active "front" are kept in memory instead of the whole matrix. Dirichlet conditions and, for heat conduction,
convection conditions are applied during the assembly of each element.

## Jacobi method (`"jacobi"`)

An iterative method: at each iteration, every unknown is updated from the values of the previous iteration,

$$
u_i^{(m+1)} = \frac{1}{\mathcal{J}_{ii}} \left( R_i - \sum_{j \ne i} \mathcal{J}_{ij} \, u_j^{(m)} \right),
$$

starting from $\bar{u}^{(0)} = 0$. The iterations stop when the residual, relative to the right-hand side, is
smaller than the tolerance:

$$
\frac{\lVert \bar{R} - \mathcal{J} \bar{u}^{(m)} \rVert_2}{\lVert \bar{R} \rVert_2} < \text{tolerance}.
$$

The size of the change between two iterations is not used: the Jacobi method can converge slowly, so the changes
become small while the iterate is still far from the solution.

The Jacobi method converges only for suitable matrices, for example diagonally dominant ones. Linear elements
usually give such matrices; quadratic elements usually do not. If the method does not converge, FEAScript logs
an error and returns the last iterate.

| Option          | Default | Description                                     |
| --------------- | ------- | ----------------------------------------------- |
| `maxIterations` | `10000` | Maximum number of Jacobi iterations             |
| `tolerance`     | `1e-8`  | Tolerance on the residual relative to $\bar{R}$ |

These options can be passed to `solve()` or `setModelConfig()` (see
[`FEAScriptModel`](../api/feascript-model.md)):

```javascript
model.setSolverMethod("jacobi");
const result = model.solve({ maxIterations: 200000, tolerance: 1e-8 });
```

## Jacobi method on the GPU (`"jacobi-gpu"`)

The same Jacobi iteration, run on the GPU with [WebGPU](https://developer.mozilla.org/en-US/docs/Web/API/WebGPU_API)
through [taichi.js](https://taichi-js.com/), in a separate web worker. It is used through the asynchronous
`solveAsync` method and is currently available for `heatConductionScript` only:

```javascript
model.setModelConfig("heatConductionScript");
// ...mesh and boundary conditions...
model.setSolverMethod("jacobi-gpu");
const result = await model.solveAsync();
```

:::caution
`"jacobi-gpu"` runs only in browsers that support WebGPU, and the GPU kernel works on a **dense** copy of the
system matrix, so its memory use grows with the square of the number of nodes.
:::

The GPU computations use single precision (32-bit) floats. The `maxIterations` option (default `10000`) has the
same meaning as for `"jacobi"`. The `tolerance` option (default `1e-4`) applies to a different stopping criterion:
the largest absolute residual, $\max_i \lvert R_i - \sum_j \mathcal{J}_{ij} u_j \rvert$, which is checked every few
iterations.

## Newton–Raphson method

Nonlinear models are solved with the Newton–Raphson method (see
[Finite element method](./finite-element-method.md#linear-and-nonlinear-systems)). It starts from
$\bar{u} = 0$ and stops when $\lVert \Delta \bar{u} \rVert_2$ is smaller than or equal to the tolerance. If the
norm of an increment exceeds $10^2$, the iterations are stopped and an error is logged.

| Option          | Default | Description                                   |
| --------------- | ------- | --------------------------------------------- |
| `maxIterations` | `100`   | Maximum number of Newton–Raphson iterations   |
| `tolerance`     | `1e-4`  | Tolerance on $\lVert \Delta \bar{u} \rVert_2$ |

For `generalFormPDEScript`, these options apply to the Newton–Raphson iterations and the inner linear system
uses the defaults of the selected method. For `frontPropagationScript`, see the
[model page](../models/front-propagation.md#solution-procedure).
