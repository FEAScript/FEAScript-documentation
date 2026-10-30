---
slug: /
sidebar_position: 1
---

# Introduction

**FEAScript** is a finite element simulation library developed in JavaScript. It enables engineering simulations in both browser-based and server-side (Node.js) environments, without the overhead of traditional desktop software.

:::caution
This is the documentation of FEAScript **0.2.0**. FEAScript is under heavy development, and its functionality and
interfaces change between versions. Use the version selector in the navigation bar to read the documentation
that matches the release you are using.
:::

## Features

- **Physics models:** creeping (Stokes) flow, front propagation, heat conduction, general form PDE (linear)
- **Meshing:** simple 1D/2D mesh generation, unstructured mesh import from Gmsh (`.msh`) with quadrilateral
  elements (linear and quadratic)
- **Solvers:** frontal, Jacobi (CPU/WebGPU) and LU, Newton–Raphson for nonlinear systems
- **Performance:** web worker support for multi-threaded computation
- **Visualization:** interactive plots with Plotly

## Where to go next

- [Installation](./getting-started/installation.md) – use FEAScript in the browser or with Node.js
- [Your first simulation](./getting-started/first-simulation.md) – a complete example, step by step
- [Fundamentals](./fundamentals/finite-element-method.md) – the finite element formulation, meshes, boundary
  conditions and solvers
- [Models](./models/heat-conduction.md) – the equations and options of every physical model
- [API reference](./api/feascript-model.md) – classes and functions exported by FEAScript
