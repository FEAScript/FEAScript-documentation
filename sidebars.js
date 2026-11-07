// @ts-check

/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  docsSidebar: [
    "intro",
    {
      type: "category",
      label: "Getting Started",
      items: ["getting-started/installation", "getting-started/first-simulation"],
    },
    {
      type: "category",
      label: "Fundamentals",
      items: [
        "fundamentals/finite-element-method",
        "fundamentals/mesh",
        "fundamentals/boundary-conditions",
        "fundamentals/solvers",
      ],
    },
    {
      type: "category",
      label: "Models",
      items: [
        { type: "doc", id: "models/heat-conduction", className: "physics-item physics-heat-transfer" },
        { type: "doc", id: "models/general-form-pde", className: "physics-item physics-general-form-pde" },
        { type: "doc", id: "models/front-propagation", className: "physics-item physics-front-propagation" },
        { type: "doc", id: "models/creeping-flow", className: "physics-item physics-creeping-flow" },
        { type: "doc", id: "models/euler-bernoulli-beam", className: "physics-item physics-structural-mechanics" },
      ],
    },
    {
      type: "category",
      label: "Examples",
      items: [
        "examples/overview",
        "examples/heat-conduction",
        "examples/general-form-pde",
        "examples/front-propagation",
        "examples/creeping-flow",
        "examples/euler-bernoulli-beam",
      ],
    },
    {
      type: "category",
      label: "Verification",
      items: [
        "verification/overview",
        "verification/heat-conduction",
        "verification/creeping-flow",
        "verification/front-propagation",
        "verification/euler-bernoulli-beam",
      ],
    },
    {
      type: "category",
      label: "API Reference",
      items: [
        "api/feascript-model",
        "api/gmsh-import",
        "api/visualization",
        "api/web-worker",
        "api/utilities",
      ],
    },
  ],
};

export default sidebars;
