// @ts-check
import { themes as prismThemes } from "prism-react-renderer";
import remarkMath from "remark-math";
import rehypeKatex from "rehype-katex";

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: "FEAScript Documentation",
  tagline: "Finite element simulation library built in JavaScript",
  favicon: "img/favicon.ico",

  url: "https://doc.feascript.com",
  baseUrl: "/",

  organizationName: "FEAScript",
  projectName: "FEAScript-documentation",
  trailingSlash: false,

  onBrokenLinks: "throw",
  markdown: {
    hooks: {
      onBrokenMarkdownLinks: "throw",
    },
  },

  i18n: {
    defaultLocale: "en",
    locales: ["en"],
  },

  presets: [
    [
      "classic",
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          routeBasePath: "/",
          sidebarPath: "./sidebars.js",
          editUrl: "https://github.com/FEAScript/FEAScript-documentation/tree/main/",
          remarkPlugins: [remarkMath],
          rehypePlugins: [rehypeKatex],
          // "current" holds the unreleased docs; released versions are snapshots (see README)
          lastVersion: "current",
          versions: {
            current: { label: "Next (0.3.0-RC)" },
          },
        },
        blog: false,
        theme: {
          customCss: "./src/css/custom.css",
        },
      }),
    ],
  ],

  stylesheets: [
    {
      href: "https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css",
      type: "text/css",
      crossorigin: "anonymous",
    },
  ],

  themes: [
    [
      "@easyops-cn/docusaurus-search-local",
      /** @type {import("@easyops-cn/docusaurus-search-local").PluginOptions} */
      ({
        hashed: true,
        indexBlog: false,
        docsRouteBasePath: "/",
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      navbar: {
        title: "FEAScript",
        logo: { alt: "FEAScript Logo", src: "img/logo.svg" },
        items: [
          {
            type: "docSidebar",
            sidebarId: "docsSidebar",
            position: "left",
            label: "Docs",
          },
          { type: "docsVersionDropdown", position: "right" },
          { href: "https://feascript.com", label: "Website", position: "right" },
          {
            href: "https://github.com/FEAScript/FEAScript-core",
            label: "GitHub",
            position: "right",
          },
        ],
      },
      footer: {
        style: "light",
        links: [
          {
            title: "FEAScript",
            items: [
              { label: "Website", href: "https://feascript.com" },
              { label: "Studio", href: "https://studio.feascript.com" },
              { label: "Blog", href: "https://blog.feascript.com" },
            ],
          },
          {
            title: "Community",
            items: [
              { label: "GitHub", href: "https://github.com/FEAScript" },
              { label: "Contributing", href: "https://github.com/FEAScript/FEAScript-core/blob/main/CONTRIBUTING.md" },
            ],
          },
        ],
        copyright: `Documentation licensed under CC-BY 4.0. The FEAScript core library is MIT licensed.`,
      },
      prism: {
        theme: {
          ...prismThemes.github,
          plain: { ...prismThemes.github.plain, backgroundColor: "#eeeeff" },
        },
        darkTheme: {
          ...prismThemes.dracula,
          plain: { ...prismThemes.dracula.plain, backgroundColor: "#2c2c40" },
        },
        additionalLanguages: ["bash"],
      },
    }),
};

export default config;
