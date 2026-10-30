---
sidebar_position: 1
---

# FEAScriptModel

`FEAScriptModel` is the main class of FEAScript. It holds the configuration of a simulation (model, mesh,
boundary conditions and solver) and solves it.

```javascript
import * as math from "mathjs";
global.math = math;

import { FEAScriptModel } from "feascript";

const model = new FEAScriptModel();
model.setModelConfig("heatConductionScript");
model.setMeshConfig({ meshDimension: "1D", elementOrder: "linear", numElementsX: 10, maxX: 0.15 });
model.addBoundaryCondition("0", ["convection", 1, 25]);
model.addBoundaryCondition("1", ["constantTemp", 5]);
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

| `modelConfig`              | Model                                               | Dimensions |
| -------------------------- | --------------------------------------------------- | ---------- |
| `"heatConductionScript"`   | [Heat conduction](../models/heat-conduction.md)     | 1D, 2D     |
| `"generalFormPDEScript"`   | [General form PDE](../models/general-form-pde.md)   | 1D         |
| `"frontPropagationScript"` | [Front propagation](../models/front-propagation.md) | 2D         |
| `"creepingFlowScript"`     | [Creeping flow](../models/creeping-flow.md)         | 2D         |

| Option                 | Type     | Used by          | Description                                          |
| ---------------------- | -------- | ---------------- | ---------------------------------------------------- |
| `coefficientFunctions` | `object` | General form PDE | Coefficients of the equation; see the model page     |
| `maxIterations`        | `number` | All              | Maximum iterations of the iterative method in use    |
| `tolerance`            | `number` | All              | Convergence tolerance of the iterative method in use |

`maxIterations` and `tolerance` apply to the Jacobi solvers in linear models and to the Newton–Raphson method in
the front propagation model; see [Solvers](../fundamentals/solvers.md) for their defaults.

```javascript
model.setModelConfig("generalFormPDEScript", {
  coefficientFunctions: {
    A: (x) => 1,
    B: (x) => -10,
    C: (x) => 0,
    D: (x) => 10 * Math.exp(-200 * Math.pow(x - 0.5, 2)),
  },
});
```

### `setSolverConfig(solverConfig, options)`

Deprecated alias of `setModelConfig`, with the same parameters. It logs a deprecation warning; use
`setModelConfig`. It was removed in version 0.3.0.

### `setMeshConfig(meshConfig)`

Sets the mesh: either the parameters of a structured mesh or a mesh imported from Gmsh.

| Property        | Type     | Description                                                                       |
| --------------- | -------- | --------------------------------------------------------------------------------- |
| `meshDimension` | `string` | `"1D"` or `"2D"` (required, also for `parsedMesh`)                                |
| `elementOrder`  | `string` | `"linear"` (default) or `"quadratic"` (must match the elements of a `parsedMesh`) |
| `numElementsX`  | `number` | Number of elements along $x$ (structured mesh)                                    |
| `numElementsY`  | `number` | Number of elements along $y$ (structured 2D mesh)                                 |
| `maxX`          | `number` | Length of the domain along $x$ (structured mesh)                                  |
| `maxY`          | `number` | Height of the domain along $y$ (structured 2D mesh)                               |
| `angleLeft`     | `number` | Interior angle of the left side in degrees, default `90` (structured 2D mesh)     |
| `angleRight`    | `number` | Interior angle of the right side in degrees, default `90` (structured 2D mesh)    |
| `parsedMesh`    | `object` | Mesh returned by [`importGmshQuadTri`](./gmsh-import.md)                          |

See [Mesh](../fundamentals/mesh.md) for the geometry, the boundary keys and the node numbering.

### `addBoundaryCondition(boundaryKey, condition)`

Adds a boundary condition, or replaces the condition of a boundary that already has one.

| Parameter     | Type     | Description                                                             |
| ------------- | -------- | ----------------------------------------------------------------------- |
| `boundaryKey` | `string` | Boundary key (`"0"`, `"1"`, ...)                                        |
| `condition`   | `array`  | Condition type followed by its parameters, e.g. `["convection", 1, 20]` |

See [Boundary conditions](../fundamentals/boundary-conditions.md) for the condition types of each model.
Condition types that the selected model does not recognize are ignored without a message.

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

| Property                             | Type       | Description                                   |
| ------------------------------------ | ---------- | --------------------------------------------- |
| `solutionVector`                     | `number[]` | The computed unknowns (see the model pages)   |
| `nodesCoordinates.nodesXCoordinates` | `number[]` | $x$ coordinates of the mesh nodes             |
| `nodesCoordinates.nodesYCoordinates` | `number[]` | $y$ coordinates of the mesh nodes (2D meshes) |

For the heat conduction, general form PDE and front propagation models, `solutionVector` has one value per node,
in the order of `nodesCoordinates`. For the [creeping flow](../models/creeping-flow.md#results) model, it holds
the velocity components and the pressure in consecutive blocks.

### `solveAsync(computeEngine, options)`

Asynchronous version of `solve`, used with the `"jacobi-gpu"` solver method. It returns a `Promise` that resolves
to the same object as `solve()`.

```javascript
model.setSolverMethod("jacobi-gpu");
const { solutionVector, nodesCoordinates } = await model.solveAsync();
```

| Parameter       | Type     | Description                                                                          |
| --------------- | -------- | ------------------------------------------------------------------------------------ |
| `computeEngine` | `object` | Not used in version 0.2.0: FEAScript creates a WebGPU compute engine for every solve |
| `options`       | `object` | Optional `{ maxIterations, tolerance }`                                              |

:::caution
`solveAsync` supports only `heatConductionScript` with the `"jacobi-gpu"` solver method, in browsers with WebGPU
support, with FEAScript imported from `src/index.js` (see
[Solvers](../fundamentals/solvers.md#jacobi-method-on-the-gpu-jacobi-gpu)). For other models or solver methods, it
returns an empty solution vector.
:::

## Error handling

FEAScript reports configuration problems (for example a creeping flow model on linear elements, or a solver that
did not converge) as `[ERROR]` messages in the console, and in most cases continues instead of throwing an
exception. Some invalid configurations, such as a missing `meshDimension`, end in a JavaScript error later in the
solution. Check the console output when a result looks wrong.
