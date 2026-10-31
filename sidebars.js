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
        "models/heat-conduction",
        "models/general-form-pde",
        "models/front-propagation",
        "models/creeping-flow",
        "models/euler-bernoulli-beam",
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
