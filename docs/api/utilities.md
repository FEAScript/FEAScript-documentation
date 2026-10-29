---
sidebar_position: 5
---

# Utilities

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

## `printVersion`

```javascript
import { printVersion } from "feascript";

console.log("FEAScript version:", printVersion); // "0.3.0 (RC)"
```

A string constant with the version of the library.
