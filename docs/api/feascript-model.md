---
sidebar_position: 1
---

# FEAScriptModel

<img className="topic-logo" src="/assets/topics/model.svg" alt="" />

`FEAScriptModel` is the main class of FEAScript. It holds the configuration of a simulation (model, mesh,
boundary conditions and solver) and solves it.

```javascript
import { FEAScriptModel } from "feascript";

const model = new FEAScriptModel();
model.setModelConfig("heatConduction", { solver: { method: "lusolve" } });
model.setGeometry({ line: 0.15 });
model.setMeshConfig({ elementOrder: "linear", divisions: 10 });
model.addBoundaryCondition("left", { type: "convection", h: 1, ambientTemperature: 25 });
model.addBoundaryCondition("right", { type: "constantTemperature", temperature: 5 });
const { solutionVector, nodesCoordinates } = model.solve();
```

## Constructor

### `new FEAScriptModel()`

Creates an empty model. The solver method defaults to `"lusolve"`.

## Methods

### `setModelConfig(modelConfig, options)`

Selects the physical model and sets its options.

| Parameter     | Type     | Description                        |
| ------------- | -------- | ---------------------------------- |
| `modelConfig` | `string` | Name of the model (see below)      |
| `options`     | `object` | Optional model options (see below) |

| `modelConfig`          | Model                                                     | Dimensions |
| ---------------------- | --------------------------------------------------------- | ---------- |
| `"heatConduction"`     | [Heat conduction](../models/heat-conduction.md)           | 1D, 2D     |
| `"generalFormPDE"`     | [General-form PDE](../models/general-form-pde.md)         | 1D         |
| `"frontPropagation"`   | [Front propagation](../models/front-propagation.md)       | 1D, 2D     |
| `"creepingFlow"`       | [Creeping flow](../models/creeping-flow.md)               | 2D         |
| `"eulerBernoulliBeam"` | [Euler–Bernoulli beam](../models/euler-bernoulli-beam.md) | 1D         |

| Option                 | Type      | Used by                                                                | Description                                                           |
| ---------------------- | --------- | ---------------------------------------------------------------------- | --------------------------------------------------------------------- |
| `coefficientFunctions` | `object`  | Heat conduction, general-form PDE, creeping flow, Euler–Bernoulli beam | Coefficients of the equation; see each model page                     |
| `nonlinear`            | `boolean` | General-form PDE                                                       | Solve with the Newton–Raphson method (default `false`)                |
| `solver`               | `object`  | All                                                                    | The linear solver, `{ method, maxIterations, tolerance }` (see below) |
| `maxIterations`        | `number`  | All                                                                    | Maximum iterations of the iterative method in use                     |
| `tolerance`            | `number`  | All                                                                    | Convergence tolerance of the iterative method in use                  |

The `solver` option selects the linear system solver and sets its iterations:

| `solver` property | Type     | Description                                                                            |
| ----------------- | -------- | -------------------------------------------------------------------------------------- |
| `method`          | `string` | `"lusolve"` (default), `"jacobi"`, `"frontal"` or `"jacobi-gpu"` (with `solveAsync()`) |
| `maxIterations`   | `number` | Maximum iterations of the Jacobi solvers, also inside Newton–Raphson                   |
| `tolerance`       | `number` | Tolerance of the Jacobi solvers, on the residual relative to the right-hand side       |

An unknown method or property, or an iteration limit or tolerance that is not positive, throws a
`FEAScriptError` with the code `INVALID_INPUT`. See [Solvers](../fundamentals/solvers.mdx) for the methods
supported by each model.

The top-level `maxIterations` and `tolerance` apply to the Newton–Raphson method in nonlinear models, and to the
Jacobi solvers when `solver` does not set them; see [Solvers](../fundamentals/solvers.mdx) for their defaults.

The model names of FEAScript 0.3, with a `Script` suffix (e.g. `"heatConductionScript"`), still work, with a
warning; they will be removed in a future version, in 0.7.0 at the earliest.

```javascript
model.setModelConfig("heatConduction", {
  solver: { method: "frontal" },
  coefficientFunctions: {
    thermalConductivity: (x, y) => (x < 2 ? 10 : 1),
    heatSource: 0,
  },
});
```

