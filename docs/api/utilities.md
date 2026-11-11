---
sidebar_position: 6
---

# Utilities

<img className="topic-logo" src="/assets/topics/utilities.svg" alt="" />

## `logSystem`

```javascript
import { logSystem } from "feascript";

logSystem("debug");
```

Sets how much FEAScript prints to the console.

| Level     | Output                                                                                                                |
| --------- | --------------------------------------------------------------------------------------------------------------------- |
| `"none"`  | Errors and warnings only                                                                                              |
| `"basic"` | Default. Adds progress messages (`[INFO]`), including the error norm of every Newton–Raphson iteration                |
| `"debug"` | Adds detailed messages (`[DEBUG]`), such as the nodes of every boundary condition and the number of Jacobi iterations |

Errors (`[ERROR]`) and warnings (`[WARN]`) are always printed. Any other value falls back to `"basic"` with a
warning. The timings of the solution steps (`totalSolvingTime`, `systemSolving`) are printed with `console.time`
at every level.

## `version`

```javascript
import { version } from "feascript";

console.log("FEAScript version:", version); // "0.4.0"
```

A string constant with the version of the library, as in its npm package (`"0.4.0"`; a release candidate reads
`"0.4.0-rc.1"`).

`printVersion`, the name used up to FEAScript 0.3, is still exported but deprecated; use `version`. It will be
removed in a future version.
