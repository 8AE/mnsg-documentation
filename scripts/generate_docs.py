#!/usr/bin/env python3
"""Generate clean Docusaurus API pages; internal research never enters the site."""
from __future__ import annotations
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN = re.compile(r'mnsg-(?:custom-fish|enable-boss-rush|extra-options|recomp-example|team-up|anchor)|\b(?:Extra Options|Team Up|Custom Fish|Anchor|multiplayer)\b', re.I)

def load_reference():
    result={};rank={'decompiled':3,'source-reviewed':2,'inferred':1}
    for file in sorted((ROOT/'data').glob('reference-*.json')):
        for name,incoming in json.loads(file.read_text()).items():
            if name not in result:result[name]=incoming;continue
            existing=result[name]
            primary,secondary=(incoming,existing) if rank.get(incoming.get('confidence'),0)>rank.get(existing.get('confidence'),0) else (existing,incoming)
            combined={**secondary,**primary}
            for key in ('behavior','cautions','related'):
                combined[key]=[]
                for item in primary.get(key,[])+secondary.get(key,[]):
                    if item not in combined[key]:combined[key].append(item)
            result[name]=combined
    core=ROOT/'data/reference-core.json'
    if core.exists():result.update(json.loads(core.read_text()))
    return result

def frontmatter(data):
    return '---\n'+'\n'.join(f'{key}: {json.dumps(value,ensure_ascii=False)}' for key,value in data.items())+'\n---\n\n'

def code(value):
    return '\n```c\n'+'\n'.join(line.rstrip() for line in value.strip().splitlines())+'\n```\n'

def table_cell(value):
    return str(value).replace('|','\\|').replace('\n',' ')

def load_value_tables(data_dir=None, known=None):
    """Read reviewed public mappings separately from internal research evidence."""
    result = {}
    for path in sorted((data_dir or ROOT/'data').glob('values-*.json')):
        records = json.loads(path.read_text())
        if not isinstance(records, dict):
            raise ValueError(f'{path.name}: expected a symbol mapping')
        for name, record in records.items():
            if name in result:
                raise ValueError(f'{name}: duplicate value-table record')
            if known is not None and (name not in known or known[name]['kind'] != 'variable'):
                raise ValueError(f'{name}: value tables require an inventoried variable')
            if not isinstance(record, dict) or not isinstance(record.get('tables'), list) or not record['tables']:
                raise ValueError(f'{name}: expected nonempty tables')
            ids = {'known-values','signature','how-it-works','usage-example','notes','related-symbols'}
            for table in record['tables']:
                if not isinstance(table, dict):
                    raise ValueError(f'{name}: expected a table object')
                label = f'{name}/{table.get("id", "unnamed")}'
                for key in ('id','title','description'):
                    if not isinstance(table.get(key), str) or not table[key].strip():
                        raise ValueError(f'{label}: missing {key}')
                if not re.fullmatch(r'[a-z][a-z0-9-]*', table['id']) or table['id'] in ids:
                    raise ValueError(f'{label}: invalid or duplicate table anchor')
                ids.add(table['id'])
                columns, rows = table.get('columns'), table.get('rows')
                if not isinstance(columns, list) or len(columns) < 2 or not all(isinstance(v,str) and v.strip() for v in columns):
                    raise ValueError(f'{label}: expected at least two named columns')
                if not isinstance(rows, list) or not rows:
                    raise ValueError(f'{label}: expected nonempty rows')
                for row in rows:
                    if not isinstance(row, list) or len(row) != len(columns) or not all(isinstance(v,str) and v.strip() for v in row):
                        raise ValueError(f'{label}: row width or cell content is invalid')
                if len({tuple(row) for row in rows}) != len(rows):
                    raise ValueError(f'{label}: duplicate table row')
                hex_columns = [i for i,c in enumerate(columns) if '(hex)' in c.lower()]
                decimal_columns = [i for i,c in enumerate(columns) if '(decimal)' in c.lower()]
                if len(hex_columns) == len(decimal_columns) == 1:
                    for row in rows:
                        hex_value, decimal_value = (row[i].strip('` ') for i in (hex_columns[0],decimal_columns[0]))
                        if re.fullmatch(r'[+-]?0x[0-9a-fA-F]+',hex_value) and re.fullmatch(r'[+-]?\d+',decimal_value) and int(hex_value,16) != int(decimal_value):
                            raise ValueError(f'{label}: hexadecimal and decimal values disagree')
            result[name] = record
    return result

def value_search_text(record):
    text = []
    for table in record.get('tables', []):
        text.extend([table['title'],table['description'],*table['columns']])
        text.extend(cell for row in table['rows'] for cell in row)
    # Only public interpretation text enters search; research paths stay private.
    return ' '.join(text).replace('`','')

def render_value_tables(record):
    if not record.get('tables'):
        return ''
    body = '\n## Known values\n'
    for table in record['tables']:
        body += f'\n### {table["title"]} {{#{table["id"]}}}\n\n{table["description"]}\n\n'
        body += '| ' + ' | '.join(table_cell(c) for c in table['columns']) + ' |\n'
        body += '| ' + ' | '.join('---' for _ in table['columns']) + ' |\n'
        for row in table['rows']:
            body += '| ' + ' | '.join(table_cell(c) for c in row) + ' |\n'
    return body

