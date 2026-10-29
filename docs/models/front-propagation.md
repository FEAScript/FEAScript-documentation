---
sidebar_position: 3
---

# Front propagation

`frontPropagationScript` computes how a front (for example a solidification interface) advances from a part of
the boundary into the domain, by solving the eikonal equation in 1D and 2D. The solution $u(\bar{x})$ is the
arrival time of the front at every point, which for a unit speed equals the distance from the initial front.

The [eikonal equation post](https://blog.feascript.com/tutorial/2025/06/15/eikonal-equation.html) on the
FEAScript blog gives the background of the method.

## Governing equation

The eikonal equation with unit speed is

$$
\lvert \nabla u \rvert = 1 \quad \text{in} \quad D,
\qquad u = 0 \quad \text{on the initial front}.
$$

It is a nonlinear, first-order equation whose solutions can have kinks (points where $\nabla u$ is
discontinuous). FEAScript uses the vanishing viscosity method: it adds a diffusion term that keeps the solution
smooth, and solves

$$
\lambda \left( \lvert \nabla u \rvert - 1 \right) - \nabla \cdot \left( \varepsilon \, \nabla u \right) = 0,
$$

where $\lambda$ is the activation parameter of the eikonal term and $\varepsilon$ the viscous term, computed for
every element as

$$
\varepsilon = 1 - \lambda + \max \left( 10^{-2}, \; 10^{-1} \, h_e \right).
$$

$h_e$ is the size of the element per node spacing: the element length in 1D and the square root of the element
area in 2D, divided by two for quadratic elements. The term proportional to $h_e$ stabilizes coarse meshes and
vanishes under mesh refinement.

## Weak form

After integration by parts of the viscous term, the Galerkin residuals are

$$
R_i = \int_{D} \varepsilon \, \nabla \phi^i \cdot \nabla u \, dS
+ \lambda \int_{D} \phi^i \left( \lvert \nabla u \rvert - 1 \right) dS,
\qquad i = 1, 2, \dots, N,
$$

where the boundary term $\oint \varepsilon \, \phi^i \, \partial u / \partial n \, dt$ vanishes on zero-gradient
boundaries. The Jacobian matrix uses the derivative
$\partial \lvert \nabla u \rvert / \partial \nabla u = \nabla u / \sqrt{\lvert \nabla u \rvert^2 + 10^{-8}}$,
regularized so that it stays finite where $\nabla u = 0$.

## Solution procedure

The eikonal term is activated gradually, in six steps:

$$
\lambda = 0, \; 0.2, \; 0.4, \; 0.6, \; 0.8, \; 1.
$$

- At $\lambda = 0$, the eikonal term is off and the equation is a linear diffusion problem.
- Each step is solved with the Newton–Raphson method, starting from the solution of the previous step (the
  first step starts from $u = 0$).
- At $\lambda = 1$, the remaining viscous term is $\max(10^{-2}, 10^{-1} h_e)$.

If a step does not converge, FEAScript stops at that step and logs an error: the returned solution is not
valid, and a finer mesh may be required. The `maxIterations` and `tolerance` options (see
[Solvers](../fundamentals/solvers.md#newtonraphson-method)) apply to the Newton–Raphson iterations of each step.

## Usage

The solidification front in a $4 \times 2$ domain, starting from the bottom, left and right sides:

```javascript
import { FEAScriptModel } from "feascript";

const model = new FEAScriptModel();

model.setModelConfig("frontPropagationScript");

model.setMeshConfig({
  meshDimension: "2D",
  elementOrder: "quadratic",
  numElementsX: 12,
  numElementsY: 8,
  maxX: 4,
  maxY: 2,
});

model.addBoundaryCondition("0", ["constantValue", 0]); // Bottom: initial front
model.addBoundaryCondition("1", ["constantValue", 0]); // Left: initial front
model.addBoundaryCondition("2", ["zeroGradient"]); // Top
model.addBoundaryCondition("3", ["constantValue", 0]); // Right: initial front

model.setSolverMethod("lusolve");

const { solutionVector, nodesCoordinates } = model.solve();
```

The model takes no coefficient functions: the speed of the front is one everywhere.

### Boundary conditions

| Condition                  | Parameters   | Kind              | Meaning                                         |
| -------------------------- | ------------ | ----------------- | ----------------------------------------------- |
| `["constantValue", value]` | Arrival time | Dirichlet         | The front is on this boundary at time $u = u_b$ |
| `["zeroGradient"]`         | –            | Neumann (natural) | $\partial u / \partial n = 0$                   |

Use `["constantValue", 0]` for the initial front. A non-zero value sets a later start time for that boundary: with
`["constantValue", 1]` on the left end of a 1D domain, for example, the solution is $u = 1 + x$.

### Solvers

`"lusolve"` (default), `"jacobi"` and `"frontal"` are supported; the selected method solves the linear system of
each Newton–Raphson iteration.

## Results

`solutionVector` holds the nodal values of $u$, the arrival time of the front (equal to the distance from the
initial front for a unit speed). The position of the front at time $t$ is the contour line $u = t$, so a contour
plot of the solution shows successive positions of the front.

## Examples

- [Solidification front in 2D](https://feascript.com/tutorials/solidification-front-2d.html)
- [Solidification front in 2D with a web worker](https://feascript.com/tutorials/solidification-front-2d-worker.html)
- Node.js script in
  [`examples/frontPropagationScript`](https://github.com/FEAScript/FEAScript-core/tree/main/examples/frontPropagationScript)
