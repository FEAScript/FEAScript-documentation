---
sidebar_position: 1
---

# Verification overview

Verification checks that FEAScript solves its equations correctly: that the computed solution matches a known
answer for the same problem. Each case on these pages is an automated test in
[FEAScript-core](https://github.com/FEAScript/FEAScript-core/tree/main/tests), runs on every pull request, and
is linked from its section so you can read the exact setup and rerun it.

:::info Checked against

The results on these pages were produced with **FEAScript-core 0.4.0 (RC)**. The docs of earlier releases are
in the version dropdown.

:::

## Kinds of reference

| Kind       | Reference                                                                                       | Folder                          |
| ---------- | ----------------------------------------------------------------------------------------------- | ------------------------------- |
| Analytical | A closed-form solution of the same problem, often reproduced exactly by the elements            | `tests/verification/analytical` |
| Benchmark  | Published values of a standard problem (NAFEMS, Code_Aster validation manual), with convergence | `tests/verification/benchmark`  |

FEAScript-core also has regression tests (`tests/regression`). They compare against values that FEAScript itself
produced, so they guard against unintended changes, but they are not verification and are not listed here.

## Cases

| Model                | Case                                                                             | Reference            | Elements                     | Result                                                         |
| -------------------- | -------------------------------------------------------------------------------- | -------------------- | ---------------------------- | -------------------------------------------------------------- |
| Heat conduction      | [NAFEMS T4](heat-conduction#nafems-t4)                                           | NAFEMS, 18.3 °C      | Linear, quadratic quads      | 18.26 °C on a 12 × 20 quadratic mesh                           |
| Heat conduction      | [Code_Aster TPLP302](heat-conduction#code_aster-tplp302)                         | Fourier series       | Linear, quadratic quads      | Largest error 1.6e-4 °C on a 16 × 160 quadratic mesh           |
| Heat conduction      | [Code_Aster TPLP01](heat-conduction#code_aster-tplp01)                           | SFM/AFNOR VPCS guide | Quadratic triangles, quads   | Within 0.24 % at 12 of 13 points                               |
| Heat conduction      | [Spatially varying coefficients](heat-conduction#spatially-varying-coefficients) | Closed form          | Linear, quadratic            | Exact to round-off                                             |
| Creeping flow        | [Couette flow](creeping-flow#couette-flow)                                       | Closed form          | Q2-Q1 quads, P2-P1 triangles | Exact to round-off                                             |
| Front propagation    | [Planar front, 1D and 2D](front-propagation#planar-front)                        | Distance function    | Linear, quadratic            | 1.0e-2 to 7.1e-2 in a boundary layer, 2.4e-10 to 2.1e-6 inside |
| Euler–Bernoulli beam | [Cantilever](euler-bernoulli-beam#cantilever-beam)                               | Closed form          | Cubic Hermite                | Exact to round-off                                             |

## How results are reported

- Computed values are given to the decimals of the reference they are compared with, for example 3 decimals for the
  Code_Aster benchmarks. Where there is no published value to the same precision, they are given to 4 decimals.
- Errors, deviations and differences are given in scientific notation with 2 significant digits, for example
  1.6e-4. An exact zero is written as 0.
- Tolerances are written as in the test code, for example `5e-2`.
- Convergence orders are given to 2 decimals.

FEAScript computes in double precision, the number format of JavaScript, which carries about 16 significant
digits. Differences of order 1e-15 relative to the values compared are round-off: the result is exact for
that format.

## Running the tests

Every case runs with the rest of the test suite:

```bash
git clone https://github.com/FEAScript/FEAScript-core.git
cd FEAScript-core
npm install
npm test
```

Each test can also be run on its own, for example
`node tests/verification/benchmark/heatConduction2DNafemsT4/benchmark.test.js`. Each test folder has a README
with the problem setup, the expected values and the tolerances.
