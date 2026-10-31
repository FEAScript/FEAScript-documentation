---
sidebar_position: 1
---

# Examples overview

FEAScript-core ships with Node.js examples for every model, in the
[`examples`](https://github.com/FEAScript/FEAScript-core/tree/main/examples) folder. Each example is a single
script that sets up a model in the five steps of [your first simulation](../getting-started/first-simulation),
solves it and prints the results.

These pages show, for each example, the geometry and boundary conditions, the mesh, and the results. The results
were computed with **FEAScript-core 0.4.0 (RC)**, by running the examples unchanged.

## Examples

| Model                                        | Example                                                                                              | Mesh                               |
| -------------------------------------------- | ---------------------------------------------------------------------------------------------------- | ---------------------------------- |
| [Heat conduction](heat-conduction)           | [Wall in 1D](heat-conduction#wall-in-1d)                                                             | 10 linear elements                 |
| [Heat conduction](heat-conduction)           | [Bi-material wall in 1D](heat-conduction#bi-material-wall-in-1d)                                     | 20 linear elements                 |
| [Heat conduction](heat-conduction)           | [Fin in 2D](heat-conduction#fin-in-2d)                                                               | 8 × 4 quadratic quadrilaterals     |
| [Heat conduction](heat-conduction)           | [Fin in 2D, Gmsh mesh](heat-conduction#fin-in-2d-gmsh-mesh)                                          | 30 quadratic quadrilaterals (Gmsh) |
| [Heat conduction](heat-conduction)           | [Rhomboid fin in 2D, Gmsh mesh](heat-conduction#rhomboid-fin-in-2d-gmsh-mesh)                        | 24 quadratic quadrilaterals (Gmsh) |
| [Heat conduction](heat-conduction)           | [Fin in 2D with spatially varying k and Q](heat-conduction#fin-in-2d-with-spatially-varying-k-and-q) | 8 × 4 quadratic quadrilaterals     |
| [General form PDE](general-form-pde)         | [Advection-diffusion in 1D](general-form-pde#advection-diffusion-in-1d)                              | 20 quadratic elements              |
| [General form PDE](general-form-pde)         | [Nonlinear reaction-diffusion in 1D](general-form-pde#nonlinear-reaction-diffusion-in-1d)            | 20 linear elements                 |
| [Front propagation](front-propagation)       | [Solidification front in 2D](front-propagation#solidification-front-in-2d)                           | 12 × 8 quadratic quadrilaterals    |
| [Creeping flow](creeping-flow)               | [Lid-driven cavity in 2D](creeping-flow#lid-driven-cavity-in-2d)                                     | 12 × 6 Q2-Q1 quadrilaterals        |
| [Creeping flow](creeping-flow)               | [Couette flow in 2D](creeping-flow#couette-flow-in-2d)                                               | 4 × 2 Q2-Q1 quadrilaterals         |
| [Euler–Bernoulli beam](euler-bernoulli-beam) | [Clamped and spring-supported beam](euler-bernoulli-beam#clamped-and-spring-supported-beam)          | 2 cubic Hermite elements           |
| [Euler–Bernoulli beam](euler-bernoulli-beam) | [Cantilever beam](euler-bernoulli-beam#cantilever-beam)                                              | 4 cubic Hermite elements           |

## Running an example

The examples import FEAScript from npm. In the folder of a model (for example
`examples/heatConductionScript`), or in an empty folder with a copy of the example:

1. Create a `package.json` with ES module support:

   ```bash
   echo '{"type":"module"}' > package.json
   ```

2. Install FEAScript:

   ```bash
   npm install feascript
   ```

3. Run the example, for example:

   ```bash
   node heatConduction2DFin/heatConduction2DFin.js
   ```

The Gmsh examples read their `.msh` file from the folder of the script, so they can be run from any folder.
Every example prints the FEAScript version first, then its results: some print the node coordinates and the
solution vector, others a short summary next to the exact or published values. The command to run each example
is given in its section.

## How the figures were made

Geometries and meshes are drawn from the same values as the examples: the structured meshes from the mesh
generator of FEAScript, the Gmsh meshes from the `.msh` files of the examples. The result figures show the
solution that each example computes. Contour lines follow the finite element solution inside each element: the
field is evaluated with the shape functions of the element on a fine grid of points, not interpolated linearly
between the nodes. The highest and lowest values quoted on these pages are found the same way, so they can lie
between the nodes.
