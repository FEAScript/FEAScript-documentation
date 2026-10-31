---
sidebar_position: 5
---

# Euler–Bernoulli beam

Verification of [`eulerBernoulliBeamScript`](../models/euler-bernoulli-beam) against closed-form solutions. All
results are from FEAScript-core 0.4.0 (RC).

## Cantilever beam

A cantilever of length $L = 4$, $EI = 10^5$, with a tip load $P = -1000$, on a single element.

![Cantilever beam of length 4 on one element, clamped at node 1, with a tip load at node 2](/assets/verification/cantilever-geometry.svg)

The exact tip deflection and rotation are

$$
w(L) = \frac{P L^3}{3 EI}, \qquad \theta(L) = \frac{P L^2}{2 EI},
$$

which the cubic Hermite element reproduces.

| Quantity            | Exact   | FEAScript | Difference |
| ------------------- | ------- | --------- | ---------- |
| Tip deflection w(L) | −0.2133 | −0.2133   | 2.8e-17    |
| Tip rotation θ(L)   | −0.0800 | −0.0800   | 4.2e-17    |
| Clamped end w(0)    | 0.0000  | 0.0000    | 2.4e-17    |
| Clamped end θ(0)    | 0.0000  | 0.0000    | 0          |

The differences are at the level of round-off in double precision, the number format of JavaScript.

The test requires each value to match within `1e-9`.

## Element stiffness matrix

The test also compares the assembled stiffness matrix of a single element, entry by entry, with the textbook
Hermite beam matrix, whose entries scale with $EI / L$, $EI / L^2$ and $EI / L^3$. It does this for two combinations of $EI$ and $L$, so
that both scalings are checked.

| $EI$              | $L$ | Largest entry ($4EI/L$) | Largest difference | Relative to largest entry |
| ----------------- | --- | ----------------------- | ------------------ | ------------------------- |
| $2 \times 10^6$   | 5   | 1,600,000               | 2.3e-10            | 1.5e-16                   |
| $7.5 \times 10^4$ | 2.5 | 120,000                 | 2.9e-11            | 2.4e-16                   |

The test requires every entry to match within `1e-6`:
[`eulerBernoulliBeam1DCantilever`](https://github.com/FEAScript/FEAScript-core/tree/main/tests/verification/analytical/eulerBernoulliBeam1DCantilever).
