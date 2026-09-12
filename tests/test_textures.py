"""Texture provenance and native-symbol mapping regressions; no ROM required."""
import json
from pathlib import Path
import struct
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from native_inventory import load_inventory


class TextureTests(unittest.TestCase):
    def test_every_saved_image_is_an_original_sheet_or_verified_crop(self):
        catalog = json.loads((ROOT / 'data/textures.json').read_text())
        rows = catalog['resources'] + catalog['icons']
        images = {row['image'] for row in rows}
        saved = {'/' + str(p.relative_to(ROOT / 'static')) for p in (ROOT / 'static/img/textures').glob('*.png')}
        self.assertEqual(images, saved)
        self.assertNotIn('references', catalog)
        for row in rows:
            with self.subTest(image=row['image']):
                png = (ROOT / 'static' / row['image'].lstrip('/')).read_bytes()
                self.assertEqual(png[:8], b'\x89PNG\r\n\x1a\n')
                self.assertEqual(struct.unpack('>II', png[16:24]), (row['width'], row['height']))

    def test_texture_variables_match_reviewed_recomp_entries(self):
        catalog = json.loads((ROOT / 'data/textures.json').read_text())
        evidence = json.loads((ROOT / 'data/value-evidence-notification-icons.json').read_text())
        matches = {m['resource']: m for m in evidence['symbolTable']['matches']}
        known = {s['name']: s for s in load_inventory(ROOT / 'data')['symbols']}
        for row in catalog['resources']:
            if row.get('nativeSymbol'):
                match = matches[row['id']]
                self.assertEqual(row['nativeSymbol'], match['symbol'])
                self.assertEqual(row['nativeHandle'], match['address'])
                self.assertEqual(known[row['nativeSymbol']]['address'], row['nativeHandle'])
                self.assertIsNone(known[row['nativeSymbol']]['romAddress'])
        flute = next(r for r in catalog['resources'] if r['id'] == '0x8016')
        dolls = next(r for r in catalog['resources'] if r['id'] == '0x800E')
        self.assertEqual(flute['nativeSymbol'], 'D_80217FAC_676F5C')
        self.assertEqual(dolls['nativeSymbol'], 'D_80217F94_676F44')
        self.assertNotEqual(flute['nativeHandle'], flute['romAddress'])

    def test_crops_link_to_their_texture_variable_and_fit_the_sheet(self):
        catalog = json.loads((ROOT / 'data/textures.json').read_text())
        sheets = {r['id']: r for r in catalog['resources']}
        for crop in catalog['icons']:
            sheet = sheets[crop['resource']]
            self.assertEqual(crop.get('nativeSymbol'), sheet.get('nativeSymbol'))
            self.assertEqual(crop['romAddress'], sheet['romAddress'])
            self.assertLessEqual(crop['x'] + crop['width'], sheet['width'])
            self.assertLessEqual(crop['y'] + crop['height'], sheet['height'])
            for symbol in crop['symbols']:
                self.assertIn(crop['image'], (ROOT / 'docs/variables' / f'{symbol}.md').read_text())

    def test_supplemental_inventory_does_not_silently_override_scanned_symbols(self):
        with tempfile.TemporaryDirectory() as directory:
            directory = Path(directory)
            symbol = {'name': 'D_80217FAC_676F5C', 'kind': 'variable', 'address': '0x80217FAC'}
            (directory / 'inventory.json').write_text(json.dumps({'symbols': [symbol]}))
            (directory / 'inventory-native-test.json').write_text(json.dumps({'symbols': [symbol]}))
            with self.assertRaisesRegex(ValueError, 'Duplicate'):
                load_inventory(directory)
