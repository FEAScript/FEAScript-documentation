---
sidebar_position: 6
---

# Euler–Bernoulli beam

Node.js examples of [`eulerBernoulliBeamScript`](../models/euler-bernoulli-beam), in
[`examples/eulerBernoulliBeamScript`](https://github.com/FEAScript/FEAScript-core/tree/main/examples/eulerBernoulliBeamScript).
Run the commands below from that folder (see [running an example](overview#running-an-example)). All results are
from FEAScript-core 0.4.0 (RC).

The beam elements are cubic Hermite elements, with the deflection $w$ and the rotation $\theta$ at each node. The
deflection curves below are drawn with the Hermite shape functions between the nodes; the markers are the nodes.

## Clamped and spring-supported beam

The "Bending of a Beam" example of J. N. Reddy, _An Introduction to the Finite Element Method_, 3rd ed., 2006: a
10 m beam, $EI = 2 \times 10^6$ N·m², clamped at $x = 0$, on a roller at midspan with an applied moment of
1250 N·m, and on a spring ($k = 200$ N/m) at the free end with a point load of −2500 N. A uniform load of
−1000 N/m acts on the clamped span.

```bash
node clampedSpringSupportedBeam1D/clampedSpringSupportedBeam1D.js
```

Source:
[`clampedSpringSupportedBeam1D.js`](https://github.com/FEAScript/FEAScript-core/blob/main/examples/eulerBernoulliBeamScript/clampedSpringSupportedBeam1D/clampedSpringSupportedBeam1D.js)

### Geometry and mesh

![Beam with a clamped end, a roller with an applied moment, and a spring with an applied force](/assets/beam-conditions.svg)

The mesh has 2 elements, with nodes 1, 2 and 3 at the clamp, the roller and the spring.

### Results

![Deflection of the beam: close to zero over the clamped span and falling to −0.0801 m at the spring](/assets/examples/clamped-spring-beam-results.svg)

The example prints the deflection and rotation at each node:

```text
Node |    x (m) | Deflection w (m) | Rotation theta (rad)
-----|----------|-------------------|----------------------
  1  |     0.00 |         0.0000e+0 |           4.5475e-18
  2  |     5.00 |        9.4739e-18 |           -5.6791e-3
  3  |    10.00 |        -8.0145e-2 |           -2.1204e-2
```

The deflection and rotation at the clamp, and the deflection at the roller, are zero to round-off.

## Cantilever beam

A 4 m cantilever, $EI = 10^5$ N·m², clamped at $x = 0$, with a point load $P = -1000$ N at the free end. The
exact tip deflection and rotation are $w(L) = P L^3 / (3 EI)$ and $\theta(L) = P L^2 / (2 EI)$, which the cubic
Hermite elements reproduce exactly.

```bash
node cantileverBeam1D/cantileverBeam1D.js
```

Source:
[`cantileverBeam1D.js`](https://github.com/FEAScript/FEAScript-core/blob/main/examples/eulerBernoulliBeamScript/cantileverBeam1D/cantileverBeam1D.js)

### Geometry and mesh

![Cantilever of length 4 m on 4 elements, clamped at node 1, with a tip load at node 5](/assets/examples/cantilever-geometry.svg)

The mesh has 4 elements, with nodes 1 to 5; the load is applied at node 5.

### Results

![Deflection of the cantilever, from zero at the clamp to −0.2133 m at the tip](/assets/examples/cantilever-results.svg)

The example prints the tip deflection and rotation next to the exact values:

```text
Tip deflection w(L): -2.133333e-1 m (exact -2.133333e-1 m)
Tip rotation θ(L): -8.000000e-2 rad (exact -8.000000e-2 rad)
```
