---
sidebar_position: 4
---

# Creeping flow

`creepingFlowScript` solves steady, incompressible creeping (Stokes) flow in 2D, for velocity and pressure,
with Taylor–Hood mixed elements.

## Governing equations

$$
\begin{aligned}
-\mu \, \nabla^2 \bar{u} + \nabla p &= 0 && \text{(momentum)}, \\
\nabla \cdot \bar{u} &= 0 && \text{(continuity)},
\end{aligned}
\qquad \text{in} \quad D,
$$

where $\bar{u} = (u, v)$ is the velocity, $p$ the pressure and $\mu$ the dynamic viscosity. Inertia and body
forces are neglected, which is valid when the Reynolds number is much smaller than one.

:::note
In version 0.2.0 the viscosity is fixed to $\mu = 1$. With velocity boundary conditions only, a constant viscosity
does not change the velocity field and the pressure scales linearly with $\mu$, so the pressure of a fluid with
another viscosity is $\mu \, p$. A viscosity option was added in version 0.3.0.
:::

## Taylor–Hood elements

Velocity and pressure are approximated with different basis functions: biquadratic (Q2) for the velocity
components and bilinear (Q1) for the pressure. This pairing satisfies the inf–sup (LBB) stability condition, so no
stabilization is needed.

![Taylor–Hood elements: velocity at every node, pressure at the corner nodes](/assets/taylor-hood-elements.svg)

| Element shape | Velocity                  | Pressure                      |
| ------------- | ------------------------- | ----------------------------- |
| Quadrilateral | Q2 (9 nodes, biquadratic) | Q1 (4 corner nodes, bilinear) |

The mesh must therefore be **2D with quadratic quadrilaterals**: a structured mesh with
`elementOrder: "quadratic"`, or a quadratic Gmsh mesh of quadrilaterals. The triangular (P2–P1) elements in the
figure were added in version 0.3.0.

## Weak form

With $\phi^i$ the quadratic (velocity) and $\psi^k$ the linear (pressure) basis functions, the Galerkin residuals
are

$$
\begin{aligned}
R^u_i &= \int_{D} \left( \mu \, \nabla \phi^i \cdot \nabla u - p \, \frac{\partial \phi^i}{\partial x} \right) dS, \\
R^v_i &= \int_{D} \left( \mu \, \nabla \phi^i \cdot \nabla v - p \, \frac{\partial \phi^i}{\partial y} \right) dS, \\
R^p_k &= \int_{D} \psi^k \left( \frac{\partial u}{\partial x} + \frac{\partial v}{\partial y} \right) dS.
\end{aligned}
$$

Integration by parts leaves the boundary term
$\oint_{\partial D} \phi^i \left( \mu \, \partial \bar{u} / \partial n - p \, \bar{n} \right) dt$, which is zero on
stress-free boundaries. The model is linear, so the system is solved once.

### Pressure level

If every boundary has a velocity condition, the pressure is defined only up to a constant. In that case
FEAScript sets $p = 0$ at the first pressure node (for a structured mesh, the bottom-left corner of the domain).
When at least one boundary is `"stressFree"`, the pressure level is set by that boundary and no node is fixed.

## Usage

The lid-driven cavity: a $4 \times 2$ cavity whose top wall moves with unit velocity.

```javascript
import * as math from "mathjs";
global.math = math;

import { FEAScriptModel } from "feascript";

// 1. Create the model and select the physics
const model = new FEAScriptModel();
model.setModelConfig("creepingFlowScript");

// 2. Define the mesh
model.setMeshConfig({
  meshDimension: "2D",
  elementOrder: "quadratic", // Required (Taylor–Hood elements)
  numElementsX: 12,
  numElementsY: 6,
  maxX: 4,
  maxY: 2,
});

// 3. Apply the boundary conditions
model.addBoundaryCondition("0", ["constantVelocity", 0, 0]); // Bottom wall
model.addBoundaryCondition("1", ["constantVelocity", 0, 0]); // Left wall
model.addBoundaryCondition("2", ["constantVelocity", 1, 0]); // Moving lid
model.addBoundaryCondition("3", ["constantVelocity", 0, 0]); // Right wall

// 4. Solve
model.setSolverMethod("lusolve");
const result = model.solve();
```

The model takes no coefficient functions.

### Boundary conditions

| Condition                      | Parameters                     | Kind              |
| ------------------------------ | ------------------------------ | ----------------- |
| `["constantVelocity", ux, uy]` | Velocity components $u_b, v_b$ | Dirichlet         |
| `["stressFree"]`               | –                              | Neumann (natural) |

Use `["constantVelocity", 0, 0]` for no-slip walls, a non-zero velocity for moving walls and inflows, and
`["stressFree"]` for outflows. A boundary without a condition behaves as `"stressFree"`, but it does not prevent
the pressure from being fixed at the first pressure node: mark open boundaries explicitly with `"stressFree"`.

### Solvers

Only `"lusolve"` is supported. The pressure rows of the system have zero diagonal entries, which the Jacobi method
cannot handle, and the frontal solver is not implemented for this model.

## Results

`result.solutionVector` holds the unknowns of the mixed formulation, in three consecutive blocks:

$$
[\, u_1, \dots, u_{N}, \; v_1, \dots, v_{N}, \; p_1, \dots, p_{N_p} \,],
$$

where $N$ is the number of mesh nodes and $N_p$ the number of pressure (corner) nodes. The velocity components
are in the order of `nodesCoordinates`. After `solve()`, the model stores the sizes of the blocks in
`model._creepingFlowMetadata`:

| Property              | Description                                                     |
| --------------------- | --------------------------------------------------------------- |
| `totalNodesVelocity`  | $N$, the number of velocity nodes (all mesh nodes)              |
| `totalNodesPressure`  | $N_p$, the number of pressure nodes                             |
| `pressureNodeIndices` | For each pressure unknown, the index of its mesh node (0-based) |

Slice the solution vector to get each field, and pass it to [`plotSolution`](../api/visualization.md) with the
coordinates of the mesh nodes:

```javascript
const { solutionVector, nodesCoordinates } = result;
const N = model._creepingFlowMetadata.totalNodesVelocity;

const u = solutionVector.slice(0, N);
const v = solutionVector.slice(N, 2 * N);
const velocityMagnitude = u.map((ui, i) => Math.sqrt(ui ** 2 + v[i] ** 2));

plotSolution(model, { solutionVector: velocityMagnitude, nodesCoordinates }, "contour", "velocityCanvas");
plotSolution(model, { solutionVector: u, nodesCoordinates }, "contour", "uVelocityCanvas");
```

The pressure has values at the corner nodes only: `solutionVector[2 * N + k]` is the pressure at mesh node
`pressureNodeIndices[k]`.

## Examples

- Node.js script in
  [`examples/creepingFlowScript`](https://github.com/FEAScript/FEAScript-core/tree/0.2.0/examples/creepingFlowScript)
  of FEAScript-core 0.2.0
