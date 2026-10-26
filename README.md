<img src="https://feascript.github.io/FEAScript-website/assets/feascript-logo.png" width="80" alt="FEAScript Logo">

# FEAScript-documentation

User & developer documentation for the FEAScript project, published at **https://doc.feascript.com**. Built with [Docusaurus](https://docusaurus.io/) (Node.js >= 20).

## Local development

```bash
npm install
npm start        # dev server with live reload
npm run build    # production build into ./build
npm run serve    # serve the production build locally
```

## Writing docs

- Pages are Markdown/MDX files under `docs/`; the sidebar is defined in `sidebars.js`.
- Math is supported with KaTeX: inline `$T$` and block `$$ ... $$`.
- `docs/` always holds the **unreleased** docs ("Next" in the version dropdown).

## Versioning

When a new FEAScript-core version is released, snapshot the current docs:

```bash
npm run version -- 0.3.0
```

This copies `docs/` to `versioned_docs/version-0.3.0/`, the sidebar to `versioned_sidebars/`, and records the version in `versions.json`. Released docs are then available at `doc.feascript.com/0.3.0/...` and appear in the version dropdown.

After the first release, edit `docusaurus.config.js`: remove `lastVersion: "current"` so the newest released version becomes the default (unversioned URLs). Fixes to an old version are made directly in its `versioned_docs/version-x.y.z/` folder.

## Deployment

Pushing to `main` triggers [`.github/workflows/deploy.yml`](.github/workflows/deploy.yml), which builds the site and deploys it to `doc.feascript.com`

## License

The content of the FEAScript documentation is licensed under <a href="https://github.com/FEAScript/FEAScript-documentation/blob/main/LICENSE" target="_blank">CC-BY 4.0</a>. Note that the core library of FEAScript is distributed under the terms of the <a href="https://github.com/FEAScript/FEAScript-core/blob/main/LICENSE" target="_blank">MIT license</a>.
