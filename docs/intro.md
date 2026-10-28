---
slug: /
sidebar_position: 1
---

# Introduction

**FEAScript** is a finite element simulation library developed in JavaScript. It enables engineering simulations in both browser-based and server-side (Node.js) environments, without the overhead of traditional desktop software.

:::caution
FEAScript is under heavy development. Its functionality and interfaces may change rapidly. Use the version selector in the navigation bar to read the documentation that matches the release you are using.
:::

## Features

- **Physics models:** creeping (Stokes) flow, Euler-Bernoulli beam bending, front propagation, heat conduction, general form PDE (linear and nonlinear)
- **Meshing:** simple 1D/2D mesh generation, unstructured mesh import from Gmsh (`.msh`) with quadrilateral and triangular elements (linear and quadratic)
- **Solvers:** frontal, Jacobi (CPU/WebGPU) and LU, Newton–Raphson for nonlinear systems
- **Performance:** web worker support for multi-threaded computation
- **Visualization:** interactive rendering with vtk.js and Plotly

## Where to go next

- [Installation](./getting-started/installation.md) – use FEAScript in the browser or with Node.js
- [Your first simulation](./getting-started/first-simulation.md)
- [Heat conduction model](./models/heat-conduction.md)
