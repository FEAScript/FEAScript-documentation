---
sidebar_position: 1
---

# Installation

## In the browser

Import the ES module build from the jsDelivr CDN or from the hosted build:

```html
<script type="module">
  import { FEAScriptModel } from "https://cdn.jsdelivr.net/gh/FEAScript/FEAScript-core/dist/feascript.esm.js";
</script>
```

```html
<script type="module">
  import { FEAScriptModel } from "https://core.feascript.com/dist/feascript.esm.js";
</script>
```

:::note
Both URLs above always serve the latest FEAScript release, so your page updates automatically when a new version is published (new versions may include breaking changes). To freeze your page to a specific version, add a version tag to the jsDelivr URL:

```html
<script type="module">
  import { FEAScriptModel } from "https://cdn.jsdelivr.net/gh/FEAScript/FEAScript-core@0.3.1/dist/feascript.esm.js";
</script>
```
:::

You can also download a release from [GitHub Releases](https://github.com/FEAScript/FEAScript-core/releases) and import it locally.

## With Node.js

```bash
npm install feascript
```

```javascript
import { FEAScriptModel } from "feascript";
```

FEAScript is built as an ES module. In a new project, set `"type": "module"` in your `package.json`.

## Optional dependencies

FEAScript itself needs no extra setup to solve a model. The plotting functions use two optional libraries:

| Library                                     | Used by                                                      | Browser                                                      | npm                           |
| ------------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ | ----------------------------- |
| [Plotly](https://plotly.com/javascript/)    | `plotSolution`, `plotInterpolatedSolution`                   | Load `plotly.min.js` with a `<script>` tag (global `Plotly`) | `npm install plotly.js`       |
| [vtk.js](https://kitware.github.io/vtk-js/) | `plotSolutionVtk`, `plotInterpolatedSolutionVtk`, VTK export | Map `@kitware/vtk.js/` with an import map                    | `npm install @kitware/vtk.js` |

See [Visualization](../api/visualization.md) for the details.

## Environments

| Feature                            | Browser             | Node.js                                   |
| ---------------------------------- | ------------------- | ----------------------------------------- |
| Models, meshes, `solve()`          | ✓                   | ✓                                         |
| `importGmshMesh`                   | ✓                   | ✓ (pass an object with a `text()` method) |
| Plotting with Plotly or vtk.js     | ✓                   |                                           |
| `FEAScriptWorker`                  | ✓                   |                                           |
| `"jacobi-gpu"` with `solveAsync()` | ✓ (WebGPU required) |                                           |
