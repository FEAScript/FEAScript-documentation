---
sidebar_position: 4
---

# Front propagation

Verification of [`frontPropagationScript`](../models/front-propagation) against closed-form solutions. All results
are from FEAScript-core 0.4.0 (RC), solved with `lusolve`.

## Planar front

A front starts at one boundary, with zero gradient on the others. The exact solution of the eikonal equation is
the distance to that boundary: $u = x$ in 1D on $[0, 2]$, and $u = y$ in 2D on a 4 m × 2 m domain.

![Planar front domains in 1D and 2D, with the front starting at the left and bottom boundaries](/assets/verification/planar-front-geometry.svg)

### Boundary layer at the outflow boundary

The model adds a viscous term $\varepsilon \nabla^2 u$ that stabilizes the eikonal equation, with
$\varepsilon = \max(10^{-2}, \, 0.1 \, h)$ for an element of size $h$. At the outflow boundary, opposite the
front, the zero-gradient condition becomes $\varepsilon \, \partial u / \partial n = 0$, while the exact solution
has $\partial u / \partial n = 1$. The solution bends to meet the condition in a boundary layer about
$\varepsilon$ wide. In 1D,

$$
u \approx x - \varepsilon \, e^{(x - L)/\varepsilon},
$$

so in 1D the largest deviation, at the outflow boundary node, equals $\varepsilon$. Because of the $10^{-2}$ floor
on $\varepsilon$, it does not drop below $10^{-2}$ under mesh refinement. Away from the outflow boundary the layer
has decayed and the solution matches the exact one closely.

### Results

![2D meshes of the planar front test: structured 12 × 8 and 80 × 40, and four Gmsh meshes](/assets/verification/planar-front-meshes.svg)

The largest deviation over all nodes is in the boundary layer. The table gives $\varepsilon$ of the elements along
the outflow boundary, which varies from element to element on the Gmsh meshes:

| Dimension | Elements                 | Mesh                              | $\varepsilon$ at the outflow boundary | Largest deviation | Tolerance |
| --------- | ------------------------ | --------------------------------- | ------------------------------------- | ----------------- | --------- |
| 1D        | Linear                   | 20 elements                       | 1.0e-2                                | 1.0e-2            | `5e-2`    |
| 1D        | Quadratic                | 20 elements                       | 1.0e-2                                | 1.0e-2            | `5e-2`    |
| 2D        | Linear quadrilaterals    | 12 × 8 structured                 | 2.9e-2                                | 2.8e-2            | `5e-2`    |
| 2D        | Linear quadrilaterals    | Gmsh, `rect_quad_linear.msh`      | 5.4e-2 to 6.4e-2                      | 7.1e-2            | `1.5e-1`  |
| 2D        | Quadratic quadrilaterals | Gmsh, `rect_quad_quadratic.msh`   | 2.5e-2 to 3.0e-2                      | 2.7e-2            | `5e-2`    |
| 2D        | Linear triangles         | Gmsh, `rect_triang_linear.msh`    | 3.6e-2 to 4.4e-2                      | 4.4e-2            | `5e-2`    |
| 2D        | Quadratic triangles      | Gmsh, `rect_triang_quadratic.msh` | 1.8e-2 to 2.2e-2                      | 2.3e-2            | `5e-2`    |

In 1D the largest deviation equals $\varepsilon$. In 2D it is close to $\varepsilon$ along the outflow boundary.
On the coarse Gmsh linear quadrilaterals it is about 10 % larger: the elements, about 0.6 wide, are too coarse to
resolve a layer about 0.06 wide.

The interior, more than 0.5 (50 $\varepsilon$) from the outflow boundary, is checked on meshes that resolve the
layer:

| Dimension | Elements              | Mesh               | Region      | Largest deviation | Tolerance |
| --------- | --------------------- | ------------------ | ----------- | ----------------- | --------- |
| 1D        | Linear                | 80 elements        | $x \le 1.5$ | 2.4e-10           | `1e-8`    |
| 1D        | Quadratic             | 40 elements        | $x \le 1.5$ | 2.4e-10           | `1e-8`    |
| 2D        | Linear quadrilaterals | 80 × 40 structured | $y \le 1.5$ | 2.1e-6            | `1e-5`    |

On coarser meshes the layer is not resolved and reaches further into the domain: in 1D the interior deviation
is 8.8e-4 with 20 linear elements, 9.0e-7 with 40 and 2.4e-10 with 80.

In 1D the test also starts the front at $u(0) = 1$, where the exact solution is $u = 1 + x$; the largest
deviation is again 1.0e-2. In every case the frontal solver matches `lusolve` to within 6.7e-16 (tolerance
`1e-8`).

Tests:
[`frontPropagation1DPlanarFront`](https://github.com/FEAScript/FEAScript-core/tree/main/tests/verification/analytical/frontPropagation1DPlanarFront)
and
[`frontPropagation2DPlanarFront`](https://github.com/FEAScript/FEAScript-core/tree/main/tests/verification/analytical/frontPropagation2DPlanarFront).
