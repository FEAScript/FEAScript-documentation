---
sidebar_position: 1
---

# Heat conduction

`heatConductionScript` solves steady-state heat conduction in 1D and 2D, with spatially varying thermal
conductivity and heat source.

## Governing equation

$$
-\nabla \cdot \left( k \, \nabla T \right) = Q \quad \text{in} \quad D,
$$

where $T$ is the temperature, $k$ the thermal conductivity and $Q$ the volumetric heat source. In 1D the
equation reduces to $-\frac{d}{dx}\left(k \frac{dT}{dx}\right) = Q$.

The boundary $\partial D$ is split into parts with prescribed temperature (Dirichlet), convective heat exchange
(Robin), and zero heat flux (Neumann):

$$
\begin{aligned}
T &= T_b && \text{constant temperature}, \\
-k \, \frac{\partial T}{\partial n} &= h \, (T - T_\infty) && \text{convection}, \\
-k \, \frac{\partial T}{\partial n} &= 0 && \text{symmetry or insulation},
\end{aligned}
$$

where $h$ is the convective heat transfer coefficient, $T_\infty$ the temperature of the surrounding fluid and
$\partial / \partial n$ the derivative along the outward normal.

## Weak form

After integration by parts, the Galerkin residuals are

$$
R_i = \int_{D} k \, \nabla \phi^i \cdot \nabla T \, dS
- \int_{D} Q \, \phi^i \, dS
+ \int_{\partial D_{conv}} h \, (T - T_\infty) \, \phi^i \, dt,
\qquad i = 1, 2, \dots, N,
$$

where $\partial D_{conv}$ is the part of the boundary with convection. On the rest of the boundary, the boundary
integral vanishes (zero heat flux) or the residual is replaced by the Dirichlet condition. In 1D the boundary
integral reduces to the value $h \, (T - T_\infty) \, \phi^i$ at the boundary node.

The model is linear, so the system is solved once.

## Usage

```javascript
import { FEAScriptModel } from "feascript";

const model = new FEAScriptModel();

model.setModelConfig("heatConductionScript", {
  coefficientFunctions: {
    thermalConductivity: 1, // k
    heatSource: 0, // Q
  },
});

model.setMeshConfig({
  meshDimension: "2D",
  elementOrder: "quadratic",
  numElementsX: 8,
  numElementsY: 4,
  maxX: 4,
  maxY: 2,
});

model.addBoundaryCondition("0", ["constantTemperature", 200]); // Bottom
model.addBoundaryCondition("1", ["symmetry"]); // Left
model.addBoundaryCondition("2", ["convection", 1, 20]); // Top
model.addBoundaryCondition("3", ["constantTemperature", 200]); // Right

model.setSolverMethod("lusolve");

const { solutionVector, nodesCoordinates } = model.solve();
```

### Coefficient functions

| Property              | Symbol | Default | Type                             |
| --------------------- | ------ | ------- | -------------------------------- |
| `thermalConductivity` | $k$    | `1`     | `number` or function of position |
| `heatSource`          | $Q$    | `0`     | `number` or function of position |

Each coefficient can be a constant or a function of the physical coordinates: `(x) => ...` in 1D and
`(x, y) => ...` in 2D. Functions are evaluated at every integration point, so piecewise (for example
multi-material) and smooth variations are both supported. `coefficientFunctions` can be omitted entirely to use
the defaults.

```javascript
model.setModelConfig("heatConductionScript", {
  coefficientFunctions: {
    // High-conductivity metal on the left half, low-conductivity ceramic on the right half
    thermalConductivity: (x, y) => (x < 2 ? 10 : 1),
    // Heat source in the upper strip only
    heatSource: (x, y) => (y > 1.5 ? 500 : 0),
  },
});
```

FEAScript does not enforce a unit system: use any consistent set of units, for example SI units (W/(m·K) for
$k$, W/m³ for $Q$, W/(m²·K) for $h$, and °C or K for temperatures).

### Boundary conditions

| Condition                    | Parameters                                                  | Kind                |
| ---------------------------- | ----------------------------------------------------------- | ------------------- |
| `["constantTemperature", T]` | Temperature $T_b$                                           | Dirichlet           |
| `["convection", h, Tinf]`    | Heat transfer coefficient $h$, fluid temperature $T_\infty$ | Robin               |
| `["symmetry"]`               | –                                                           | Neumann (zero flux) |

`h` and `Tinf` are constants. A boundary without a condition is insulated (zero heat flux), exactly like
`"symmetry"`. The deprecated name `"constantTemp"` is still accepted, with a warning.

### Solvers

All solver methods are supported: `"lusolve"` (default), `"jacobi"`, `"frontal"`, and `"jacobi-gpu"` with
`solveAsync()`. Coefficient functions are supported by all of them. See [Solvers](../fundamentals/solvers.md).

## Results

`solutionVector` holds the nodal temperatures, in the order of the nodes in `nodesCoordinates` (see
[Node numbering](../fundamentals/mesh.md#node-numbering)). Plot them with
[`plotSolution`](../api/visualization.md) or post-process them directly:

```javascript
const { nodesXCoordinates, nodesYCoordinates } = nodesCoordinates;
const maxTemperature = Math.max(...solutionVector);
```

## Examples

- [Heat conduction in a 1D wall](https://feascript.com/tutorials/heat-conduction-1d-wall.html)
- [Heat conduction in a 2D fin](https://feascript.com/tutorials/heat-conduction-2d-fin.html) (structured mesh)
- [Heat conduction in a 2D fin with a Gmsh mesh](https://feascript.com/tutorials/heat-conduction-2d-fin-gmsh.html)
- [Heat conduction in a 2D rhomboid fin with a Gmsh mesh](https://feascript.com/tutorials/heat-conduction-2d-rhom-fin-gmsh.html)
- Node.js scripts in
  [`examples/heatConductionScript`](https://github.com/FEAScript/FEAScript-core/tree/main/examples/heatConductionScript),
  including spatially varying $k(x)$ and $k(x, y)$, $Q(x, y)$