### `setGeometry(geometry)`

Sets the domain and names its boundaries: `{ line: length }`, `{ rectangle: [width, height] }` or
`{ shape, holes, points }`, a polygon with holes whose boundaries are named, written as a path `{ start, boundaries: [{ name, to }] }`. See [Mesh](../fundamentals/mesh.md#geometry) for the forms and the boundary names. The geometry is
checked at once: a polygon that is not simple, a hole outside the shape or inside another hole, or a point
outside the domain throws a `FEAScriptError` of code `"INVALID_INPUT"` listing every problem.

### `setMeshConfig(meshConfig)`

Sets how the geometry is meshed. The mesh is generated at the first solve (or by `getMesh()`).

| Property       | Type                   | Description                                                                                                    |
| -------------- | ---------------------- | -------------------------------------------------------------------------------------------------------------- |
| `elements`     | `string`               | `"quadrilaterals"` (default; a rectangle or a convex four-point shape) or `"triangles"` (any shape with holes) |
| `elementOrder` | `string`               | `"linear"` (default) or `"quadratic"`                                                                          |
| `size`         | `number` or `function` | The length of an element side; for triangles also a function `(x, y)` of position                              |
| `divisions`    | `number` or `number[]` | Instead of `size`: the number of elements of a line, or `[nx, ny]` of a quadrilateral                          |
| `minAngle`     | `number`               | Triangles: the smallest angle of the elements, in degrees (default `20`)                                       |
| `maxNodes`     | `number`               | Triangles: the limit on the number of vertices (default `100000`)                                              |

The mesh settings of FEAScript 0.3 (`meshDimension`, `numElementsX`, `maxX`, `numElementsY`, `maxY`,
`angleLeft`, `angleRight`, and `parsedMesh`) keep working with a deprecation warning; see
[Mesh](../fundamentals/mesh.md#mesh-settings-of-feascript-03).

### `setMesh(mesh)`

Sets the mesh directly: a mesh imported with [`importGmshMesh`](./gmsh-import.md), or generated with
[`generateTriangleMesh` or `generateQuadrilateralMesh`](./mesh-generators.md). The geometry and the mesh
configuration are then not used. The boundaries of the mesh are keyed by their names.

### `getMesh()`

Returns the [mesh object](../fundamentals/mesh.md#meshes-as-objects) of the model, generating it from the
geometry and the mesh configuration at the first call. `getMeshDimension()` returns `"1D"` or `"2D"`.

### `addBoundaryCondition(boundaryKey, condition)`

Adds a boundary condition, or replaces the condition of a boundary that already has one.

| Parameter     | Type     | Description                                                                                                                                                                      |
| ------------- | -------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `boundaryKey` | `string` | The name of a boundary of the geometry or the mesh (e.g. `"top"`, see [Boundary names](../fundamentals/mesh.md#boundary-names)), or the node number for the Euler–Bernoulli beam |
| `condition`   | `object` | The condition type and its named parameters, e.g. `{ type: "convection", h: 1, ambientTemperature: 20 }`; for the Euler–Bernoulli beam, one such object or a list of them        |

See [Boundary conditions](../fundamentals/boundary-conditions.md) for the condition types of each model. A
condition object with no or an unknown type, or with a missing or unknown parameter, throws a `FEAScriptError`
with the code `INVALID_INPUT` when it is added; the other problems (a type that the selected model does not
have, a value that is not a number, a boundary that is not in the mesh) are reported when `solve()` runs (see
[Checks](../fundamentals/boundary-conditions.md#checks)). The array form of FEAScript 0.3, e.g.
`["convection", 1, 20]`, still works, with a warning.

### `setSolverMethod(solverMethod)`

Deprecated: use the `solver` option of `setModelConfig`, e.g.
`setModelConfig("heatConduction", { solver: { method: "jacobi" } })`. `setSolverMethod` still selects the
linear system solver, with a warning, and will be removed in a future version.

### `solve(options)`

Prepares the mesh, assembles the system, applies the boundary conditions and solves it. This method is
synchronous.

| Parameter | Type     | Description                                                                                                    |
| --------- | -------- | -------------------------------------------------------------------------------------------------------------- |
| `options` | `object` | Optional `{ maxIterations, tolerance }`; they take precedence over the `setModelConfig` options for this solve |

Returns an object with:

| Property                             | Type           | Description                                                              |
| ------------------------------------ | -------------- | ------------------------------------------------------------------------ |
| `solutionVector`                     | `Float64Array` | The computed unknowns (see the model pages)                              |
| `nodesCoordinates.nodesXCoordinates` | `number[]`     | $x$ coordinates of the mesh nodes                                        |
| `nodesCoordinates.nodesYCoordinates` | `number[]`     | $y$ coordinates of the mesh nodes (2D meshes)                            |
| `fields`                             | `object`       | Named fields, one value per node (models with several unknowns per node) |

For scalar models (heat conduction, general-form PDE, front propagation), `solutionVector` has one value per
node, in the order of `nodesCoordinates`, and there is no `fields` property. The
[creeping flow](../models/creeping-flow.md#results) (`velocityMagnitude`, `u`, `v`, `p`) and
[Euler–Bernoulli beam](../models/euler-bernoulli-beam.md#results) (`w`, `theta`) models have more unknowns per
node: `fields` holds each of them as a `Float64Array` with one value per node, ready to plot or post-process.

### `solveAsync(computeEngine, options)`

Asynchronous version of `solve`, used with the `"jacobi-gpu"` solver method. It returns a `Promise` that resolves
to the same object as `solve()`.

```javascript
model.setModelConfig("heatConduction", { solver: { method: "jacobi-gpu" } });
// ...mesh and boundary conditions...
const { solutionVector, nodesCoordinates } = await model.solveAsync();
```

| Parameter       | Type     | Description                                                                                                                                                                                        |
| --------------- | -------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `computeEngine` | `object` | Optional. An initialized WebGPU compute engine to reuse across solves. When omitted or `null`, FEAScript creates one for the solve and terminates it afterwards; a provided engine is left running |
| `options`       | `object` | Optional `{ maxIterations, tolerance }`                                                                                                                                                            |

:::caution
`solveAsync` currently supports only `heatConduction` with the `"jacobi-gpu"` solver method, in browsers
with WebGPU support. For other models or solver methods, it returns an empty solution vector.
:::

## Error handling

An input that FEAScript cannot use, or a solve that would return an empty or a wrong result, throws a
`FEAScriptError`, exported by the library, with one of these codes in `error.code`:

| Code                 | Meaning                                                                                                                                                                                                                                                            |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `INVALID_INPUT`      | A setting, a boundary condition or a coefficient that is missing, misspelled or out of range, for example a condition on a boundary that is not in the mesh or a coefficient the model does not use. Every problem found by one check is listed in `error.details` |
| `UNSUPPORTED_MESH`   | A mesh the model or the Gmsh reader cannot use yet, for example creeping flow on linear elements or a Gmsh mesh that mixes element shapes                                                                                                                          |
| `UNSUPPORTED_SOLVER` | The model does not support the solver method, or `solveAsync()` cannot run the model                                                                                                                                                                               |
| `NOT_CONVERGED`      | A Jacobi solve, a front propagation or a nonlinear general-form PDE did not converge                                                                                                                                                                               |
| `SINGULAR_MATRIX`    | The system has no unique solution, for example with a zero conductivity                                                                                                                                                                                            |
| `NON_FINITE_VALUES`  | A NaN or infinite value in the assembled system or in the solution, for example from a coefficient function that returns NaN somewhere                                                                                                                             |
| `MESH_TOO_FINE`      | The triangle mesh generator passed its `maxNodes` limit ([mesh generators](./mesh-generators.md))                                                                                                                                                                  |
| `INTERNAL_ERROR`     | A step of the frontal solver failed                                                                                                                                                                                                                                |

The checks run before the solve, so all the input mistakes are reported at once, in `error.details`. Through
`FEAScriptWorker` the error keeps its `code` and `details`.

Problems that do not stop the solve, for example a mesh setting that conflicts with an imported mesh (the value of
the mesh is used), are reported as `[WARN]` messages in the console. See [Logging](./utilities.md#logsystem) to
control the amount of output.
