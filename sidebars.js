// @ts-check

/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  docsSidebar: [
    "intro",
    {
      type: "category",
      label: "Getting Started",
      items: [
        { type: "doc", id: "getting-started/installation", className: "logo-item topic-installation" },
        { type: "doc", id: "getting-started/first-simulation", className: "logo-item topic-first-simulation" },
      ],
    },
    {
      type: "category",
      label: "Fundamentals",
      items: [
        { type: "doc", id: "fundamentals/finite-element-method", className: "logo-item topic-finite-element" },
        { type: "doc", id: "fundamentals/mesh", className: "logo-item topic-mesh" },
        { type: "doc", id: "fundamentals/boundary-conditions", className: "logo-item topic-boundary-conditions" },
        { type: "doc", id: "fundamentals/solvers", className: "logo-item topic-solver" },
      ],
    },
    {
      type: "category",
      label: "Models",
      items: [
        { type: "doc", id: "models/heat-conduction", className: "logo-item physics-heat-transfer" },
        { type: "doc", id: "models/general-form-pde", className: "logo-item physics-general-form-pde" },
        { type: "doc", id: "models/front-propagation", className: "logo-item physics-front-propagation" },
        { type: "doc", id: "models/creeping-flow", className: "logo-item physics-creeping-flow" },
        { type: "doc", id: "models/euler-bernoulli-beam", className: "logo-item physics-structural-mechanics" },
      ],
    },
    {
      type: "category",
      label: "Examples",
      items: [
        { type: "doc", id: "examples/overview", className: "logo-item topic-examples" },
        { type: "doc", id: "examples/heat-conduction", className: "logo-item physics-heat-transfer" },
        { type: "doc", id: "examples/general-form-pde", className: "logo-item physics-general-form-pde" },
        { type: "doc", id: "examples/front-propagation", className: "logo-item physics-front-propagation" },
        { type: "doc", id: "examples/creeping-flow", className: "logo-item physics-creeping-flow" },
        { type: "doc", id: "examples/euler-bernoulli-beam", className: "logo-item physics-structural-mechanics" },
      ],
    },
    {
      type: "category",
      label: "Verification",
      items: [
        { type: "doc", id: "verification/overview", className: "logo-item topic-verification" },
        { type: "doc", id: "verification/heat-conduction", className: "logo-item physics-heat-transfer" },
        { type: "doc", id: "verification/creeping-flow", className: "logo-item physics-creeping-flow" },
        { type: "doc", id: "verification/front-propagation", className: "logo-item physics-front-propagation" },
        { type: "doc", id: "verification/euler-bernoulli-beam", className: "logo-item physics-structural-mechanics" },
      ],
    },
    {
      type: "category",
      label: "API Reference",
      items: [
        { type: "doc", id: "api/feascript-model", className: "logo-item topic-model" },
        { type: "doc", id: "api/gmsh-import", className: "logo-item topic-mesh-import" },
        { type: "doc", id: "api/mesh-generators", className: "logo-item topic-mesh" },
        { type: "doc", id: "api/visualization", className: "logo-item topic-visualization" },
        { type: "doc", id: "api/web-worker", className: "logo-item topic-web-worker" },
        { type: "doc", id: "api/utilities", className: "logo-item topic-utilities" },
      ],
    },
  ],
};

export default sidebars;
