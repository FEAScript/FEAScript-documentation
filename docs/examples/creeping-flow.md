---
sidebar_position: 5
---

# Creeping flow

Node.js examples of [`creepingFlowScript`](../models/creeping-flow), in
[`examples/creepingFlowScript`](https://github.com/FEAScript/FEAScript-core/tree/main/examples/creepingFlowScript).
Run the commands below from that folder (see [running an example](overview#running-an-example)). All results are
from FEAScript-core 0.4.0 (RC).

## Lid-driven cavity in 2D

Creeping (Stokes) flow in a 4 m × 2 m cavity, $\mu = 1$, driven by its top wall (the lid), which moves at 1 m/s.
The other walls are fixed (no slip). The elements are Taylor-Hood Q2-Q1: quadratic velocity and linear pressure.

```bash
node lidDrivenCavity2DCreepingFlow/lidDrivenCavity2DCreepingFlow.js
```

Source:
[`lidDrivenCavity2DCreepingFlow.js`](https://github.com/FEAScript/FEAScript-core/blob/main/examples/creepingFlowScript/lidDrivenCavity2DCreepingFlow/lidDrivenCavity2DCreepingFlow.js)

### Geometry

![4 m by 2 m cavity with a moving lid and fixed walls](/assets/examples/cavity-geometry.svg)

### Mesh

![12 by 6 Q2-Q1 quadrilaterals with the boundary numbering](/assets/examples/cavity-mesh.svg)

### Results

![Velocity vectors forming a recirculation below the lid](/assets/examples/cavity-results.svg)

The lid drags the fluid along under it, and the fluid returns along the bottom of the cavity, forming one large
recirculation. The flow is mirror-symmetric about $x = 2$ m. The strongest return flow is $u = -0.3245$ m/s, at
(2 m, 0.667 m). At the corners of the lid the velocity is that of the fixed walls, zero (see
[pressure level](../models/creeping-flow#pressure-level)). The example prints the node coordinates and the fields
`u`, `v` and `p`.

## Couette flow in 2D

A 4 m × 2 m channel, $\mu = 1$, whose top wall moves at 1 m/s over a fixed bottom wall, with stress-free (open)
ends. The exact solution is the linear profile $u = y / 2$, $v = 0$, $p = 0$, which the Taylor-Hood elements
reproduce exactly (see the [verification page](../verification/creeping-flow)).

```bash
node couetteFlow2DCreepingFlow/couetteFlow2DCreepingFlow.js
```

Source:
[`couetteFlow2DCreepingFlow.js`](https://github.com/FEAScript/FEAScript-core/blob/main/examples/creepingFlowScript/couetteFlow2DCreepingFlow/couetteFlow2DCreepingFlow.js)

### Geometry

![Channel with a moving top wall, a fixed bottom wall and stress-free ends](/assets/verification/couette-geometry.svg)

### Mesh

![4 by 2 Q2-Q1 quadrilaterals with the boundary numbering](/assets/examples/couette-mesh.svg)

### Results

![Velocity profile at the left end: the computed values lie on the exact line u = y / 2](/assets/examples/couette-results.svg)

The example prints the velocity along the left end next to the exact values, and the largest deviations:

```text
Velocity u along the left end (x = 0):
  y = 0.00: u = 0.0000 (exact 0)
  y = 0.50: u = 0.2500 (exact 0.25)
  y = 1.00: u = 0.5000 (exact 0.5)
  y = 1.50: u = 0.7500 (exact 0.75)
  y = 2.00: u = 1.0000 (exact 1)
Largest deviation from u = U y / H: 3.33e-16
Largest |v|: 0.00e+0 (exact 0)
Largest |p|: 0.00e+0 (exact 0)
```
