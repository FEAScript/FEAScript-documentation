---
sidebar_position: 3
---

# Visualization

FEAScript can plot results with [Plotly](https://plotly.com/javascript/) or [vtk.js](https://kitware.github.io/vtk-js/),
and export them for other tools. Both libraries are optional peer dependencies: load only the one you use.

All plotting functions take the same first arguments:

| Parameter   | Type     | Description                                                                                                                               |
| ----------- | -------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| `model`     | `object` | The `FEAScriptModel`, or any object with its `solverConfig` and `meshConfig` (for example the result of `FEAScriptWorker.getModelInfo()`) |
| `result`    | `object` | `{ solutionVector, nodesCoordinates }`, as returned by `solve()`                                                                          |
| `plotType`  | `string` | `"line"` for 1D meshes, `"contour"` for 2D meshes                                                                                         |
| `plotDivId` | `string` | `id` of the HTML element in which the plot is drawn                                                                                       |

The plotting functions draw one value per mesh node, taken from the beginning of `solutionVector`. For models with
several unknowns per node, pass the field to plot instead of the full solution vector, for example
`{ solutionVector: velocityMagnitude, nodesCoordinates }` (see the
[creeping flow](../models/creeping-flow.md#results) and
[Euler–Bernoulli beam](../models/euler-bernoulli-beam.md#results) pages).

## Plotly

Load Plotly with a `<script>` tag before using these functions; FEAScript uses the global `Plotly` object:

```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/plotly.js/2.35.3/plotly.min.js"></script>
<div id="resultsCanvas"></div>
```

### `plotSolution(model, result, plotType, plotDivId)`

Plots the nodal values directly:

- `"line"` (1D): a line plot of the solution along $x$.
- `"contour"` (2D): a contour plot built from the nodal values and coordinates.

```javascript
const result = model.solve();
plotSolution(model, result, "contour", "resultsCanvas");
```

### `plotInterpolatedSolution(model, result, plotType, plotDivId)`

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

## vtk.js

The vtk.js functions are `async`. They import vtk.js modules with bare specifiers (`@kitware/vtk.js/...`):

- with npm and a bundler, install `@kitware/vtk.js` (version 32);
- in the browser without a bundler, map the specifiers with an import map:

```html
<script type="importmap">
  {
    "imports": {
      "@kitware/vtk.js/": "https://cdn.jsdelivr.net/npm/@kitware/vtk.js@32.12.0/",
      "gl-matrix": "https://esm.sh/v135/gl-matrix@3.4.3",
      "d3-scale": "https://esm.sh/v135/d3-scale@4.0.2",
      "fast-deep-equal": "https://esm.sh/v135/fast-deep-equal@3.1.3",
      "seedrandom": "https://esm.sh/v135/seedrandom@3.0.5",
      "spark-md5": "https://esm.sh/v135/spark-md5",
      "fflate": "https://esm.sh/v135/fflate",
      "utif": "https://esm.sh/v135/utif",
      "webworker-promise": "https://esm.sh/v135/webworker-promise",
      "xmlbuilder2": "https://esm.sh/v135/xmlbuilder2",
      "globalthis": "data:text/javascript,export default function(){return globalThis}"
    }
  }
</script>
```

### `plotSolutionVtk(model, result, plotType, plotDivId, renderOptions)`

Renders the nodal solution on the mesh elements (`"contour"`, 2D) or as a line (`"line"`, 1D), in an interactive
canvas with pan and zoom.

### `plotInterpolatedSolutionVtk(model, result, plotType, plotDivId, renderOptions)`

Renders the solution interpolated with the basis functions of each element, for smoother contours. It supports
`"contour"` on 2D meshes; for other cases it falls back to `plotSolutionVtk`.

```javascript
await plotInterpolatedSolutionVtk(model, result, "contour", "resultsCanvas", {
  colorScale: createColorScale({ presetName: "Cool to Warm", scalarBarTitle: "Temperature" }),
  contourLines: createContourLineOptions({ enabled: true, numberOfContours: 14, lineWidth: 1.25 }),
});
```

| `renderOptions` property | Default                | Description                           |
| ------------------------ | ---------------------- | ------------------------------------- |
| `colorScale`             | `createColorScale({})` | Color map and scalar bar              |
| `contourLines`           | Contour lines disabled | Contour lines drawn over the solution |

### `createColorScale(options)`

| Option           | Default          | Description                       |
| ---------------- | ---------------- | --------------------------------- |
| `presetName`     | `"Cool to Warm"` | Name of a vtk.js color map preset |
| `reverse`        | `false`          | Reverse the color map             |
| `showScalarBar`  | `true`           | Show the scalar bar               |
| `scalarBarTitle` | `"Solution"`     | Title of the scalar bar           |

### `createContourLineOptions(options)`

| Option             | Default              | Description                         |
| ------------------ | -------------------- | ----------------------------------- |
| `enabled`          | `true`               | Draw contour lines                  |
| `numberOfContours` | `12`                 | Number of contour lines             |
| `color`            | `[0.15, 0.15, 0.15]` | RGB color, each component in [0, 1] |
| `lineWidth`        | `1`                  | Line width                          |

## Export

### `transformSolverOutputToVTP(model, result, meshData, options)`

Returns a `Promise` with the result as a VTK PolyData XML string, which can be saved as a `.vtp` file and opened in
[ParaView](https://www.paraview.org/). `meshData` can be `null` (the mesh is prepared from `model.meshConfig`),
and `options.mode` is `"surface"` (default, mesh elements) or `"line"` (1D).

```javascript
const vtp = await transformSolverOutputToVTP(model, result, null, { mode: "surface" });
```

### `transformSolverOutputToVtkData(model, result, meshData, options)`

Same arguments as `transformSolverOutputToVTP`. Returns a `Promise` with the vtk.js data of the result:
`{ points, scalars, cells, polyData, mode, metadata }`, where `polyData` is a vtk.js `vtkPolyData` object.

Both export functions use vtk.js modules, so vtk.js must be available as described above.

### `transformSolverOutputToMLBuffers(result)`

Returns the result as typed arrays, for example to train a machine learning model:

| Property        | Type           | Description                                     |
| --------------- | -------------- | ----------------------------------------------- |
| `features`      | `Float32Array` | $N \times 3$ values, $[x, y, u]$ for every node |
| `featuresShape` | `number[]`     | `[N, 3]`                                        |
| `labels`        | `Float32Array` | The $N$ nodal solution values                   |
| `points`        | `Float32Array` | $N \times 3$ coordinates $[x, y, 0]$            |

This function is synchronous and does not need vtk.js.
