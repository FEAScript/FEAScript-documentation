---
sidebar_position: 5
---

# Euler–Bernoulli beam

`eulerBernoulliBeamScript` solves the bending of a straight beam under transverse loads, with Euler–Bernoulli
beam theory, on a 1D mesh. It supports variable bending stiffness, an elastic foundation, distributed loads, and
supports, springs, point forces and point moments at any node.

## Governing equation

$$
\frac{d^2}{dx^2} \left( EI(x) \, \frac{d^2 w}{dx^2} \right) + c_0(x) \, w = q(x),
\qquad 0 \le x \le maxX,
$$

where $w$ is the transverse deflection, $EI$ the bending stiffness (Young's modulus times the second moment of
area), $c_0$ the modulus of an elastic (Winkler) foundation and $q$ the distributed transverse load. The rotation
of the cross-section is $\theta = dw/dx$.

$w$, $q$ and point forces are positive in the same direction, and point moments are positive in the direction
of positive $\theta$.

## Cubic Hermite elements

The equation is of fourth order, so both $w$ and $\theta$ must be continuous between elements ($C^1$ continuity).
FEAScript uses cubic Hermite basis functions $\psi$: every node carries **two unknowns**, the deflection $w$ and
the rotation $\theta$, and the deflection inside an element of length $l_e$ is

$$
w(\xi) = \psi_1(\xi) \, w_1 + \psi_2(\xi) \, \theta_1 + \psi_3(\xi) \, w_2 + \psi_4(\xi) \, \theta_2,
\qquad 0 \le \xi \le 1,
$$

where the rotation basis functions $\psi_2, \psi_4$ include the element length $l_e$.

The geometry of each element only needs its two end nodes, so the mesh must use `elementOrder: "linear"`. The
cubic Hermite interpolation of the deflection is applied internally, independently of this setting.

## Weak form

After integrating the bending term by parts twice, the Galerkin residuals are

$$
R_i = \int_{0}^{maxX} \left( EI \, \frac{d^2 \psi^i}{dx^2} \frac{d^2 w}{dx^2} + c_0 \, \psi^i w - q \, \psi^i \right) dx
- \sum_{\text{nodes}} \left( F \, \psi^i + M \, \frac{d\psi^i}{dx} \right),
$$

where $F$ and $M$ are the point forces and moments applied at the nodes. Springs add $k \, (w - w_{ref})$ to the
residual of the deflection at their node. The model is linear, so the system is solved once.

## Usage

A 10 m beam, clamped at the left end, supported by a roller at midspan and by a spring at the right end. It
carries a uniform load over the first span, a moment at the roller and a point force at the right end (example
from J. N. Reddy, _An Introduction to the Finite Element Method_, 3rd ed., McGraw-Hill, 2006):

![Beam with a clamped end, a roller with an applied moment, and a spring with an applied force](/assets/beam-conditions.svg)

```javascript
import { FEAScriptModel } from "feascript";

// 1. Create the model and select the physics
const model = new FEAScriptModel();
model.setModelConfig("eulerBernoulliBeamScript", {
  coefficientFunctions: {
    EI: (x) => 2.0e6, // Bending stiffness
    q: (x) => (x <= 5 ? -1000 : 0), // Distributed load over the first span
  },
});

// 2. Define the mesh
model.setMeshConfig({
  meshDimension: "1D",
  elementOrder: "linear", // Required
  numElementsX: 2, // Nodes "1", "2", "3" at x = 0, 5, 10
  maxX: 10,
});

// 3. Apply the boundary conditions
model.addBoundaryCondition("1", [["fixed"]]); // Clamped end
model.addBoundaryCondition("2", [["pinned"], ["moment", 1250]]); // Roller with an applied moment
model.addBoundaryCondition("3", [
  ["spring", 200],
  ["force", -2500],
]); // Spring support with an applied force

// 4. Solve
model.setSolverMethod("lusolve");
const { solutionVector, nodesCoordinates } = model.solve();
```

### Coefficient functions

| Property | Symbol   | Default    | Required |
| -------- | -------- | ---------- | -------- |
| `EI`     | $EI(x)$  | –          | Yes      |
| `c0`     | $c_0(x)$ | `(x) => 0` | No       |
| `q`      | $q(x)$   | `(x) => 0` | No       |

All coefficients must be **functions** of $x$, even when they are constant (write `EI: (x) => 2.0e6`). They are
evaluated at the integration points of every element.

### Boundary conditions

Unlike the other models, the beam model keys its conditions by **node number**, so supports and loads can be
placed at interior nodes as well as at the ends:

- The key is the 1-based node number as a string. With $n_e$ = `numElementsX` elements, node $j$ is at
  $x = (j - 1) \cdot maxX / n_e$, from `"1"` at $x = 0$ to `"n_e + 1"` at $x = maxX$.
- The condition is an **array of conditions**, since a node can carry more than one (for example a support and
  a load): `[["pinned"], ["moment", 1250]]`. Always wrap the conditions in an outer array, even a single one:
  `[["fixed"]]`.

| Condition             | Kind      | Effect                                                                                  |
| --------------------- | --------- | --------------------------------------------------------------------------------------- |
| `["fixed"]`           | Essential | $w = 0$ and $\theta = 0$ (clamped support)                                              |
| `["pinned"]`          | Essential | $w = 0$ (pin or roller support)                                                         |
| `["deflection", w]`   | Essential | $w = w_b$ (prescribed deflection; default $0$)                                          |
| `["rotationFixed"]`   | Essential | $\theta = 0$                                                                            |
| `["rotation", θ]`     | Essential | $\theta = \theta_b$ (prescribed rotation; default $0$)                                  |
| `["force", F]`        | Natural   | Point force $F$ at the node                                                             |
| `["moment", M]`       | Natural   | Point moment $M$ at the node                                                            |
| `["spring", k, wRef]` | Robin     | Transverse spring of stiffness $k$, force $-k \, (w - w_{ref})$; `wRef` defaults to $0$ |

A node without conditions is free (zero shear force and bending moment at the ends of the beam). If a node has
both an essential condition and a load or spring on the same unknown, the essential condition takes precedence.
An unknown condition type, or a condition that is not wrapped in the outer array (for example `["fixed"]`
instead of `[["fixed"]]`), is reported as an error.

### Solvers

Use `"lusolve"`. The frontal solver is not supported for this model. `"jacobi"` can be selected, but beam
stiffness matrices are generally not diagonally dominant, so it may not converge.

## Results

`solutionVector` holds two unknowns per node, ordered node by node:

$$
[\, w_1, \theta_1, \; w_2, \theta_2, \; \dots, \; w_N, \theta_N \,],
$$

so it is twice as long as `nodesCoordinates.nodesXCoordinates`. Extract the deflection and rotation with:

```javascript
const deflection = solutionVector.filter((_, index) => index % 2 === 0);
const rotation = solutionVector.filter((_, index) => index % 2 === 1);
```

Pass `deflection` (not the full `solutionVector`) to the plotting functions, for example
`plotSolution(model, { solutionVector: deflection, nodesCoordinates }, "line", "plotDiv")`.

## Examples

- [Cantilever beam in 1D](https://feascript.com/tutorials/cantilever-beam-1d.html)
- Node.js script in
  [`examples/eulerBernoulliBeamScript`](https://github.com/FEAScript/FEAScript-core/tree/main/examples/eulerBernoulliBeamScript)
