"""Native Docusaurus reference regressions; run npm run build before npm test."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("validate_site", ROOT / "scripts/validate_site.py")
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


class ValidatorTests(unittest.TestCase):
    def test_docusaurus_base_paths_and_clean_route_fragments(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            native = root / "functions/func_800240DC_24CDC"
            native.mkdir(parents=True)
            (root / "assets").mkdir()
            (root / "assets/style.css").write_text("")
            (root / "index.html").write_text('<main id="main"><a href="/mnsg-documentation/functions/func_800240DC_24CDC/#usage">Read a flag</a></main>')
            (native / "index.html").write_text('<link href="/mnsg-documentation/assets/style.css"><main id="usage"><a href="/mnsg-documentation/#main">Home</a></main>')
            pages = {p: validator.Page(p.read_text()) for p in root.rglob("*.html")}
            errors, count = validator.validate_links(root, pages)
            self.assertEqual(errors, [])
            self.assertEqual(count, 3)

    def test_missing_fragment_escape_localhost_and_wrong_base_are_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            index = root / "index.html"
            index.write_text('<a href="#absent">Bad</a><a href="../outside.html">Escape</a><a href="http://localhost:3000/">Local</a><a href="/functions/test/">Wrong base</a>')
            errors, _ = validator.validate_links(root, {index: validator.Page(index.read_text())})
            self.assertEqual(len(errors), 4)
            for expected in ("missing fragment", "development-only", "escapes", "base path"):
                self.assertTrue(any(expected in error for error in errors), errors)

    def test_project_names_provenance_and_specific_helpers_are_rejected(self):
        for forbidden in ("mnsg-extra-options", "Team Up", "Anchor", "Custom Fish", "the mod", "multiplayer", "extra_options_tick()", "s_anchor_state"):
            with self.subTest(forbidden=forbidden):
                self.assertTrue(validator.public_content_errors(forbidden, "native page"))
        self.assertEqual(validator.public_content_errors('Enable the native Boss Rush menu item. Include "modding.h" for RECOMP_HOOK. This pointer is used by the actor scheduler.', "native page"), [])
        self.assertTrue(validator.public_content_errors("## Used by\n", "native page"))

    def test_mod_repository_links_are_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            path = root / "index.html"
            path.write_text('<a href="https://github.com/8AE/mnsg-anchor/blob/main/src/main.c">Source</a>')
            errors, _ = validator.validate_links(root, {path: validator.Page(path.read_text())})
            self.assertEqual(len(errors), 1)
            self.assertIn("mod repository", errors[0])

    def test_native_article_text_and_code_survive_html_escaping(self):
        page = validator.Page('<nav>Elsewhere</nav><main><article><h1>Read a game flag</h1><pre><code>if (flag &lt; 2048 &amp;&amp; flag &gt; 0) read(flag);</code></pre></article></main>')
        self.assertNotIn("Elsewhere", page.body)
        self.assertIn("flag < 2048 && flag > 0", page.body)
        self.assertEqual(page.code_blocks, 1)

    def test_standalone_native_output_rejects_published_research_files(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            site, docs, data = root / "build", root / "docs", root / "data"
            name = "func_800240DC_24CDC"
            (site / "functions" / name).mkdir(parents=True)
            (docs / "functions").mkdir(parents=True)
            data.mkdir()
            symbol = {"name": name, "kind": "function"}
            (data / "inventory.json").write_text(json.dumps({"symbols": [symbol]}))
            description = "Reads a single bit from the native save-state bank. The caller supplies a bounded nonnegative index and treats any nonzero result as a set flag."
            markdown = f"{name}\n\n{description}\n\n## Signature\n\n```c\nextern int {name}(int flag);\n```\n\n## How it works\n\n{description}\n\n## Usage example\n\n```c\nint enabled = {name}(42);\n```\n"
            (docs / "functions" / f"{name}.md").write_text(markdown)
            (site / "functions" / name / "index.html").write_text(f'<main><article><h1>Read a flag</h1><p>{name} {description}</p><h2 id="how-it-works">How it works</h2><p>{description}</p><h2 id="usage-example">Usage example</h2><pre><code>{name}(42);</code></pre></article></main>')
            (site / "api-index.json").write_text(json.dumps([{**symbol, "title": "Read a flag", "summary": description, "url": f"/functions/{name}/"}]))
            clean = validator.validate_site(site, data, docs)
            self.assertTrue(clean["ok"], clean["errors"])
            (site / "source-snapshots.json").write_text("{}")
            leaked = validator.validate_site(site, data, docs)
            self.assertFalse(leaked["ok"])
            self.assertEqual(leaked["publicSourceFiles"], 1)
            self.assertTrue(any("Internal research" in error for error in leaked["errors"]))

    def test_markdown_frontmatter_does_not_count_as_native_prose(self):
        content = '---\nid: test\ntitle: Read a flag\n---\nThe native routine returns a bit mask.\n'
        self.assertEqual(validator.markdown_body(content), 'The native routine returns a bit mask.\n')


@unittest.skipUnless((ROOT / "build").is_dir(), "Run npm run build before Docusaurus site verification.")
class BuiltSiteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = validator.validate_site(ROOT / "build", ROOT / "data", ROOT / "docs")

    def test_every_native_route_link_fragment_and_standalone_page(self):
        self.assertTrue(self.report["ok"], "\n".join(self.report["errors"]))

    def test_header_enter_submission_uses_query_name_and_pages_base_path(self):
        home = validator.Page((ROOT / "build/index.html").read_text())
        actions = [link["url"] for link in home.links if link["tag"] == "form" and link["attribute"] == "action"]
        self.assertIn("/mnsg-documentation/reference/", actions)
        self.assertTrue(any(item.get("type") == "search" for item in home.search_inputs))

    def test_complete_native_catalog_and_search_without_public_source_data(self):
        inventory = json.loads((ROOT / "data/inventory.json").read_text())
        self.assertEqual(self.report["symbols"], len(inventory["symbols"]))
        self.assertEqual(self.report["functionPages"] + self.report["variablePages"], len(inventory["symbols"]))
        self.assertEqual(self.report["searchEntries"], len(inventory["symbols"]))
        self.assertEqual(self.report["publicSourceFiles"], 0)


if __name__ == "__main__":
    unittest.main()
