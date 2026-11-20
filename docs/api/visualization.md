---
sidebar_position: 4
---

# Visualization

<img className="topic-logo" src="/assets/topics/visualization.svg" alt="" />

FEAScript can plot results with [Plotly](https://plotly.com/javascript/) or [vtk.js](https://kitware.github.io/vtk-js/),
and export them for other tools. Both libraries are optional peer dependencies: load only the one you use.

All plotting functions take the same first arguments:

| Parameter   | Type     | Description                                                                                                                               |
| ----------- | -------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| `model`     | `object` | The `FEAScriptModel`, or any object with its `solverConfig` and `meshConfig` (for example the result of `FEAScriptWorker.getModelInfo()`) |
| `result`    | `object` | The object returned by `solve()` (`{ solutionVector, nodesCoordinates }`, and `fields` for models with several unknowns per node)         |
| `plotType`  | `string` | `"line"` for 1D meshes, `"contour"` for 2D meshes                                                                                         |
| `plotDivId` | `string` | `id` of the HTML element in which the plot is drawn                                                                                       |

The plotting functions draw one value per mesh node. For scalar models this is `solutionVector`. Models with
several unknowns per node return named `fields`, and the plotting functions draw one of them, selected with the
`field` option:

| Model                | Fields                             | Default             |
| -------------------- | ---------------------------------- | ------------------- |
| `creepingFlow`       | `velocityMagnitude`, `u`, `v`, `p` | `velocityMagnitude` |
| `eulerBernoulliBeam` | `w`, `theta`                       | `w`                 |

```javascript
const result = model.solve();
plotSolution(model, result, "contour", "velocityMagnitudeCanvas"); // Default field
plotSolution(model, result, "contour", "pressureCanvas", { field: "p" });
```

An unknown field name, a `field` for a scalar model, a plot type the function cannot draw, or a plot element
that does not exist throws a `FEAScriptError` with the code `INVALID_INPUT`. See the
[creeping flow](../models/creeping-flow.md#results) and
[Euler–Bernoulli beam](../models/euler-bernoulli-beam.md#results) pages for the fields.

## Plotly

Load Plotly with a `<script>` tag before using these functions; FEAScript uses the global `Plotly` object:

```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/plotly.js/2.35.3/plotly.min.js"></script>
<div id="resultsCanvas"></div>
```

### `plotSolution(model, result, plotType, plotDivId, options)`

Plots the nodal values directly (`options.field` selects the field, see above):

- `"line"` (1D): a line plot of the solution along $x$.
- `"contour"` (2D): a contour plot built from the nodal values and coordinates.

```javascript
const result = model.solve();
plotSolution(model, result, "contour", "resultsCanvas");
```

### `plotInterpolatedSolution(model, result, plotType, plotDivId, options)`

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
| `field`                  | Default field of model | Field to plot (see above)             |

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

## Values at points

### `evaluateSolution(model, result, points, options)`

:::note
Added in FEAScript 0.4.1.
:::

Returns the solution of a 2D model at the given points, for example to read it along a line or to pass it to
another program on its own grid. Each point is located in the mesh, and the nodal values of its element are
interpolated with the element basis functions, the same way as `plotInterpolatedSolution` does. It needs no
plotting library and also runs in Node.js.

| Parameter       | Type                 | Description                                                                  |
| --------------- | -------------------- | ---------------------------------------------------------------------------- |
| `model`         | `object`             | As for the plotting functions                                                |
| `result`        | `object`             | As for the plotting functions                                                |
| `points`        | `[number, number][]` | The points, as `[x, y]` pairs                                                |
| `options.field` | `string`             | The field to evaluate, for models with several unknowns per node (see above) |

It returns a `Float64Array` with one value per point, in the order of the points. A point outside the mesh
(outside the domain or inside a hole) gets `NaN`, and a point on the boundary counts as inside.

```javascript
const result = model.solve();
const points = [];
for (let i = 0; i <= 20; i++) points.push([i * 0.2, 1]); // A line across the domain at y = 1
const temperatures = evaluateSolution(model, result, points);
```

The values are exact for the fields the elements reproduce: linear fields on linear elements, and quadratic fields
on straight-sided quadratic elements. A 1D model, points that are not an array, or a point that is not a pair of
finite numbers throws a `FEAScriptError` with the code `INVALID_INPUT`.

:::tip
Points that follow each other, such as the points of a grid or a line, are located fastest: the search starts from
the element that held the previous point.
:::

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
