---
sidebar_position: 3
---

# General form PDE

Node.js examples of [`generalFormPDEScript`](../models/general-form-pde), in
[`examples/generalFormPDEScript`](https://github.com/FEAScript/FEAScript-core/tree/main/examples/generalFormPDEScript).
Run the commands below from that folder (see [running an example](overview#running-an-example)). All results are
from FEAScript-core 0.4.0 (RC).

## Advection-diffusion in 1D

Steady advection-diffusion on $[0, 1]$ with a Gaussian source centered at $x = 0.5$:

$$
\frac{d^2u}{dx^2} - 10 \, \frac{du}{dx} = 10 \, e^{-200 (x - 0.5)^2},
$$

that is $A = 1$, $B = -10$, $C = 0$ and $D(x) = 10 \, e^{-200 (x - 0.5)^2}$ in the general form. The value is
fixed at the inlet, $u(0) = 1$, and the gradient is zero at the outlet.

```bash
node advectionDiffusion1D/advectionDiffusion1D.js
```

Source:
[`advectionDiffusion1D.js`](https://github.com/FEAScript/FEAScript-core/blob/main/examples/generalFormPDEScript/advectionDiffusion1D/advectionDiffusion1D.js)

### Geometry

![1D domain with a fixed value at the left end, zero gradient at the right end and a Gaussian source](/assets/examples/advection-diffusion-geometry.svg)

### Mesh

![20 quadratic elements: end nodes as open circles, midside nodes as dots](/assets/examples/advection-diffusion-mesh.svg)

### Results

![Solution falling from 1 at the inlet to 0.8756 downstream of the source](/assets/examples/advection-diffusion-results.svg)

Upstream of the source the solution stays close to the inlet value. Across the source it drops, and downstream
it is carried unchanged to the outlet, where $u(1) = 0.8756$. The markers are the end nodes of the elements.
The example prints the node coordinates and the solution vector.

## Nonlinear reaction-diffusion in 1D

Steady diffusion with a quadratic reaction on $[0, 10]$:

$$
\frac{d^2u}{dx^2} - u^2 = 0,
$$

solved with the Newton-Raphson method (`nonlinear: true`, with $D(x, u) = u^2$ and its derivative
$\partial D / \partial u = 2u$). The value is fixed at $u(0) = 1$ and the gradient is zero at $x = 10$.

```bash
node nonlinearReactionDiffusion1D/nonlinearReactionDiffusion1D.js
```

Source:
[`nonlinearReactionDiffusion1D.js`](https://github.com/FEAScript/FEAScript-core/blob/main/examples/generalFormPDEScript/nonlinearReactionDiffusion1D/nonlinearReactionDiffusion1D.js)

### Geometry

![1D domain of length 10 with a fixed value at the left end and zero gradient at the right end](/assets/examples/reaction-diffusion-geometry.svg)

### Mesh

![20 linear elements](/assets/examples/reaction-diffusion-mesh.svg)

### Results

![Solution decaying from 1 at x = 0 to 0.0568 at x = 10](/assets/examples/reaction-diffusion-results.svg)

The reaction consumes $u$ as it diffuses into the domain: on the 20 linear elements of the example, $u = 0.5009$
at $x = 1$ and $u = 0.0568$ at $x = 10$. The elements are 0.5 long, so these values are 0.7 % and 0.5 % below the
mesh-converged solution, $u(1) = 0.5043$ and $u(10) = 0.0571$, which FEAScript reaches on finer meshes. The example prints the node coordinates and the solution
vector.
