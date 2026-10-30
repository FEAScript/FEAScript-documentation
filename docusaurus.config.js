// @ts-check
import { themes as prismThemes } from "prism-react-renderer";
import remarkMath from "remark-math";
import rehypeKatex from "rehype-katex";

// Code blocks are dark in both modes, like the terminal snippets on feascript.com
const darkCode = {
  ...prismThemes.dracula,
  plain: { ...prismThemes.dracula.plain, backgroundColor: "#1f1f1f" },
};

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: "FEAScript Documentation",
  tagline: "Finite element simulation library built in JavaScript",
  favicon: "img/favicon.ico",

  url: "https://docs.feascript.com",
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
            current: { label: "0.3.1" },
          },
        },
        blog: false,
        theme: {
          customCss: "./src/css/custom.css",
        },
        // Same GA4 property as feascript.com, the blog and Studio
        gtag: {
          trackingID: "G-1JPK0KLEC9",
          anonymizeIP: true,
        },
      }),
    ],
  ],

  headTags: [
    { tagName: "link", attributes: { rel: "preconnect", href: "https://fonts.googleapis.com" } },
    {
      tagName: "link",
      attributes: { rel: "preconnect", href: "https://fonts.gstatic.com", crossorigin: "anonymous" },
    },
  ],

  stylesheets: [
    {
      href: "https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@400&family=Roboto:wght@300;400;500;700&display=swap",
      type: "text/css",
    },
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
        items: [
          { type: "docsVersionDropdown", position: "right" },
          {
            type: "custom-github",
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
              { label: "FEAScript Studio", href: "https://feascript.com/studio.html" },
              { label: "Blog", href: "https://blog.feascript.com" },
            ],
          },
          {
            title: "Community",
            items: [
              { label: "Discord", href: "https://discord.gg/3DVjNcuW4f" },
              { label: "GitHub", href: "https://github.com/FEAScript/FEAScript-core" },
              { label: "YouTube", href: "https://www.youtube.com/@FEAScript" },
              { label: "LinkedIn", href: "https://www.linkedin.com/company/feascript/" },
            ],
          },
        ],
        copyright: `<span>&#169; 2023-${new Date().getFullYear()} FEAScript</span><span>Core: MIT license &middot; Docs: CC BY 4.0</span>`,
      },
      prism: {
        theme: darkCode,
        darkTheme: darkCode,
        additionalLanguages: ["bash"],
      },
    }),
};

export default config;
