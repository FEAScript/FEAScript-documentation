---
sidebar_position: 2
---

# General form PDE

`generalFormPDEScript` solves a general linear, second-order, one-dimensional PDE, defined by four coefficient
functions. It covers diffusion, advection–diffusion and reaction–diffusion problems.

:::caution
The general form PDE model of version 0.2.0 supports **1D meshes** and the **linear** form only. The nonlinear form
(solved with the Newton–Raphson method) was added in version 0.3.0.
:::

## Governing equation

$$
\frac{d}{dx}\left( A(x) \, \frac{du}{dx} \right) + B(x) \, \frac{du}{dx} + C(x) \, u = D(x),
\qquad 0 \le x \le maxX,
$$

where $A$ is the diffusion coefficient, $B$ the advection coefficient, $C$ the reaction coefficient and $D$ the
source term.

### Boundary conditions

$$
\begin{aligned}
u &= u_b && \text{constant value}, \\
A \, \frac{du}{dx} &= 0 && \text{zero gradient}.
\end{aligned}
$$

## Weak form

After integration by parts of the diffusion term, the Galerkin residuals are

$$
R_i = \int_{D} \left( A \, \frac{d\phi^i}{dx} \frac{du}{dx}
- B \, \phi^i \frac{du}{dx}
- C \, \phi^i u
+ D \, \phi^i \right) dx,
\qquad i = 1, 2, \dots, N.
$$

The boundary term $\left[ A \, \frac{du}{dx} \, \phi^i \right]$ vanishes on zero-gradient boundaries, and the
residuals of the nodes with a constant value are replaced by the Dirichlet condition.

## Usage

The equation $\frac{d^2u}{dx^2} - 10 \frac{du}{dx} = 10 \, e^{-200 (x - 0.5)^2}$ on $0 \le x \le 1$:

```javascript
import * as math from "mathjs";
global.math = math;

import { FEAScriptModel } from "feascript";

// 1. Create the model and select the physics
const model = new FEAScriptModel();
model.setModelConfig("generalFormPDEScript", {
  coefficientFunctions: {
    A: (x) => 1, // Diffusion coefficient
    B: (x) => -10, // Advection coefficient
    C: (x) => 0, // Reaction coefficient
    D: (x) => 10 * Math.exp(-200 * Math.pow(x - 0.5, 2)), // Source term
  },
});

// 2. Define the mesh
model.setMeshConfig({
  meshDimension: "1D",
  elementOrder: "quadratic",
  numElementsX: 20,
  maxX: 1.0,
});

// 3. Apply the boundary conditions
model.addBoundaryCondition("0", ["constantValue", 1]); // Left, x = 0
model.addBoundaryCondition("1", ["zeroGradient"]); // Right, x = 1

// 4. Solve
model.setSolverMethod("lusolve");
const { solutionVector, nodesCoordinates } = model.solve();
```

### Coefficient functions

| Property | Symbol | Signature       | Required |
| -------- | ------ | --------------- | -------- |
| `A`      | $A(x)$ | `(x) => number` | Yes      |
| `B`      | $B(x)$ | `(x) => number` | Yes      |
| `C`      | $C(x)$ | `(x) => number` | Yes      |
| `D`      | $D(x)$ | `(x) => number` | Yes      |

All coefficients must be **functions**, even when they are constant (write `A: (x) => 1`, not `A: 1`). They are
evaluated at every integration point.

The `maxIterations` and `tolerance` options of `setModelConfig` and `solve()` apply to the `"jacobi"` solver.

### Boundary conditions

| Condition                  | Parameters | Kind              |
| -------------------------- | ---------- | ----------------- |
| `["constantValue", value]` | $u_b$      | Dirichlet         |
| `["zeroGradient"]`         | –          | Neumann (natural) |

The boundary keys are `"0"` (left end, $x = 0$) and `"1"` (right end, $x = maxX$). A boundary without a
condition behaves as `"zeroGradient"`.

### Solvers

`"lusolve"` (default) and `"jacobi"` are supported. The frontal solver is not supported for this model in version
0.2.0: it logs an error and returns an empty solution vector.

## Results

`solutionVector` holds the nodal values of $u$, in the order of `nodesCoordinates.nodesXCoordinates` (left to
right).

## Examples

- Node.js script in
  [`examples/generalFormPDEScript`](https://github.com/FEAScript/FEAScript-core/tree/0.2.0/examples/generalFormPDEScript)
  of FEAScript-core 0.2.0 (advection–diffusion)
