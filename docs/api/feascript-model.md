---
sidebar_position: 1
---

# FEAScriptModel

`FEAScriptModel` is the main class of FEAScript. It holds the configuration of a simulation (model, mesh,
boundary conditions and solver) and solves it.

```javascript
import { FEAScriptModel } from "feascript";

const model = new FEAScriptModel();
model.setModelConfig("heatConductionScript");
model.setMeshConfig({ meshDimension: "1D", elementOrder: "linear", numElementsX: 10, maxX: 0.15 });
model.addBoundaryCondition("0", ["convection", 1, 25]);
model.addBoundaryCondition("1", ["constantTemperature", 5]);
model.setSolverMethod("lusolve");
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

| `modelConfig`                | Model                                                     | Dimensions |
| ---------------------------- | --------------------------------------------------------- | ---------- |
| `"heatConductionScript"`     | [Heat conduction](../models/heat-conduction.md)           | 1D, 2D     |
| `"generalFormPDEScript"`     | [General form PDE](../models/general-form-pde.md)         | 1D         |
| `"frontPropagationScript"`   | [Front propagation](../models/front-propagation.md)       | 1D, 2D     |
| `"creepingFlowScript"`       | [Creeping flow](../models/creeping-flow.md)               | 2D         |
| `"eulerBernoulliBeamScript"` | [Euler–Bernoulli beam](../models/euler-bernoulli-beam.md) | 1D         |

| Option                 | Type      | Used by                                                 | Description                                            |
| ---------------------- | --------- | ------------------------------------------------------- | ------------------------------------------------------ |
| `coefficientFunctions` | `object`  | Heat conduction, general form PDE, Euler–Bernoulli beam | Coefficients of the equation; see each model page      |
| `nonlinear`            | `boolean` | General form PDE                                        | Solve with the Newton–Raphson method (default `false`) |
| `maxIterations`        | `number`  | All                                                     | Maximum iterations of the iterative method in use      |
| `tolerance`            | `number`  | All                                                     | Convergence tolerance of the iterative method in use   |

`maxIterations` and `tolerance` apply to the Jacobi solvers in linear models and to the Newton–Raphson method in
nonlinear models; see [Solvers](../fundamentals/solvers.md) for their defaults.

```javascript
model.setModelConfig("heatConductionScript", {
  coefficientFunctions: {
    thermalConductivity: (x, y) => (x < 2 ? 10 : 1),
    heatSource: 0,
  },
});
```

### `setMeshConfig(meshConfig)`

Sets the mesh: either the parameters of a structured mesh or a mesh imported from Gmsh.

| Property        | Type     | Description                                                                     |
| --------------- | -------- | ------------------------------------------------------------------------------- |
| `meshDimension` | `string` | `"1D"` or `"2D"` (detected automatically for `parsedMesh`)                      |
| `elementOrder`  | `string` | `"linear"` (default) or `"quadratic"` (detected automatically for `parsedMesh`) |
| `numElementsX`  | `number` | Number of elements along $x$ (structured mesh)                                  |
| `numElementsY`  | `number` | Number of elements along $y$ (structured 2D mesh)                               |
| `maxX`          | `number` | Length of the domain along $x$ (structured mesh)                                |
| `maxY`          | `number` | Height of the domain along $y$ (structured 2D mesh)                             |
| `angleLeft`     | `number` | Interior angle of the left side in degrees, default `90` (structured 2D mesh)   |
| `angleRight`    | `number` | Interior angle of the right side in degrees, default `90` (structured 2D mesh)  |
| `parsedMesh`    | `object` | Mesh returned by [`importGmshMesh`](./gmsh-import.md)                           |

See [Mesh](../fundamentals/mesh.md) for the geometry, the boundary keys and the node numbering.

### `addBoundaryCondition(boundaryKey, condition)`

Adds a boundary condition, or replaces the condition of a boundary that already has one.

| Parameter     | Type     | Description                                                                   |
| ------------- | -------- | ----------------------------------------------------------------------------- |
| `boundaryKey` | `string` | Boundary key (`"0"`, `"1"`, ...), or node number for the Euler–Bernoulli beam |
| `condition`   | `array`  | Condition type followed by its parameters, e.g. `["convection", 1, 20]`       |

See [Boundary conditions](../fundamentals/boundary-conditions.md) for the condition types of each model.
Condition types that the selected model does not recognize are reported as errors when `solve()` runs (see
[Checks](../fundamentals/boundary-conditions.md#checks)).

### `setSolverMethod(solverMethod)`

Selects the linear system solver: `"lusolve"` (default), `"jacobi"`, `"frontal"` or `"jacobi-gpu"`. See
[Solvers](../fundamentals/solvers.md) for the methods supported by each model.

### `solve(options)`

Prepares the mesh, assembles the system, applies the boundary conditions and solves it. This method is
synchronous.

| Parameter | Type     | Description                                                                                 |
| --------- | -------- | ------------------------------------------------------------------------------------------- |
| `options` | `object` | Optional `{ maxIterations, tolerance }`; they take precedence over `setModelConfig` options |

Returns an object with:

| Property                             | Type           | Description                                                              |
| ------------------------------------ | -------------- | ------------------------------------------------------------------------ |
| `solutionVector`                     | `Float64Array` | The computed unknowns (see the model pages)                              |
| `nodesCoordinates.nodesXCoordinates` | `number[]`     | $x$ coordinates of the mesh nodes                                        |
| `nodesCoordinates.nodesYCoordinates` | `number[]`     | $y$ coordinates of the mesh nodes (2D meshes)                            |
| `fields`                             | `object`       | Named fields, one value per node (models with several unknowns per node) |

For scalar models (heat conduction, general form PDE, front propagation), `solutionVector` has one value per
node, in the order of `nodesCoordinates`, and there is no `fields` property. The
[creeping flow](../models/creeping-flow.md#results) (`velocityMagnitude`, `u`, `v`, `p`) and
[Euler–Bernoulli beam](../models/euler-bernoulli-beam.md#results) (`w`, `theta`) models have more unknowns per
node: `fields` holds each of them as a `Float64Array` with one value per node, ready to plot or post-process.

### `solveAsync(computeEngine, options)`

Asynchronous version of `solve`, used with the `"jacobi-gpu"` solver method. It returns a `Promise` that resolves
to the same object as `solve()`.

```javascript
model.setSolverMethod("jacobi-gpu");
const { solutionVector, nodesCoordinates } = await model.solveAsync();
```

| Parameter       | Type     | Description                                                                                                                                                                                        |
| --------------- | -------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `computeEngine` | `object` | Optional. An initialized WebGPU compute engine to reuse across solves. When omitted or `null`, FEAScript creates one for the solve and terminates it afterwards; a provided engine is left running |
| `options`       | `object` | Optional `{ maxIterations, tolerance }`                                                                                                                                                            |

:::caution
`solveAsync` currently supports only `heatConductionScript` with the `"jacobi-gpu"` solver method, in browsers
with WebGPU support. For other models or solver methods, it returns an empty solution vector.
:::

## Error handling

FEAScript reports configuration problems (for example an unsupported mesh for a model, or a solver that did not
converge) as `[ERROR]` messages in the console, and in most cases continues instead of throwing an exception.
Check the console output when a result looks wrong. See [Logging](./utilities.md#logsystem) to control the
amount of output.
