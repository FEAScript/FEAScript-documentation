---
sidebar_position: 1
---

# Verification overview

<img className="topic-logo" src="/assets/topics/verification.svg" alt="" />

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

## Comparison with Elmer

Two examples are also solved with [Elmer](https://www.elmerfem.org/), the open-source finite element software of
CSC – IT Center for Science, on the same meshes, and the two programs are compared node by node: the
[fin in 2D](../examples/heat-conduction#comparison-with-elmer), which also has an exact solution, and the
[lid-driven cavity](../examples/creeping-flow#comparison-with-elmer), which has none. These comparisons are not
part of the test suite; they are run with
[FEAScript-benchmark](https://github.com/FEAScript/FEAScript-benchmark), which also times both programs (see
[Solvers](../fundamentals/solvers#performance)).

## Comparison with scikit-fem

The same two examples are also solved with [scikit-fem](https://github.com/kinnala/scikit-fem), an open-source finite element library
for Python, on the same meshes. FEAScript and scikit-fem agree to within 1.7e-10 °C on the
[fin in 2D](../examples/heat-conduction#comparison-with-scikit-fem), and to within 4.0e-13 in velocity and 2.2e-10 in
pressure on the [lid-driven cavity](../examples/creeping-flow#comparison-with-scikit-fem), lid corners included.
They also agree on [unstructured Gmsh meshes](../examples/heat-conduction#comparison-on-unstructured-meshes).

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
  Code_Aster benchmarks. Otherwise they are given to enough digits to show the differences listed next to them, and
  in full where the result is exact to round-off.
- Exact values are written exactly, for example $-16/75$, $-0.08$ or 0, never padded with zeros such as
  −0.0800.
- Errors, deviations and differences are given in scientific notation with 2 significant digits, for example
  1.6e-4. An exact zero is written as 0. Relative errors are not given for quantities whose exact value is 0.
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
