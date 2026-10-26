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
          { href: "https://feascript.com", label: "Website", position: "right" },
          {
            type: "html",
            position: "right",
            value:
              '<a class="nav-icon" href="https://github.com/FEAScript/FEAScript-core" target="_blank" rel="noopener noreferrer" aria-label="FEAScript on GitHub" title="FEAScript on GitHub"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12"/></svg></a>',
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
              { label: "FEAScript Studio", href: "https://studio.feascript.com" },
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
