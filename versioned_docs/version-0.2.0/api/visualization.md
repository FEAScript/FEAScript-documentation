---
sidebar_position: 3
---

# Visualization

FEAScript 0.2.0 plots results with [Plotly](https://plotly.com/javascript/). Load Plotly with a `<script>` tag
before using these functions; FEAScript uses the global `Plotly` object:

```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/plotly.js/2.35.3/plotly.min.js"></script>
<div id="resultsCanvas"></div>
```

Both plotting functions take the same arguments:

| Parameter   | Type     | Description                                                                                                                               |
| ----------- | -------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| `model`     | `object` | The `FEAScriptModel`, or any object with its `solverConfig` and `meshConfig` (for example the result of `FEAScriptWorker.getModelInfo()`) |
| `result`    | `object` | The object returned by `solve()`: `{ solutionVector, nodesCoordinates }`                                                                  |
| `plotType`  | `string` | `"line"` for 1D meshes, `"contour"` for 2D meshes                                                                                         |
| `plotDivId` | `string` | `id` of the HTML element in which the plot is drawn                                                                                       |

The plotting functions draw one value per mesh node. For the creeping flow model, whose `solutionVector` holds
several fields, slice the field to plot and pass it as the `solutionVector` of `result` (see
[Creeping flow](../models/creeping-flow.md#results)).

## `plotSolution(model, result, plotType, plotDivId)`

Plots the nodal values directly:

- `"line"` (1D): a line plot of the solution along $x$.
- `"contour"` (2D): a contour plot built from the nodal values and coordinates.

```javascript
const result = model.solve();
plotSolution(model, result, "contour", "resultsCanvas");
```

## `plotInterpolatedSolution(model, result, plotType, plotDivId)`

Evaluates the finite element solution, with the basis functions of each element, on a regular grid of 50 points
per unit length, and draws a contour plot of it. Grid points outside the mesh are left empty, so non-rectangular
domains (for example Gmsh meshes) are drawn with their true shape. It supports `"contour"` on 2D meshes only.

```javascript
plotInterpolatedSolution(model, result, "contour", "resultsCanvas");
```

:::note
The grid density is fixed at 50 points per unit length of the domain, so the number of grid points depends on the
units of the model: a domain of 0.1 × 0.1 gets a coarse grid, and a very large domain a very dense one. Use
`plotSolution` in these cases.
:::
