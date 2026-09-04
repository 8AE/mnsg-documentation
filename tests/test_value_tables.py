"""Verify reviewed mappings survive generation without changing their raw values."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('generate_docs', ROOT/'scripts/generate_docs.py')
generator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(generator)


class ValueTableTests(unittest.TestCase):
    def record(self):
        return {'D_800C7AB2': {'tables': [{
            'id': 'room-ids', 'title': 'Room IDs',
            'description': 'Known room identifiers.',
            'columns': ['Raw value (hex)', 'Raw value (decimal)', 'Room'],
            'rows': [['`0x016`', '`22`', 'Congo fight']],
        }]}}

    def load(self, record):
        with tempfile.TemporaryDirectory() as temporary:
            data = Path(temporary)
            (data/'values-test.json').write_text(json.dumps(record))
            return generator.load_value_tables(data, {'D_800C7AB2': {'kind': 'variable'}})

    def test_rejects_disagreeing_numeric_values_and_malformed_tables(self):
        for mutation in ('decimal', 'row-width', 'duplicate-anchor', 'duplicate-row', 'unknown-symbol'):
            record = self.record()
            table = record['D_800C7AB2']['tables'][0]
            if mutation == 'decimal': table['rows'][0][1] = '`23`'
            if mutation == 'row-width': table['rows'][0].pop()
            if mutation == 'duplicate-anchor': record['D_800C7AB2']['tables'].append(table.copy())
            if mutation == 'duplicate-row': table['rows'].append(table['rows'][0].copy())
            if mutation == 'unknown-symbol': record['D_UNKNOWN'] = record.pop('D_800C7AB2')
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                self.load(record)

    def test_renders_stable_anchor_and_preserves_raw_values(self):
        record = self.load(self.record())['D_800C7AB2']
        output = generator.render_value_tables(record)
        self.assertIn('### Room IDs {#room-ids}', output)
        self.assertIn('| `0x016` | `22` | Congo fight |', output)
        self.assertIn('Congo fight', generator.value_search_text(record))

    def test_table_cells_escape_pipe_and_newlines(self):
        self.assertEqual(generator.table_cell('`mask | 1`\nmeaning'), '`mask \\| 1` meaning')

    def test_internal_evidence_is_never_loaded_as_public_values(self):
        with tempfile.TemporaryDirectory() as temporary:
            data = Path(temporary)
            (data/'value-evidence-test.json').write_text('{"internal": "source path"}')
            self.assertEqual(generator.load_value_tables(data), {})


if __name__ == '__main__':
    unittest.main()
