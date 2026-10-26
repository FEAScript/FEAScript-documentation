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
      label: "Models",
      items: ["models/heat-conduction"],
    },
  ],
};

export default sidebars;
