"""Scanner regressions: source semantics that simple grep misses."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

SPEC = importlib.util.spec_from_file_location("scan_symbols", Path(__file__).resolve().parents[1] / "scripts/scan_symbols.py")
scanner = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(scanner)


class ReferenceTests(unittest.TestCase):
    def refs(self, text, known=()):
        refs, declarations, errors = scanner.extract_references(text, set(known))
        return {(r["name"], r["line"], r["role"]) for r in refs}, declarations, errors

    def test_comments_and_log_strings_are_not_usage(self):
        text = '''// func_80000001_1001();
/* D_80000002 = 0; */
const char *message = "func_80000003_1003 D_80000004";
func_80000005_1005(); // D_80000006
'''
        refs, _, _ = self.refs(text)
        self.assertEqual(refs, {("func_80000005_1005", 4, "called")})

    def test_multiline_extern_and_function_pointer_argument(self):
        text = '''extern void *func_80034E08_35A08(
    void *list, void (*callback)(void *, void *),
    short kind);
extern unsigned short D_800C7AB2;
void run(void) {
    func_80034E08_35A08(0, callback, 8);
    short room = D_800C7AB2;
}
'''
        refs, declarations, errors = self.refs(text)
        self.assertEqual(len(declarations), 2)
        self.assertIn("void (*callback)(void *, void *)", declarations[0]["text"])
        self.assertIn(("func_80034E08_35A08", 1, "declared"), refs)
        self.assertIn(("func_80034E08_35A08", 6, "called"), refs)
        self.assertIn(("D_800C7AB2", 7, "referenced"), refs)
        self.assertEqual(errors, [])

    def test_direct_entry_return_hooks_and_patch(self):
        text = '''RECOMP_HOOK("func_80002040_2C40")
void before(void) {}
RECOMP_HOOK_RETURN("func_80002040_2C40")
void after(void) {}
RECOMP_PATCH void *func_80035EEC_36AEC(void *task, short kind) {
    return func_80035D8C_3698C(kind);
}
'''
        refs, declarations, errors = self.refs(text)
        self.assertIn(("func_80002040_2C40", 1, "hook"), refs)
        self.assertIn(("func_80002040_2C40", 3, "hook-return"), refs)
        self.assertIn(("func_80035EEC_36AEC", 5, "patched"), refs)
        self.assertNotIn(("func_80035EEC_36AEC", 5, "called"), refs)
        self.assertEqual(declarations[0]["text"], "RECOMP_PATCH void *func_80035EEC_36AEC(void *task, short kind);")
        self.assertEqual(errors, [])

    def test_macro_hooks_preserve_real_invocation_line(self):
        text = '''#define TRACK_CONGO_PART(function, part) \\
    RECOMP_HOOK_RETURN(function) \\
    void track_##part(void) { record(part); }
TRACK_CONGO_PART("func_080066B0_6B9950", 0)
TRACK_CONGO_PART("func_080068B8_6B9B58", 1)
'''
        refs, _, errors = self.refs(text)
        self.assertEqual(refs, {("func_080066B0_6B9950", 4, "hook-return"),
                                ("func_080068B8_6B9B58", 5, "hook-return")})
        self.assertEqual(errors, [])

    def test_nested_wrapper_and_unknown_target_audit(self):
        text = '''#define ENTER(target) RECOMP_HOOK(target)
#define TRACK(target, id) ENTER(target)
TRACK("func_80002040_2C40", 1)
RECOMP_HOOK(UNRESOLVED_TARGET)
'''
        refs, _, errors = self.refs(text)
        self.assertEqual(refs, {("func_80002040_2C40", 3, "hook")})
        self.assertEqual(errors, [{"line": 4, "expression": "UNRESOLVED_TARGET"}])

    def test_sdk_names_only_if_symbol_table_known(self):
        refs, _, _ = self.refs("osGetCount(); recomp_printf(\"hello\"); local_helper();", {"osGetCount"})
        self.assertEqual(refs, {("osGetCount", 1, "called")})

    def test_callback_reference_is_not_a_call(self):
        refs, _, _ = self.refs("register_callback(func_80002040_2C40);\n")
        self.assertEqual(refs, {("func_80002040_2C40", 1, "referenced")})

    def test_short_hook_context_is_complete(self):
        text = '\n'.join(['// documentation', 'RECOMP_HOOK("func_80002040_2C40")', 'void hook(void) {'] + ['    tick();'] * 12 + ['}'])
        snippet, start_line = scanner.source_context(text, 2, "hook")
        self.assertEqual(start_line, 1)
        self.assertTrue(snippet.endswith("}"))


class InventoryTests(unittest.TestCase):
    def fixture(self, root, project, address="0x80002040"):
        repo = root / project
        (repo / "src").mkdir(parents=True)
        (repo / "include").mkdir()
        (repo / "Goemon64RecompSyms").mkdir()
        (repo / "Goemon64RecompSyms/mnsg.syms.toml").write_text(f'''[[section]]
name = ".main"
vram = 0x80000400
rom = 0x1000
functions = [
  {{ name = "func_80002040_2C40", vram = {address}, size = 0x40 }},
  {{ name = "FrameDispatcher", vram = {address}, size = 0x40 }},
]
''')
        (repo / "Goemon64RecompSyms/mnsg.datasyms.toml").write_text('''[[section]]
name = ".bss"
vram = 0x800C0000
symbols = [{ name = "D_800C7AB2", vram = 0x800C7AB2 }]
''')
        (repo / "src/main.c").write_text('''extern unsigned short D_800C7AB2;
RECOMP_HOOK_RETURN("func_80002040_2C40")
void hook(void) { sink(D_800C7AB2); func_800FFFFF_FFFFF(); }
''')
        (repo / "include/recompui.h").write_text('extern int D_800FFFF0;')
        return repo

    def test_alias_size_missing_metadata_and_sdk_exclusion(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.fixture(root, "one")
            inventory = scanner.scan(root, ["one"])
            symbols = {s["name"]: s for s in inventory["symbols"]}
            self.assertEqual(set(symbols), {"D_800C7AB2", "func_80002040_2C40", "func_800FFFFF_FFFFF"})
            self.assertEqual(symbols["func_80002040_2C40"]["aliases"], ["FrameDispatcher"])
            self.assertEqual(symbols["func_80002040_2C40"]["romAddress"], "0x00002C40")
            self.assertIsNone(symbols["D_800C7AB2"]["size"])
            self.assertIsNone(symbols["D_800C7AB2"]["romAddress"])
            self.assertIsNone(symbols["func_800FFFFF_FFFFF"]["address"])
            self.assertEqual(inventory["audit"]["unresolvedSymbols"][0]["name"], "func_800FFFFF_FFFFF")

    def test_conflicting_tables_are_preserved(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.fixture(root, "one")
            self.fixture(root, "two", "0x80002044")
            inventory = scanner.scan(root, ["one", "two"])
            function = next(s for s in inventory["symbols"] if s["name"] == "func_80002040_2C40")
            self.assertEqual(len(function["variants"]), 2)
            self.assertEqual(len(function["symbolSources"]), 2)
            self.assertTrue(any(c["field"] == "address" for c in function["conflicts"]))


if __name__ == "__main__":
    unittest.main()
