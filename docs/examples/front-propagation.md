---
sidebar_position: 4
---

# Front propagation

Node.js example of [`frontPropagationScript`](../models/front-propagation), in
[`examples/frontPropagationScript`](https://github.com/FEAScript/FEAScript-core/tree/main/examples/frontPropagationScript).
Run the command below from that folder (see [running an example](overview#running-an-example)). The results are
from FEAScript-core 0.4.0 (RC).

## Solidification front in 2D

A solidification front that starts on the bottom, left and right edges of a 4 m × 2 m domain and moves inward
at unit speed. The solution $u$ of the eikonal equation $|\nabla u| = 1$ is the time at which the front reaches
each point, which at unit speed is the distance to the nearest of those edges. The top edge has a zero gradient.

```bash
node solidificationFront2D/solidificationFront2D.js
```

Source:
[`solidificationFront2D.js`](https://github.com/FEAScript/FEAScript-core/blob/main/examples/frontPropagationScript/solidificationFront2D/solidificationFront2D.js)

### Geometry

![4 m by 2 m domain with the initial front on the bottom, left and right edges and zero gradient on the top edge](/assets/examples/solidification-geometry.svg)

### Mesh

![12 by 8 quadratic quadrilaterals with the boundary numbering](/assets/examples/solidification-mesh.svg)

### Results

![Contours of the arrival time, nested inside the bottom, left and right edges](/assets/examples/solidification-results.svg)

The contours follow the distance to the nearest initial front edge. The last point reached is the middle of the
top edge, (2 m, 2 m), at $u = 1.9812$, against an exact distance of 2: the viscous term that stabilizes the
eikonal equation smooths the solution slightly (see the [verification page](../verification/front-propagation)).
The example prints the node coordinates and the solution vector.
