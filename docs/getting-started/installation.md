---
sidebar_position: 1
---

# Installation

## In the browser

Import the ES module build from the hosted build or from a CDN:

```html
<script type="module">
  import { FEAScriptModel } from "https://core.feascript.com/dist/feascript.esm.js";
</script>
```

```html
<script type="module">
  import { FEAScriptModel } from "https://cdn.jsdelivr.net/gh/FEAScript/FEAScript-core/dist/feascript.esm.js";
</script>
```

You can also download a release from [GitHub Releases](https://github.com/FEAScript/FEAScript-core/releases) and import it locally.

## With Node.js

```bash
npm install feascript
```

```javascript
import { FEAScriptModel } from "feascript";
```

FEAScript is built as an ES module. In a new project, set `"type": "module"` in your `package.json`.
