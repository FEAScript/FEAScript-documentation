---
sidebar_position: 3
---

# Creeping flow

Verification of [`creepingFlowScript`](../models/creeping-flow) against closed-form solutions. All results are from
FEAScript-core 0.4.0 (RC), solved with `lusolve`.

## Couette flow

A 4 m × 2 m channel, $\mu = 1$: the bottom wall is fixed, the top wall moves with velocity 1, and both ends are
stress-free.

![Couette flow channel with a moving top wall, a fixed bottom wall and stress-free ends](/assets/verification/couette-geometry.svg)

The exact solution is

$$
u = \frac{y}{2}, \qquad v = 0, \qquad p = 0.
$$

The linear velocity profile lies in the Taylor-Hood element spaces, so the elements reproduce it exactly, and the
remaining deviations are round-off. The table gives the largest deviation from the exact solution over all nodes.

![Meshes of the Couette flow test: structured Q2-Q1, Gmsh Q2-Q1 and Gmsh P2-P1](/assets/verification/couette-meshes.svg)

| Elements        | Mesh                        | $\max \lvert u - y/2 \rvert$ | $\max \lvert v \rvert$ | $\max \lvert p \rvert$ |
| --------------- | --------------------------- | ---------------------------- | ---------------------- | ---------------------- |
| Q2-Q1 quads     | 4 × 2 structured            | 3.3e-16                      | 0                      | 0                      |
| Q2-Q1 quads     | Gmsh, 9-node quadrilaterals | 1.1e-15                      | 2.1e-15                | 1.9e-14                |
| P2-P1 triangles | Gmsh, 6-node triangles      | 1.7e-15                      | 1.0e-15                | 1.5e-14                |

The test requires every nodal value to match within `1e-10`:
[`creepingFlow2DCouette`](https://github.com/FEAScript/FEAScript-core/tree/main/tests/verification/analytical/creepingFlow2DCouette).
