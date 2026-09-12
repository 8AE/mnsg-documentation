"""Combine source-usage inventory with explicitly reviewed native-only symbols."""
import json
from pathlib import Path


def load_inventory(data_dir):
    data_dir = Path(data_dir)
    inventory = json.loads((data_dir / 'inventory.json').read_text())
    known = {row['name'] for row in inventory['symbols']}
    for path in sorted(data_dir.glob('inventory-native-*.json')):
        for row in json.loads(path.read_text())['symbols']:
            if row['name'] in known:
                raise ValueError(f'Duplicate native inventory symbol: {row["name"]}')
            if row['kind'] not in ('function', 'variable') or not row.get('address'):
                raise ValueError(f'Invalid native inventory symbol: {row["name"]}')
            known.add(row['name'])
            inventory['symbols'].append(row)
    return inventory