def declaration(a,name):
    if a.get('declaration'):return a['declaration']
    candidates=re.findall(r'\bextern\s+[^;]+;',a.get('example',''))
    return '\n'.join(c for c in candidates if re.search(r'\b'+re.escape(name)+r'\b',c))

def render(s,a,known,values=None):
    name=s['name'];folder='functions' if s['kind']=='function' else 'variables'
    body=frontmatter({'title':a['title'],'sidebar_label':name,'slug':f'/{folder}/{name}','description':a['summary']})
    body+=f'`{name}` · **{s["kind"].capitalize()}**\n\n{a["summary"]}\n\n'
    body+='| Runtime address | ROM address | Section |\n| --- | --- | --- |\n'
    body+='| '+' | '.join(f'`{table_cell(v)}`' if v else '—' for v in [s.get('address'),s.get('romAddress'),s.get('section')])+' |\n'
    if s.get('size') is not None:body+=f'\nNative code size: **{s["size"]} bytes**.\n'
    decl=declaration(a,name)
    if decl:body+='\n## Signature\n'+code(decl)
    elif s['kind']=='function':body+='\n## Interface\n\nA complete callable prototype has not been established. Use the observation or callback-identity pattern in the example rather than guessing the native arguments.\n'
    if a.get('behavior'):body+='\n## How it works\n\n'+'\n\n'.join(a['behavior'])+'\n'
    if a.get('parameters'):
        body+='\n## Parameters\n\n| Parameter | Type | Description |\n| --- | --- | --- |\n'
        for p in a['parameters']:body+=f'| `{table_cell(p["name"])}` | `{table_cell(p.get("type","See signature"))}` | {table_cell(p["description"])} |\n'
    if a.get('returns'):body+='\n## Return value\n\n'+a['returns']+'\n'
    body+=render_value_tables(values or {})
    body+='\n## Usage example\n'+code(a['example'])+'\n'+a.get('exampleExplanation','The example illustrates the native interface and its required state.')+'\n'
    if a.get('cautions'):body+='\n## Notes\n\n'+'\n'.join('- '+item for item in a['cautions'])+'\n'
    if a.get('decompilation'):
        body+='\n## Native implementation\n\n'+a.get('decompilationNote','Recovered native logic. Decompiler types and temporary names are approximate; this is reference material, not a replacement function.')+'\n'+code(a['decompilation'])
    related=[n for n in a.get('related',[]) if n in known and n!=name]
    if related:
        body+='\n## Related symbols\n\n'
        for n in related:
            target='functions' if known[n]['kind']=='function' else 'variables'
            body+=f'- [`{n}`](../{target}/{n}.md)\n'
    return body

def generate():
    inv=json.loads((ROOT/'data/inventory.json').read_text());reference=load_reference();known={s['name']:s for s in inv['symbols']}
    values=load_value_tables(known=known)
    missing=sorted(known.keys()-reference.keys())
    if missing:raise ValueError(f'Native API descriptions missing: {missing}')
    outputs={};index=[]
    for s in inv['symbols']:
        a=reference[s['name']]
        for field in ('title','summary','behavior','example'):
            if not a.get(field):raise ValueError(f'{s["name"]}: missing {field}')
        body=render(s,a,known,values.get(s['name']))
        match=FORBIDDEN.search(body)
        if match:raise ValueError(f'{s["name"]}: project reference in public text: {match.group()}')
        folder='functions' if s['kind']=='function' else 'variables'
        outputs[ROOT/'docs'/folder/(s['name']+'.md')]=body
        index.append({'name':s['name'],'kind':s['kind'],'title':a['title'],'summary':a['summary'],'address':s.get('address'),'romAddress':s.get('romAddress'),'url':f'/{folder}/{s["name"]}/'})
        if s['name'] in values:index[-1]['values']=value_search_text(values[s['name']])
    for folder in ('functions','variables'):
        directory=ROOT/'docs'/folder;directory.mkdir(parents=True,exist_ok=True)
        # Only remove generated symbol markdown; handwritten overview pages survive.
        for old in directory.glob('*.md'):
            if old.name!='index.md' and old not in outputs:old.unlink()
        entries=sorted((s for s in index if s['kind']==('function' if folder=='functions' else 'variable')),key=lambda s:s['name'])
        text=frontmatter({'title':folder.capitalize(),'slug':f'/{folder}','description':f'Native {folder} for the US recompilation of Mystical Ninja Starring Goemon.'})
        text+=f'{len(entries)} {folder} with C interfaces, behavior, and usage examples. Use the search bar to look up an exact symbol, address, or purpose.\n\n'
        if folder == 'variables':
            text+='Value tables decode established raw values and document known field layouts. Select **Tables** to jump to a variable’s mappings.\n\n'
            text+='| Symbol | Purpose | Known values |\n| --- | --- | --- |\n'
        else:text+='| Symbol | Purpose |\n| --- | --- |\n'
        for s in entries:
            text+=f'| [`{s["name"]}`]({s["name"]}.md) | {table_cell(s["title"])} |'
            if folder == 'variables':
                text+=f' [Tables]({s["name"]}.md#known-values) |' if s['name'] in values else ' — |'
            text+='\n'
        outputs[directory/'index.md']=text
    for dest,body in outputs.items():dest.write_text(body)
    for dest in (ROOT/'static/api-index.json',ROOT/'src/data/api-index.json'):
        dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(json.dumps(index,ensure_ascii=False,separators=(',',':'))+'\n')
    print(f'Generated {len(index)} native API pages and public search index.')

if __name__=='__main__':generate()
