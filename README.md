# Mystical Ninja Starring Goemon Recompiled

A **Docusaurus 3** mod development reference for native Mystical Ninja Starring Goemon Recompiled functions and variables. The public site documents API behavior, C interfaces, usage examples, and related native symbols. The game project is [Goemon64Recomp](https://github.com/klorfmorf/Goemon64Recomp).

[Open the documentation](https://8ae.github.io/mnsg-documentation/)

## Develop and build

Requires Node.js 20+ and Python 3.11+. GitHub Actions uses Node.js 24 and Python 3.14.

```sh
npm ci
npm start
```

Create and validate the production site:

```sh
npm run build
npm test
npm run serve -- --host 127.0.0.1 --port 8765
```

The Docusaurus output is `build/`, served under `/mnsg-documentation/`. `npm run build` first generates the API Markdown and local search index. Docusaurus supplies the document layout, sidebar, table of contents, navigation, syntax highlighting, copy buttons, theme switching, static rendering, and GitHub Pages output. A custom React search component supports exact symbol names, addresses, and semantic descriptions without an external search service.

## Public documentation

- `docs/getting-started.md` and `docs/native-lifecycle.md`: introductory guides.
- `docs/functions/` and `docs/variables/`: generated native API Markdown.
- `data/reference-*.json`: public explanations and complete C usage examples.
- `data/values-*.json`: reviewed raw-value mappings, field layouts, and decoded meanings for variable pages. Each symbol supplies `tables` with a stable `id`, `title`, `description`, `columns`, and `rows`. Label array indices, stored values, offsets, and flag masks explicitly. Include hexadecimal and decimal columns for known numeric identifiers.
- `scripts/generate_docs.py`: merges public reference entries and symbol metadata.
- `src/pages/`: homepage and searchable symbol explorer.
- `src/theme/SearchBar/`: local navbar search.
- `src/css/custom.css`: Docusaurus theme customization.

Edit the public `reference-*.json` records to improve a generated page. Each record supplies `title`, `summary`, `behavior`, `example`, and optionally `declaration`, `parameters`, `returns`, `cautions`, `exampleExplanation`, `decompilation`, `decompilationNote`, and `related`. Examples should contain their declarations and a complete C helper or observation hook. Uncertain native behavior must remain explicit.

Value tables appear on their variable pages and contribute their interpreted names to search. The generator rejects malformed rows, duplicate anchors, and mismatched hexadecimal/decimal values; site validation checks each rendered row and table anchor. Keep source locations, conflicts, and research decisions in `data/value-evidence-*.json`, which is excluded from public output.

The public site intentionally has no project-specific sections, source excerpts, project names, or links to the source projects. The generator only publishes native API text and selected symbol metadata. Maintenance provenance is never copied into `static/` or `build/`. That research remains available in this public repository for review.

## Refresh the internal inventory

The initial inventory contains **167 symbols: 135 functions and 32 variables**, with 677 reference locations. It covers the native symbols used by the five source projects, not every unused symbol in the game tables.

Keep these checkouts alongside this repository: `mnsg-custom-fish`, `mnsg-enable-boss-rush`, `mnsg-extra-options`, `mnsg-recomp-example`, and `mnsg-team-up`.

```sh
python3 scripts/scan_symbols.py --workspace ..
npm run build
npm test
```

The scanner reads each project's `Goemon64RecompSyms/mnsg*.syms.toml` and `mnsg*.datasyms.toml`, and scans mod-owned `src` and `include` files. It captures native declarations, calls, function-pointer references, hooks, return hooks, patches, and supported macro-generated hooks. Comments, unrelated string literals, SDK headers, and vendored code are excluded as usage. This is a lexical scanner, not a compiler: conditional source branches remain in the inventory, and complex macro changes require audit review.

`data/inventory.json`, `data/source-snapshots.json`, and `data/annotations-*.json` retain the research trail for maintainers. Source snapshots include exact files and SHA-256 hashes; native descriptions can therefore be checked against local changes as well as committed code. Rebuilds use captured data and do not require sibling checkouts or a game ROM. New native symbols must receive a public reference record before the build can pass.

## Validation and publication

The scanner has regression tests for declarations, comments, function-pointer references, direct and macro-generated hooks, patches, table aliases, and conflicts. Site validation checks native page and search coverage, C examples, generated links and anchors, and absence of project references or provenance data in public output. C example syntax checks and browser interaction checks are separate from native game-runtime testing.

`.github/workflows/pages.yml` builds and tests pushes and pull requests. Pushes to `main` and manual runs publish the Docusaurus `build/` artifact; pull requests only validate. Set **Settings → Pages → Source** to **GitHub Actions**.

The deployment follows the [Docusaurus GitHub Pages guide](https://docusaurus.io/docs/deployment#deploying-to-github-pages) and [GitHub's Pages workflow documentation](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages).
