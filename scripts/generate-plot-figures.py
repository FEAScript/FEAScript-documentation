"""Generate the log-log plots of the documentation: convergence, comparison with Elmer and solver times.

The plots follow the style of the other figures in static/assets (see scripts/figure_style.py). Their values are
those of the tables next to each plot in the docs; update both together:

    python3 scripts/generate-plot-figures.py
"""

import os

from figure_style import *  # noqa: F401,F403 (shared drawing helpers)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "static", "assets")

H = f"Element size {italic('h')} (m)"

FIGURES = {
    # docs/verification/heat-conduction.mdx, NAFEMS T4
    "verification/nafems-t4-convergence": log_plot(
        [
            ("Linear", [(0.2, 9.754), (0.1, 0.2998), (0.05, 0.161), (0.025, 0.04011), (0.0125, 0.009997)]),
            ("Quadratic", [(0.2, 3.269), (0.1, 0.1446), (0.05, 0.002085), (0.025, 0.0001002)]),
        ],
        H,
        f"|{italic('T')}(E) − 18.2538| (°C)",
        "NAFEMS T4: error at point E",
    ),
    # docs/verification/heat-conduction.mdx, Code_Aster TPLP302
    "verification/tplp302-convergence": log_plot(
        [
            ("Linear", [(0.05, 6.893), (0.025, 1.629), (0.0125, 0.3514), (0.00625, 0.08533)]),
            ("Quadratic", [(0.05, 0.6381), (0.025, 0.01277), (0.0125, 0.0001638), (0.00625, 0.00000994)]),
        ],
        H,
        "Largest error (°C)",
        "Code_Aster TPLP302: largest error at the seven reference points",
    ),
    # docs/examples/creeping-flow.mdx, comparison with Elmer
    "examples/cavity-elmer-comparison": log_plot(
        [
            ("Velocity", [(1 / 8, 0.08007), (1 / 16, 0.01158), (1 / 24, 0.005279), (1 / 32, 0.001053), (1 / 48, 0.0001008), (1 / 64, 0.00004933)]),
            (f"{italic('ψ')}{sub('min')}", [(1 / 8, 0.0001202), (1 / 16, 0.0000364), (1 / 24, 0.00001865), (1 / 32, 0.000009628), (1 / 48, 0.000003159), (1 / 64, 0.000001252)]),
        ],
        f"Element size {italic('h')}",
        "Difference",
        "Lid-driven cavity: difference between FEAScript and Elmer",
    ),
    # docs/examples/heat-conduction.md, fin in 2D, comparison with Elmer
    "examples/fin-elmer-comparison": log_plot(
        [
            ("Linear", [(0.2, 1.0230), (0.1, 0.57365), (0.05, 0.30669), (0.025, 0.15922), (0.0125, 0.081244)]),
            ("Quadratic", [(0.4, 0.79974), (0.2, 0.39427), (0.1, 0.19570), (0.05, 0.097499), (0.025, 0.048665)]),
        ],
        H,
        "Largest error (°C)",
        "Fin in 2D: largest error against the exact solution",
    ),
    # docs/fundamentals/solvers.mdx, performance
    "solver-performance": log_plot(
        [
            ('"frontal"', [(231, 0.022), (861, 0.09407), (3321, 0.1284), (13041, 0.3676), (51681, 2.396)]),
            ('"lusolve"', [(231, 0.05207), (861, 0.1038), (3321, 0.1955), (13041, 0.5122), (51681, 1.959)]),
            ('"jacobi"', [(231, 0.01563), (861, 0.06255), (3321, 0.4542)]),  # Does not converge with its defaults on larger meshes
        ],
        "Number of nodes",
        "Time (s)",
        "Fin in 2D: assembly and solve time",
    ),
    "solver-memory": log_plot(
        [
            ('"frontal"', [(231, 61.2), (861, 69.3), (3321, 70.8), (13041, 96.4), (51681, 254.6)]),
            ('"lusolve"', [(231, 65.2), (861, 66.8), (3321, 82.6), (13041, 140.1), (51681, 347.4)]),
            ('"jacobi"', [(231, 57.8), (861, 63.2), (3321, 64.6)]),
        ],
        "Number of nodes",
        "Peak memory (MB)",
        "Fin in 2D: peak memory",
    ),
}

if __name__ == "__main__":
    for name, content in FIGURES.items():
        with open(os.path.join(ASSETS, f"{name}.svg"), "w") as handle:
            handle.write(content)
        print(f"Wrote static/assets/{name}.svg")
