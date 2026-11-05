---
sidebar_position: 2
---

# Heat conduction

Node.js examples of [`heatConductionScript`](../models/heat-conduction), in
[`examples/heatConductionScript`](https://github.com/FEAScript/FEAScript-core/tree/main/examples/heatConductionScript).
Run the commands below from that folder (see [running an example](overview#running-an-example)). All results are
from FEAScript-core 0.4.0 (RC).

## Wall in 1D

Steady heat flow through a building wall 0.15 m thick. The inner side exchanges heat with the room by convection
($h = 1$ W/(m²·K), $T_\infty = 25$ °C) and the outer side is held at 5 °C. $k = 1$ W/(m·K).

```bash
node heatConduction1DWall/heatConduction1DWall.js
```

Source:
[`heatConduction1DWall.js`](https://github.com/FEAScript/FEAScript-core/blob/main/examples/heatConductionScript/heatConduction1DWall/heatConduction1DWall.js)

### Geometry

![Wall 0.15 m thick with convection on the left side and a fixed temperature on the right side](/assets/examples/wall-geometry.svg)

### Mesh

![10 linear elements over the wall thickness](/assets/examples/wall-mesh.svg)

### Results

![Temperature through the wall: a straight line from 7.6087 °C at the inner side to 5 °C at the outer side](/assets/examples/wall-results.svg)

With constant $k$ and no heat source the temperature is linear through the wall. It falls from 7.6087 °C at the
inner side to 5 °C at the outer side, the exact values: the heat flux is $(25 - 5) / (1/h + W/k) = 17.3913$ W/m²,
so $T(0) = 25 - 17.3913 / h$. The example solves with the Jacobi method; the linear elements are exact at the
nodes. The example prints the node coordinates and the solution vector.

## Bi-material wall in 1D

The same wall in two layers: concrete ($k = 10$ W/(m·K)) for $x < 0.075$ m and insulation ($k = 1$ W/(m·K))
beyond. The conductivity is given as a function of position, `(x) => (x < 0.075 ? 10 : 1)`. The inner side
exchanges heat by convection ($h = 25$ W/(m²·K), $T_\infty = 5$ °C) and the outer side is held at 20 °C.

```bash
node heatConduction1DWall/heatConduction1DVaryingK.js
```

Source:
[`heatConduction1DVaryingK.js`](https://github.com/FEAScript/FEAScript-core/blob/main/examples/heatConductionScript/heatConduction1DWall/heatConduction1DVaryingK.js)

### Geometry

![Wall in two layers, k = 10 on the left half and k = 1 on the right half](/assets/examples/wall-varying-k-geometry.svg)

### Mesh

![20 linear elements, with the material interface at a node](/assets/examples/wall-varying-k-mesh.svg)

### Results

![Temperature through the bi-material wall: a gentle slope in the concrete and a steep slope in the insulation](/assets/examples/wall-varying-k-results.svg)

The heat flux is the same in both layers, so the temperature gradient is 10 times steeper in the insulation. The
temperature is 9.8980 °C at the inner side and 10.8163 °C at the interface. The example prints the node
coordinates and the solution vector.

## Fin in 2D

A 4 m × 2 m cooling fin, $k = 1$ W/(m·K): fixed temperature of 200 °C at the bottom and right edges, symmetry
at the left edge, and convection ($h = 1$ W/(m²·K), $T_\infty = 20$ °C) at the top edge. The mesh is generated
by FEAScript.

```bash
node heatConduction2DFin/heatConduction2DFin.js
```

Source:
[`heatConduction2DFin.js`](https://github.com/FEAScript/FEAScript-core/blob/main/examples/heatConductionScript/heatConduction2DFin/heatConduction2DFin.js)

### Geometry

![4 m by 2 m fin with fixed temperature at the bottom and right, symmetry at the left and convection at the top](/assets/examples/fin-geometry.svg)

### Mesh

![8 by 4 quadratic quadrilaterals with the boundary numbering](/assets/examples/fin-mesh.svg)

### Results

![Temperature contours of the fin, falling from 200 °C at the heated edges to 81 °C at the top left corner](/assets/examples/fin-results.svg)

The lowest temperature, 81.3187 °C, is at the top left corner, farthest from the heated edges. The example
prints the node coordinates and the solution vector.

### Comparison with Elmer

The fin was also solved with [Elmer](https://www.elmerfem.org/), the open-source finite element software of CSC –
IT Center for Science, on the same structured meshes, with linear and quadratic quadrilaterals from 231 to 51,681
nodes. The problem has an exact solution, a Fourier series,

$$
T(x, y) = 200 + \sum_{n=1}^{\infty} A_n \cos(\lambda_n x) \sinh(\lambda_n y), \qquad
\lambda_n = \frac{(2n-1)\pi}{8},
$$

so both programs are compared with it at every node, and with each other:

| Elements  | Mesh      | Nodes  | Largest error (°C) | RMS error (°C) | Difference from Elmer (°C) |
| --------- | --------- | ------ | ------------------ | -------------- | -------------------------- |
| Linear    | 20 × 10   | 231    | 1.0e0              | 1.1e-1         | 5.0e-6                     |
| Linear    | 40 × 20   | 861    | 5.7e-1             | 3.2e-2         | 5.0e-6                     |
| Linear    | 80 × 40   | 3,321  | 3.1e-1             | 8.8e-3         | 5.0e-6                     |
| Linear    | 160 × 80  | 13,041 | 1.6e-1             | 2.4e-3         | 5.0e-6                     |
| Linear    | 320 × 160 | 51,681 | 8.1e-2             | 6.7e-4         | 5.0e-6                     |
| Quadratic | 10 × 5    | 231    | 8.0e-1             | 6.7e-2         | 5.0e-6                     |
| Quadratic | 20 × 10   | 861    | 3.9e-1             | 1.7e-2         | 5.0e-6                     |
| Quadratic | 40 × 20   | 3,321  | 2.0e-1             | 4.3e-3         | 5.0e-6                     |
| Quadratic | 80 × 40   | 13,041 | 9.7e-2             | 1.1e-3         | 5.0e-6                     |
| Quadratic | 160 × 80  | 51,681 | 4.9e-2             | 2.7e-4         | 5.0e-6                     |

![Fin in 2D: largest error against the exact solution against element size, for linear and quadratic elements, logarithmic axes](/assets/examples/fin-elmer-comparison.svg)

The errors of Elmer are the same to the digits shown, and the temperatures of the two programs differ by at most
5.0e-6 °C on every mesh, the rounding of the 8 significant digits that Elmer writes its results with. The
largest error is at the node next to the top right corner, where the fixed temperature of the right edge meets the
convection of the top edge and the exact solution is not smooth. There it falls only in proportion to the element
size $h$, with either element; the RMS error over all the nodes falls about as $h^2$.

FEAScript-core 0.4.0 (RC) was used, with `"frontal"` and `"lusolve"`, which give the same temperatures. Elmer used
its `HeatSolver` with the UMFPACK direct solver, run on one core as a single MPI process. For the solve times, see
[Solvers](../fundamentals/solvers.mdx#performance). The benchmark, with the Elmer setup, is in
[FEAScript-benchmark](https://github.com/FEAScript/FEAScript-benchmark).

### Comparison with scikit-fem

The fin was also solved with [scikit-fem](https://github.com/kinnala/scikit-fem), an open-source finite element library for Python, on the
same meshes, with the same elements and its default direct solver. The temperatures of FEAScript and scikit-fem
differ by at most 1.8e-10 °C on every mesh, from 231 to 51,681 nodes. This comparison is closer than the one with
Elmer because scikit-fem's results are kept to full double precision.

## Fin in 2D, Gmsh mesh

The fin of the previous example on an unstructured mesh made with [Gmsh](https://gmsh.info/), read from
`rect_quad.msh` (see [Gmsh import](../api/gmsh-import)). The geometry and boundary conditions are the same; the
physical groups of the mesh are tagged bottom, left, top, right, like the sides of the structured mesh.

```bash
node heatConduction2DFin/heatConduction2DFinGmsh.js
```

Source:
[`heatConduction2DFinGmsh.js`](https://github.com/FEAScript/FEAScript-core/blob/main/examples/heatConductionScript/heatConduction2DFin/heatConduction2DFinGmsh.js)

### Mesh

![30 quadratic quadrilaterals made with Gmsh, with the boundary numbering](/assets/examples/fin-gmsh-mesh.svg)

### Results

![Temperature contours of the fin on the Gmsh mesh](/assets/examples/fin-gmsh-results.svg)

The lowest temperature is 81.3207 °C, against 81.3187 °C on the structured mesh. The example prints the node
coordinates and the solution vector.

## Rhomboid fin in 2D, Gmsh mesh

A fin whose top edge is shifted by 1 m, so the left and right edges slant. The boundary conditions are those of
the rectangular fin. The mesh is read from `rhom_quad.msh`.

```bash
node heatConduction2DFin/heatConduction2DRhomFinGmsh.js
```

Source:
[`heatConduction2DRhomFinGmsh.js`](https://github.com/FEAScript/FEAScript-core/blob/main/examples/heatConductionScript/heatConduction2DFin/heatConduction2DRhomFinGmsh.js)

### Geometry

![Rhomboid fin: bottom edge 4 m, top edge shifted by 1 m, height 2 m](/assets/examples/rhomboid-fin-geometry.svg)

### Mesh

![24 quadratic quadrilaterals made with Gmsh, with the boundary numbering](/assets/examples/rhomboid-fin-mesh.svg)

### Results

![Temperature contours of the rhomboid fin](/assets/examples/rhomboid-fin-results.svg)

The lowest temperature, 87.5205 °C, is on the top edge, at $x = 2.25$ m, between two nodes (the lowest nodal
value is 87.6060 °C, at $x = 2.3333$ m). The example prints the node
coordinates and the solution vector.

## Fin in 2D with spatially varying k and Q

The fin of the first 2D example with two materials and a local heat source: $k = 10$ W/(m·K) for $x < 2$ m and
$k = 1$ W/(m·K) beyond, and a heat source $Q = 500$ W/m³ in the strip $y > 1.5$ m. Both are given as functions
of position.

```bash
node heatConduction2DFin/heatConduction2DVaryingKQ.js
```

Source:
[`heatConduction2DVaryingKQ.js`](https://github.com/FEAScript/FEAScript-core/blob/main/examples/heatConductionScript/heatConduction2DFin/heatConduction2DVaryingKQ.js)

### Geometry

![Fin with k = 10 on the left half, k = 1 on the right half and a heat source in the top strip](/assets/examples/fin-varying-geometry.svg)

### Mesh

The mesh is that of the [fin in 2D](#fin-in-2d): 8 × 4 quadratic quadrilaterals.

### Results

![Temperature contours with a hot spot in the heated strip of the low-conductivity half](/assets/examples/fin-varying-results.svg)

The heat source raises the temperature above that of the heated edges. The highest temperature, 240.1414 °C, is
at (2.875 m, 1.625 m), inside an element, in the low-conductivity half, where the heat has the most difficulty
escaping. The highest nodal value is 237.4724 °C, at (3 m, 1.5 m). On a mesh refined 8 times in each
direction (64 × 32 elements) the peak is 240.2033 °C at (2.875 m, 1.594 m).

At $x = 2$ m the contour lines bend: the heat flux is continuous across the material interface, so the
temperature gradient is 10 times steeper on the low-conductivity side.
