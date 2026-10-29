---
sidebar_position: 3
---

# Boundary conditions

Boundary conditions are added with `model.addBoundaryCondition(boundaryKey, condition)`:

```javascript
model.addBoundaryCondition("0", ["constantTemperature", 200]);
```

- `boundaryKey` is a string that identifies the boundary: `"0"`, `"1"`, ... (see
  [Mesh](./mesh.md#boundaries-of-a-structured-mesh) for the keys of structured and Gmsh meshes).
- `condition` is an array whose first entry is the condition type, followed by its parameters.

Each boundary holds one condition: calling `addBoundaryCondition` again with the same key replaces the previous
condition. A boundary without a condition gets the natural (zero Neumann) condition of the model.

:::note
The [Euler–Bernoulli beam](../models/euler-bernoulli-beam.md) model is the exception: its keys are node numbers
and each node takes an array of conditions. See the model page for details.
:::

## Condition types by model

| Model                                                     | Condition                              | Kind              | Meaning                                                     |
| --------------------------------------------------------- | -------------------------------------- | ----------------- | ----------------------------------------------------------- |
| [Heat conduction](../models/heat-conduction.md)           | `["constantTemperature", T]`           | Dirichlet         | $T = T_b$ on the boundary                                   |
|                                                           | `["convection", h, Tinf]`              | Robin             | $-k \, \partial T / \partial n = h (T - T_\infty)$          |
|                                                           | `["symmetry"]`                         | Neumann (natural) | $-k \, \partial T / \partial n = 0$ (insulated or symmetry) |
| [General form PDE](../models/general-form-pde.md)         | `["constantValue", value]`             | Dirichlet         | $u = u_b$ on the boundary                                   |
|                                                           | `["zeroGradient"]`                     | Neumann (natural) | $A \, du/dx = 0$                                            |
| [Front propagation](../models/front-propagation.md)       | `["constantValue", value]`             | Dirichlet         | Arrival time of the front, $u = u_b$ (`0`: initial front)   |
|                                                           | `["zeroGradient"]`                     | Neumann (natural) | $\partial u / \partial n = 0$                               |
| [Creeping flow](../models/creeping-flow.md)               | `["constantVelocity", ux, uy]`         | Dirichlet         | $u = u_b$, $v = v_b$ on the boundary                        |
|                                                           | `["stressFree"]`                       | Neumann (natural) | $\mu \, \partial \bar{u} / \partial n - p \, \bar{n} = 0$   |
| [Euler–Bernoulli beam](../models/euler-bernoulli-beam.md) | `["fixed"]`                            | Essential         | $w = 0$, $\theta = 0$                                       |
|                                                           | `["pinned"]`, `["deflection", w]`      | Essential         | $w = w_b$ (default $0$)                                     |
|                                                           | `["rotationFixed"]`, `["rotation", θ]` | Essential         | $\theta = \theta_b$ (default $0$)                           |
|                                                           | `["force", F]`                         | Natural           | Point force at the node                                     |
|                                                           | `["moment", M]`                        | Natural           | Point moment at the node                                    |
|                                                           | `["spring", k, wRef]`                  | Robin             | Transverse spring of stiffness $k$ (default $w_{ref} = 0$)  |

Here $\bar{n}$ is the outward unit normal and $\partial / \partial n$ the derivative along it.

:::note
Natural conditions such as `"symmetry"`, `"zeroGradient"` and `"stressFree"` add nothing to the discrete
system: they name the condition that a boundary without a Dirichlet or Robin condition already satisfies. They
are still useful to document the setup.
:::

## Checks

When `solve()` runs, FEAScript checks every condition against the condition types of the selected model (the
table above). A type that the model does not recognize, for example a misspelled `"convektion"`, is reported as
an `[ERROR]` in the console with the list of supported types; that boundary then gets the natural condition of
the model.

A condition without parameters may also be given as a plain string, for example `"zeroGradient"` instead of
`["zeroGradient"]`. FEAScript wraps it in an array and logs a warning; use the array form.

## How the conditions are imposed

Following the [Galerkin formulation](./finite-element-method.md#boundary-conditions):

- **Dirichlet conditions** replace the residual of every node on the boundary: the row of the Jacobian matrix is
  cleared, its diagonal entry is set to one, and the residual entry is set to the prescribed value. With the
  frontal solver, the nodes are flagged as constrained before the elimination.
- **Robin conditions** (`"convection"`) add the boundary integral of the condition to the Jacobian matrix and
  the residual vector. In 2D, this integral is computed with Gauss quadrature along each element side on the
  boundary, so curved sides of quadratic elements are taken into account.
- **Natural conditions** need no assembly.

When two boundaries share a node, for example at a corner of a rectangle:

- a Dirichlet condition on either boundary takes precedence over a Robin or natural condition on the other;
- if both boundaries have Dirichlet conditions with different values, the boundary with the larger key sets the
  value at the shared node (the boundaries are processed in increasing key order). In the lid-driven cavity of
  the [creeping flow](../models/creeping-flow.md) model, for example, the top-right corner takes the velocity of
  the right wall (`"3"`) and the top-left corner the velocity of the lid (`"2"`).

## Deprecated names

| Deprecated type  | Replacement             |
| ---------------- | ----------------------- |
| `"constantTemp"` | `"constantTemperature"` |

Deprecated names still work and are converted automatically, with a warning in the console. They will be
removed in a future version.
