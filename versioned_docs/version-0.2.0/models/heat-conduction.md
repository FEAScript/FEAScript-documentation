---
sidebar_position: 1
---

# Heat conduction

`heatConductionScript` solves steady-state heat conduction in 1D and 2D, with unit thermal conductivity and no heat
source.

## Governing equation

$$
-\nabla \cdot \left( k \, \nabla T \right) = 0 \quad \text{in} \quad D, \qquad k = 1,
$$

where $T$ is the temperature and $k$ the thermal conductivity. In 1D the equation reduces to
$\frac{d^2 T}{dx^2} = 0$.

:::note
In version 0.2.0, the thermal conductivity is fixed to $k = 1$ and there is no volumetric heat source. A constant
conductivity other than one can be taken into account by dividing the convection coefficients $h$ by $k$.
Spatially varying $k$ and a heat source $Q$ were added in version 0.3.0.
:::

The boundary $\partial D$ is split into parts with prescribed temperature (Dirichlet), convective heat exchange
(Robin), and zero heat flux (Neumann):

$$
\begin{aligned}
T &= T_b && \text{constant temperature}, \\
-k \, \frac{\partial T}{\partial n} &= h \, (T - T_\infty) && \text{convection}, \\
-k \, \frac{\partial T}{\partial n} &= 0 && \text{symmetry or insulation},
\end{aligned}
$$

where $h$ is the convective heat transfer coefficient, $T_\infty$ the temperature of the surrounding fluid and
$\partial / \partial n$ the derivative along the outward normal.

## Weak form

After integration by parts, the Galerkin residuals are

$$
R_i = \int_{D} k \, \nabla \phi^i \cdot \nabla T \, dS
+ \int_{\partial D_{conv}} h \, (T - T_\infty) \, \phi^i \, dt,
\qquad i = 1, 2, \dots, N,
$$

where $\partial D_{conv}$ is the part of the boundary with convection. On the rest of the boundary, the boundary
integral vanishes (zero heat flux) or the residual is replaced by the Dirichlet condition. In 1D the boundary
integral reduces to the value $h \, (T - T_\infty) \, \phi^i$ at the boundary node.

The model is linear, so the system is solved once.

## Usage

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
model.setSolverMethod("lusolve");
const { solutionVector, nodesCoordinates } = model.solve();
```

The model takes no coefficient functions.

### Boundary conditions

| Condition                 | Parameters                                                  | Kind                |
| ------------------------- | ----------------------------------------------------------- | ------------------- |
| `["constantTemp", T]`     | Temperature $T_b$                                           | Dirichlet           |
| `["convection", h, Tinf]` | Heat transfer coefficient $h$, fluid temperature $T_\infty$ | Robin               |
| `["symmetry"]`            | –                                                           | Neumann (zero flux) |

`h` and `Tinf` are constants. A boundary without a condition is insulated (zero heat flux), exactly like
`"symmetry"`. Version 0.2.0 does not recognize `"constantTemperature"`: use `"constantTemp"` (see
[Boundary conditions](../fundamentals/boundary-conditions.md#unrecognized-condition-types)).

### Solvers

All solver methods are supported: `"lusolve"` (default), `"jacobi"`, `"frontal"`, and `"jacobi-gpu"` with
`solveAsync()`. See [Solvers](../fundamentals/solvers.md).

## Results

`solutionVector` holds the nodal temperatures, in the order of the nodes in `nodesCoordinates` (see
[Node numbering](../fundamentals/mesh.md#node-numbering)). Plot them with
[`plotSolution`](../api/visualization.md) or post-process them directly:

```javascript
const { nodesXCoordinates, nodesYCoordinates } = nodesCoordinates;
const maxTemperature = Math.max(...solutionVector);
```

## Examples

- Node.js scripts in
  [`examples/heatConductionScript`](https://github.com/FEAScript/FEAScript-core/tree/0.2.0/examples/heatConductionScript)
  of FEAScript-core 0.2.0: a 1D wall, and a 2D fin with a structured mesh and with Gmsh meshes
