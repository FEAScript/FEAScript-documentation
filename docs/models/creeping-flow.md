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
The viscosity is fixed to $\mu = 1$ and cannot be changed yet. For a Newtonian fluid with a different viscosity
and velocity boundary conditions only, the velocity field is the same and the pressure scales linearly with
$\mu$.
:::

## Taylor–Hood elements

Velocity and pressure are approximated with different basis functions: quadratic for the velocity components
and linear for the pressure. This pairing satisfies the inf–sup (LBB) stability condition, so no stabilization
is needed.

![Taylor–Hood Q2–Q1 and P2–P1 elements: velocity at every node, pressure at the corner nodes](/assets/taylor-hood-elements.svg)

| Element shape | Velocity                  | Pressure                      |
| ------------- | ------------------------- | ----------------------------- |
| Quadrilateral | Q2 (9 nodes, biquadratic) | Q1 (4 corner nodes, bilinear) |
| Triangle      | P2 (6 nodes, quadratic)   | P1 (3 corner nodes, linear)   |

The mesh must therefore be **2D with quadratic elements**: a structured mesh with `elementOrder: "quadratic"`,
or a quadratic Gmsh mesh with quadrilaterals or triangles.

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
const { solutionVector, nodesCoordinates } = model.solve();
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

`solutionVector` holds all the unknowns of the mixed formulation, in three consecutive blocks:

$$
[\, u_1, \dots, u_{N}, \; v_1, \dots, v_{N}, \; p_1, \dots, p_{N_p} \,],
$$

where $N$ is the number of mesh nodes (the velocity nodes, in the order of `nodesCoordinates`) and $N_p$ the
number of pressure (corner) nodes. Extract the velocity components and magnitude with:

```javascript
const totalNodesVelocity = nodesCoordinates.nodesXCoordinates.length;

const uVelocity = solutionVector.slice(0, totalNodesVelocity);
const vVelocity = solutionVector.slice(totalNodesVelocity, 2 * totalNodesVelocity);
const velocityMagnitude = uVelocity.map((u, i) => Math.hypot(u, vVelocity[i]));
const pressure = solutionVector.slice(2 * totalNodesVelocity);
```

Pass each field separately to the plotting functions, for example
`plotSolution(model, { solutionVector: velocityMagnitude, nodesCoordinates }, "contour", "plotDiv")` (see
[Visualization](../api/visualization.md)).

The pressure nodes are numbered in the order in which corner nodes first appear when the elements are traversed.
After `solve()`, the mesh node of every pressure unknown is available in
`model._creepingFlowMetadata.pressureNodeIndices` (0-based node indices).

:::caution
`_creepingFlowMetadata` is an internal property, not part of the public API, and may change in a future version.
:::

## Examples

- [Lid-driven cavity creeping flow in 2D](https://feascript.com/tutorials/lid-driven-cavity-2d-creeping-flow.html)
- [Lid-driven cavity creeping flow in 2D with a web worker](https://feascript.com/tutorials/lid-driven-cavity-2d-creeping-flow-worker.html)
- Node.js script in
  [`examples/creepingFlowScript`](https://github.com/FEAScript/FEAScript-core/tree/main/examples/creepingFlowScript)
