---
sidebar_position: 2
---

# General form PDE

`generalFormPDEScript` solves a general second-order, one-dimensional PDE, defined by four coefficient functions.
It covers diffusion, advection–diffusion and reaction–diffusion problems, in linear or nonlinear form.

:::caution
The general form PDE model currently supports **1D meshes only**.
:::

## Governing equation

### Linear form

$$
\frac{d}{dx}\left( A(x) \, \frac{du}{dx} \right) + B(x) \, \frac{du}{dx} + C(x) \, u = D(x),
\qquad 0 \le x \le maxX,
$$

where $A$ is the diffusion coefficient, $B$ the advection coefficient, $C$ the reaction coefficient and $D$ the
source term.

### Nonlinear form

With `nonlinear: true`, the source term may depend on the solution:

$$
\frac{d}{dx}\left( A(x) \, \frac{du}{dx} \right) + B(x) \, \frac{du}{dx} + C(x) \, u = D(x, u),
$$

and the system is solved with the Newton–Raphson method. The derivative $\partial D / \partial u$ must be given
as well, since it enters the Jacobian matrix.

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
residuals of the nodes with a constant value are replaced by the Dirichlet condition. In the nonlinear form the
Jacobian matrix is

$$
\mathcal{J}_{ij} = -\frac{\partial R_i}{\partial u_j}
= -\int_{D} \left( A \, \frac{d\phi^i}{dx} \frac{d\phi^j}{dx}
- B \, \phi^i \frac{d\phi^j}{dx}
- C \, \phi^i \phi^j
+ \frac{\partial D}{\partial u} \, \phi^i \phi^j \right) dx.
$$

## Usage

### Linear: advection–diffusion

The equation $\frac{d^2u}{dx^2} - 10 \frac{du}{dx} = 10 \, e^{-200 (x - 0.5)^2}$ on $0 \le x \le 1$:

```javascript
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

### Nonlinear: reaction–diffusion

The equation $\frac{d^2u}{dx^2} - Da \, u^2 = 0$ on $0 \le x \le 10$, written as
$\frac{d^2u}{dx^2} = D(x, u)$ with $D = Da \, u^2$:

```javascript
const Da = 1;

model.setModelConfig("generalFormPDEScript", {
  nonlinear: true, // Solve with the Newton-Raphson method
  coefficientFunctions: {
    A: (x) => 1,
    B: (x) => 0,
    C: (x) => 0,
    D: (x, u) => Da * u ** 2, // Nonlinear source term
    dDdu: (x, u) => 2 * Da * u, // ∂D/∂u, required for the Jacobian matrix
  },
});

model.setMeshConfig({ meshDimension: "1D", elementOrder: "linear", numElementsX: 20, maxX: 10.0 });

model.addBoundaryCondition("0", ["constantValue", 1]);
model.addBoundaryCondition("1", ["zeroGradient"]);

model.setSolverMethod("lusolve");

const { solutionVector, nodesCoordinates } = model.solve({ maxIterations: 100, tolerance: 1e-5 });
```

### Model options

| Option                 | Type      | Default | Description                                                                   |
| ---------------------- | --------- | ------- | ----------------------------------------------------------------------------- |
| `coefficientFunctions` | `object`  | –       | The coefficient functions below (required)                                    |
| `nonlinear`            | `boolean` | `false` | Solve the nonlinear form with the Newton–Raphson method                       |
| `maxIterations`        | `number`  | `100`   | Maximum Newton–Raphson iterations (nonlinear form)                            |
| `tolerance`            | `number`  | `1e-4`  | Newton–Raphson tolerance on $\lVert \Delta \bar{u} \rVert_2$ (nonlinear form) |

`maxIterations` and `tolerance` can also be passed to `solve()`, which takes precedence. In the linear form,
they apply to the `"jacobi"` solver instead.

### Coefficient functions

| Property | Symbol                    | Signature                             | Required       |
| -------- | ------------------------- | ------------------------------------- | -------------- |
| `A`      | $A(x)$                    | `(x) => number`                       | Yes            |
| `B`      | $B(x)$                    | `(x) => number`                       | Yes            |
| `C`      | $C(x)$                    | `(x) => number`                       | Yes            |
| `D`      | $D(x)$ or $D(x, u)$       | `(x) => number` or `(x, u) => number` | Yes            |
| `dDdu`   | $\partial D / \partial u$ | `(x, u) => number`                    | Nonlinear form |

All coefficients must be **functions**, even when they are constant (write `A: (x) => 1`, not `A: 1`). They are
evaluated at every integration point; in the nonlinear form, `u` is the value of the current Newton–Raphson
iterate at that point.

### Boundary conditions

| Condition                  | Parameters | Kind              |
| -------------------------- | ---------- | ----------------- |
| `["constantValue", value]` | $u_b$      | Dirichlet         |
| `["zeroGradient"]`         | –          | Neumann (natural) |

The boundary keys are `"0"` (left end, $x = 0$) and `"1"` (right end, $x = maxX$). A boundary without a
condition behaves as `"zeroGradient"`.

### Solvers

| Form      | Supported methods                               |
| --------- | ----------------------------------------------- |
| Linear    | `"lusolve"`, `"jacobi"`, `"frontal"`            |
| Nonlinear | `"lusolve"`, `"jacobi"` (inside Newton–Raphson) |

The frontal solver is not supported for the nonlinear form.

## Results

`solutionVector` holds the nodal values of $u$, in the order of `nodesCoordinates.nodesXCoordinates` (left to
right).

## Examples

- [Advection–diffusion in 1D](https://feascript.com/tutorials/advection-diffusion-1d.html)
- Node.js scripts in
  [`examples/generalFormPDEScript`](https://github.com/FEAScript/FEAScript-core/tree/0.3.1/examples/generalFormPDEScript)
  (advection–diffusion and nonlinear reaction–diffusion)
