---
sidebar_position: 3
---

# Boundary conditions

<img className="topic-logo" src="/assets/topics/boundary-conditions.svg" alt="" />

Boundary conditions are added with `model.addBoundaryCondition(boundaryKey, condition)`:

```javascript
model.addBoundaryCondition("bottom", { type: "constantTemperature", temperature: 200 });
```

- `boundaryKey` is the name of the boundary: `"left"` and `"right"` for a line, `"bottom"`, `"right"`, `"top"`
  and `"left"` for a rectangle, the names given to the edges of a polygon, or the names of the physical groups
  of a Gmsh mesh (see [Boundary names](./mesh.md#boundary-names)).
- `condition` is an object with the condition `type` and its parameters, named as in the table below.

Each boundary holds one condition: calling `addBoundaryCondition` again with the same key replaces the previous
condition. A boundary without a condition gets the natural (zero Neumann) condition of the model.

:::note
The [Euler–Bernoulli beam](../models/euler-bernoulli-beam.md) model is the exception: its keys are node numbers,
and each node takes one condition object or a list of them. See the model page for details.
:::

## Condition types by model

| Model                                                     | Condition                                                     | Kind              | Meaning                                                                               |
| --------------------------------------------------------- | ------------------------------------------------------------- | ----------------- | ------------------------------------------------------------------------------------- |
| [Heat conduction](../models/heat-conduction.md)           | `{ type: "constantTemperature", temperature }`                | Dirichlet         | $T = T_b$ on the boundary, with $T_b$ = `temperature`                                 |
|                                                           | `{ type: "convection", h, ambientTemperature }`               | Robin             | $-k \, \partial T / \partial n = h (T - T_\infty)$, $T_\infty$ = `ambientTemperature` |
|                                                           | `{ type: "symmetry" }`                                        | Neumann (natural) | $-k \, \partial T / \partial n = 0$ (insulated or symmetry)                           |
| [General-form PDE](../models/general-form-pde.md)         | `{ type: "constantValue", value }`                            | Dirichlet         | $u = u_b$ on the boundary                                                             |
|                                                           | `{ type: "zeroGradient" }`                                    | Neumann (natural) | $A \, du/dx = 0$                                                                      |
| [Front propagation](../models/front-propagation.md)       | `{ type: "constantValue", value }`                            | Dirichlet         | Arrival time of the front, $u = u_b$ (`0`: initial front)                             |
|                                                           | `{ type: "zeroGradient" }`                                    | Neumann (natural) | $\partial u / \partial n = 0$                                                         |
| [Creeping flow](../models/creeping-flow.md)               | `{ type: "constantVelocity", u, v }`                          | Dirichlet         | $u = u_b$, $v = v_b$ on the boundary                                                  |
|                                                           | `{ type: "stressFree" }`                                      | Neumann (natural) | $\mu \, \partial \bar{u} / \partial n - p \, \bar{n} = 0$                             |
| [Euler–Bernoulli beam](../models/euler-bernoulli-beam.md) | `{ type: "fixed" }`                                           | Essential         | $w = 0$, $\theta = 0$                                                                 |
|                                                           | `{ type: "pinned" }`, `{ type: "deflection", deflection }`    | Essential         | $w = w_b$ (`deflection`, default $0$)                                                 |
|                                                           | `{ type: "rotationFixed" }`, `{ type: "rotation", rotation }` | Essential         | $\theta = \theta_b$ (`rotation`, default $0$)                                         |
|                                                           | `{ type: "force", force }`                                    | Natural           | Point force at the node                                                               |
|                                                           | `{ type: "moment", moment }`                                  | Natural           | Point moment at the node                                                              |
|                                                           | `{ type: "spring", stiffness, referenceDeflection }`          | Robin             | Transverse spring of stiffness $k$ about $w_{ref}$ (default $0$)                      |

Here $\bar{n}$ is the outward unit normal and $\partial / \partial n$ the derivative along it. All parameters
are numbers; `deflection`, `rotation` and `referenceDeflection` may be left out.

:::note
Natural conditions such as `"symmetry"`, `"zeroGradient"` and `"stressFree"` add nothing to the discrete
system: they name the condition that a boundary without a Dirichlet or Robin condition already satisfies. They
are still useful to document the setup.
:::

## Checks

A condition object is checked when it is added: a missing or unknown `type`, a missing parameter, or a parameter
that the type does not have (for example a misspelled `ambientTemprature`) throws a `FEAScriptError` with the
code `INVALID_INPUT`, listing every problem of the condition.

When `solve()` runs, FEAScript checks every condition against the condition types of the selected model (the
table above) and checks that every parameter is a finite number and every boundary exists in the mesh. All the
problems found are reported at once, in one `FEAScriptError` with the code `INVALID_INPUT`, before anything is
computed.

## How the conditions are imposed

Following the [Galerkin formulation](./finite-element-method.md#boundary-conditions):

- **Dirichlet conditions** replace the residual of every node on the boundary: the row of the Jacobian matrix is
  cleared, its diagonal entry is set to one, and the residual entry is set to the prescribed value. The column of
  the node is eliminated as well, by moving the known value to the residual of the other rows, so a symmetric
  matrix stays symmetric. With the frontal solver, the nodes are flagged as constrained before the elimination.
- **Robin conditions** (`"convection"`) add the boundary integral of the condition to the Jacobian matrix and
  the residual vector. In 2D, this integral is computed with Gauss quadrature along each element side on the
  boundary, so curved sides of quadratic elements are taken into account.
- **Natural conditions** need no assembly.

When two boundaries share a node, for example at a corner of a rectangle:

- a Dirichlet condition on either boundary takes precedence over a Robin or natural condition on the other;
- if both boundaries have Dirichlet conditions with different values, the condition added last sets the value
  at the shared node (the conditions are applied in the order of the `addBoundaryCondition` calls);
- in the [creeping flow](../models/creeping-flow.md) model, a zero velocity (no slip) takes precedence over a
  nonzero velocity, whatever the order. In the lid-driven cavity, both top corners therefore take the velocity
  of the side walls, zero, so that the moving lid does not push fluid through the side walls at the corners.

## Deprecated forms

FEAScript 0.3 gave a condition as an array, with the type first and the parameters in a fixed order:

| Deprecated form                        | Replacement                                            |
| -------------------------------------- | ------------------------------------------------------ |
| `["convection", 1, 20]`                | `{ type: "convection", h: 1, ambientTemperature: 20 }` |
| `"zeroGradient"` (a plain string)      | `{ type: "zeroGradient" }`                             |
| `[["fixed"], ["force", -1000]]` (beam) | `[{ type: "fixed" }, { type: "force", force: -1000 }]` |

The array form and plain strings still work, with a warning in the console that gives the object form of the
condition. They will be removed in a future version, in 0.7.0 at the earliest.

The type `"constantTemp"`, renamed `"constantTemperature"` in 0.3.0, was removed in 0.4.0: it now throws an
`INVALID_INPUT` error that names its replacement.
