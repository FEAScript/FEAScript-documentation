---
sidebar_position: 1
---

# Installation

FEAScript 0.2.0 solves linear systems with [math.js](https://mathjs.org/), which it expects as a **global**
`math` object. Load math.js before you call `solve()`, as shown below.

## In the browser

Load math.js with a `<script>` tag, then import the ES module build of FEAScript 0.2.0 from a CDN:

```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/mathjs/11.12.0/math.min.js"></script>

<script type="module">
  import { FEAScriptModel } from "https://cdn.jsdelivr.net/npm/feascript@0.2.0/dist/feascript.esm.js";
</script>
```

:::note
`https://core.feascript.com/dist/feascript.esm.js` always serves the latest release of FEAScript, not 0.2.0. Pin
the version in the URL, as above, to keep using 0.2.0.
:::

[`FEAScriptWorker`](../api/web-worker.md) and the [`"jacobi-gpu"` solver](../fundamentals/solvers.md#jacobi-method-on-the-gpu-jacobi-gpu)
start web workers whose scripts are not part of the bundled build. To use them, import the source modules
instead:

```javascript
import { FEAScriptWorker } from "https://cdn.jsdelivr.net/npm/feascript@0.2.0/src/index.js";
```

You can also download the release from [GitHub Releases](https://github.com/FEAScript/FEAScript-core/releases) and import it locally.

## With Node.js

```bash
npm install feascript@0.2.0 mathjs
```

```javascript
import * as math from "mathjs";
global.math = math;

import { FEAScriptModel } from "feascript";
```

FEAScript is built as an ES module. In a new project, set `"type": "module"` in your `package.json`.

## Optional dependencies

The plotting functions use [Plotly](https://plotly.com/javascript/), through the global `Plotly` object. In the
browser, load `plotly.min.js` with a `<script>` tag (see [Visualization](../api/visualization.md)).

## Environments

| Feature                            | Browser             | Node.js                                   |
| ---------------------------------- | ------------------- | ----------------------------------------- |
| Models, meshes, `solve()`          | ✓                   | ✓                                         |
| `importGmshQuadTri`                | ✓                   | ✓ (pass an object with a `text()` method) |
| Plotting with Plotly               | ✓                   |                                           |
| `FEAScriptWorker`                  | ✓                   |                                           |
| `"jacobi-gpu"` with `solveAsync()` | ✓ (WebGPU required) |                                           |
