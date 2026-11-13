---
sidebar_position: 1
---

# Installation

<img className="topic-logo" src="/assets/topics/installation.svg" alt="" />

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
  import { FEAScriptModel } from "https://cdn.jsdelivr.net/gh/FEAScript/FEAScript-core@0.4.0/dist/feascript.esm.js";
</script>
```
:::

You can also download a release from [GitHub Releases](https://github.com/FEAScript/FEAScript-core/releases) and import it locally.

### With a script tag

Pages that do not use ES modules can load the UMD build with a classic `<script>` tag. It defines a global
`FEAScript` object that holds every export:

```html
<script src="https://core.feascript.com/dist/feascript.umd.js"></script>
<script>
  const { FEAScriptModel, plotSolution } = FEAScript;
</script>
```

`FEAScriptWorker` works with this build too: it loads `feascript-worker.esm.js` from the same folder as
`feascript.umd.js`, so keep the files of `dist/` together when you host the library yourself.

## With Node.js

```bash
npm install feascript
```

```javascript
import { FEAScriptModel } from "feascript";
```

FEAScript is built as an ES module. In a new project, set `"type": "module"` in your `package.json`.

### TypeScript and editors

The npm package ships TypeScript declarations, so TypeScript projects are type-checked against the FEAScript API,
and editors such as VS Code show the options of each method and complete them as you type, in JavaScript too.
A misspelled model name, solver method or boundary condition parameter is marked before the code runs:

```typescript
import { FEAScriptModel } from "feascript";
import type { SolveResult } from "feascript";

const model = new FEAScriptModel();
model.setModelConfig("heatConduction", { solver: { method: "frontal" } });
model.addBoundaryCondition("top", { type: "convection", h: 1, ambientTemperature: 20 });
const result: SolveResult = model.solve();
console.log(result.info.solveTime);
```

The types of the inputs and the results (`Geometry`, `MeshConfig`, `BoundaryCondition`, `SolveResult`,
`RunReport` and the others) can be imported with `import type`.

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
| `generateTriangleMesh`, `generateQuadrilateralMesh` | ✓      | ✓                                         |
| `importGmshMesh`                   | ✓                   | ✓ (pass an object with a `text()` method) |
| Plotting with Plotly or vtk.js     | ✓                   |                                           |
| `FEAScriptWorker`                  | ✓                   |                                           |
| `"jacobi-gpu"` with `solveAsync()` | ✓ (WebGPU required) |                                           |
