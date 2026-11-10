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
          // Also gives the sitemap its <lastmod> dates
          showLastUpdateTime: true,
          // "current" holds the docs of the latest minor version; older minor versions are snapshots (see README)
          lastVersion: "current",
          versions: {
            current: { label: "0.4.0 (RC)" },
            "0.3.1": { label: "0.3.1" },
            "0.2.0": { label: "0.2.0", banner: "unmaintained" },
          },
        },
        blog: false,
        // <lastmod> comes from each page's last git commit (showLastUpdateTime in docs), so the deploy workflow
        // checks out the full history. The search page is left out of the sitemap
        sitemap: {
          lastmod: "date",
          ignorePatterns: ["/search"],
        },
        theme: {
          customCss: "./src/css/custom.css",
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

  // Cloudflare Web Analytics (no cookies); it follows client-side page changes on its own
  scripts: [
    {
      src: "https://static.cloudflareinsights.com/beacon.min.js",
      defer: true,
      "data-cf-beacon": '{"token": "491db947f23147048bcc5e6c1521834a"}',
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
            title: "Learn",
            items: [
              { label: "Tutorials", icon: "tutorials", href: "https://feascript.com/#tutorials" },
              { label: "CodePen", icon: "codepen", href: "https://codepen.io/FEAScript" },
              {
                label: "Scribbler",
                icon: "scribbler",
                href: "https://hub.scribbler.live/portfolio/#!nikoscham/FEAScript-Scribbler-examples",
              },
              { label: "Documentation", icon: "documentation", href: "https://docs.feascript.com" },
            ],
          },
          {
            title: "Build",
            items: [
              { label: "FEAScript Studio", icon: "studio", href: "https://feascript.com/studio.html" },
              { label: "Tri's Lab", icon: "tris-lab", href: "https://lab.feascript.com/" },
              { label: "npm package", icon: "npm", href: "https://www.npmjs.com/package/feascript" },
              { label: "GitHub", icon: "github", href: "https://github.com/FEAScript/FEAScript-core" },
            ],
          },
          {
            title: "Community",
            items: [
              { label: "Blog", icon: "blog", href: "https://blog.feascript.com" },
              { label: "Discord", icon: "discord", href: "https://discord.gg/3DVjNcuW4f" },
              { label: "Support", icon: "support", href: "https://github.com/FEAScript/FEAScript-core/issues" },
              { label: "Sponsors", icon: "sponsors", href: "https://feascript.com/sponsors.html" },
            ],
          },
        ],
        copyright: `<span>&#169; 2024-${new Date().getFullYear()} FEAScript &middot; <a href="https://feascript.com/privacy.html">Privacy</a> &middot; <span data-icon="no-cookies">This site uses no cookies</span></span><span>Core: MIT license &middot; Docs: CC BY 4.0</span>`,
      },
      prism: {
        theme: darkCode,
        darkTheme: darkCode,
        additionalLanguages: ["bash"],
      },
    }),
};

export default config;
