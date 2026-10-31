---
sidebar_position: 1
---

# Finite element method in FEAScript

This page summarizes how FEAScript discretizes a boundary value problem. It uses the notation of the
[Finite Element Method Notes](https://blog.feascript.com/tutorial/2023/12/01/finite-element-method-notes.html)
on the FEAScript blog, which explains each step in more detail.

## Galerkin residuals

Every model in FEAScript solves a boundary value problem of the form

$$
\begin{aligned}
Lu &= f \quad \text{in} \quad D, \\
Bu &= g \quad \text{on} \quad \partial D,
\end{aligned}
$$

where $L$ is the differential operator of the model, $B$ the boundary operator, $D$ the domain and
$\partial D$ its boundary. The solution is approximated with the basis functions $\phi^j$ of the mesh:

$$
u(\bar{x}) = \sum_{j=1}^{N} u_j \, \phi^j(\bar{x}),
$$

where $N$ is the number of mesh nodes and $u_j$ are the unknown nodal values. FEAScript uses the Galerkin
method: the weighting functions are the basis functions themselves, and the nodal values are those that zero
every residual

$$
R_i = \int_{D} (Lu - f) \, \phi^i \, dS = 0, \qquad i = 1, 2, \dots, N.
$$

Each model page lists the residual that FEAScript assembles for that model, after integration by parts.

## Linear and nonlinear systems

FEAScript always assembles a **Jacobian matrix** $\mathcal{J}$ and a **residual vector** $\bar{R}$, in both
linear and nonlinear models (the symbol $\mathcal{J}$ keeps the system matrix apart from the Jacobian
$\bar{\bar{J}}$ of the isoparametric mapping below):

- In a **linear** model, the residuals are linear in $u_j$. The Jacobian matrix is the classic stiffness
  (or conductivity) matrix, the residual vector is the load vector, and the system is solved once.
- In a **nonlinear** model, the system is solved with the Newton–Raphson method. At iteration $k$ the
  increment $\Delta \bar{u}$ is the solution of
  $$
  \mathcal{J}(\bar{u}^{k}) \, \Delta \bar{u} = \bar{R}(\bar{u}^{k}), \qquad
  \mathcal{J}_{ij} = -\frac{\partial R_i}{\partial u_j},
  $$
  and the solution is updated as $\bar{u}^{k+1} = \bar{u}^{k} + \Delta \bar{u}$. The iterations stop when the
  Euclidean norm $\lVert \Delta \bar{u} \rVert_2$ drops to the tolerance or below
  (see [Solvers](./solvers.md)).

## Boundary conditions

Boundary conditions enter the discrete system in two ways:

- **Dirichlet (essential) conditions** prescribe the value of the solution. At every node $n$ on a Dirichlet
  boundary, the Galerkin residual is replaced by $R_n = u_n - F(t_n)$: the row of the Jacobian matrix is
  cleared, its diagonal entry is set to one, and the residual entry is set to the prescribed value.
- **Neumann (natural) and Robin (mixed) conditions** enter through the boundary integral that appears after
  integration by parts. A zero Neumann condition needs no assembly at all: it is what a boundary without a
  Dirichlet or Robin condition gets.

See [Boundary conditions](./boundary-conditions.md) for the condition types of each model.

## Reference elements and isoparametric mapping

The basis functions are defined on reference elements $E_0$: the unit interval $0 \le \xi \le 1$ in 1D, the
unit square $0 \le \xi, \eta \le 1$ for quadrilaterals, and the triangle with vertices $(0, 0)$, $(0, 1)$ and
$(1, 0)$. Each element of the mesh is mapped to the reference element with the same basis functions
(isoparametric mapping):

$$
\bar{x} = \sum_{i=1}^{n_k} \bar{x}_i \, \phi_i(\bar{\xi}),
$$

where $\phi_i$ is the local basis function of node $i$ and $n_k$ is the number of nodes of the element. The
derivatives of the basis functions with respect to $x$ and $y$ are obtained from the Jacobian of the mapping,
and every element integral is computed on the reference element:

$$
I_{ij}^k = \int_{E_0} \phi_i(\bar{\xi}) \, L_{\bar{\xi}} \phi_j(\bar{\xi}) \, \det \bar{\bar{J}} \, d\bar{\xi}.
$$

![Reference elements of FEAScript with the local node numbering and the side numbering](/assets/reference-elements.svg)

The local node numbering above is the one used by the nodal numbering (NOP) array of every mesh, and the side
numbers are the ones stored in the boundary elements of the mesh (see [Mesh](./mesh.md)).

| Element                  | Nodes | Basis functions                                       |
| ------------------------ | ----- | ----------------------------------------------------- |
| 1D, linear               | 2     | Linear Lagrange                                       |
| 1D, quadratic            | 3     | Quadratic Lagrange                                    |
| Quadrilateral, linear    | 4     | Bilinear Lagrange                                     |
| Quadrilateral, quadratic | 9     | Biquadratic Lagrange                                  |
| Triangle, linear         | 3     | Linear (P1)                                           |
| Triangle, quadratic      | 6     | Quadratic (P2)                                        |
| 1D, cubic Hermite        | 2     | Cubic Hermite (used only by the Euler–Bernoulli beam) |

## Numerical integration

The integrals on the reference element are computed with Gauss quadrature:

$$
\int_{E_0} f(\bar{\xi}) \, d\bar{\xi} = \sum_{k=1}^{NGP} w_k \, f(\bar{\xi}_{gk}).
$$

The rule depends on the element type:

| Element                       | Integration rule                           |
| ----------------------------- | ------------------------------------------ |
| 1D / quadrilateral, linear    | 2-point Gauss rule per direction           |
| 1D / quadrilateral, quadratic | 3-point Gauss rule per direction           |
| Triangle, linear              | 3-point rule (exact up to degree 2)        |
| Triangle, quadratic           | 6-point rule (exact up to degree 4)        |
| 1D, cubic Hermite             | 6-point Gauss rule (exact up to degree 11) |

Quadrilateral rules are tensor products of the 1D rule (2 × 2 points for linear quadrilaterals, 3 × 3 for
quadratic ones), which integrate the stiffness and mass terms of undistorted elements exactly. Coefficients given as functions of position (for
example a thermal conductivity $k(x, y)$) are evaluated at these integration points.
