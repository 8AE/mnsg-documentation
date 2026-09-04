#!/usr/bin/env python3
"""Index stock game symbols actually used by five MNSG mod source trees.

Python 3.11+, standard library only. This is a lexical source inventory, not a C
compiler: it includes all conditional compilation branches, ignores comments and
ordinary string literals, and recognizes direct and function-macro hook targets.
Addresses and sizes are copied from the checked-in symbol tables, never guessed
from names. Source declarations describe the mods' ABI assumptions, not proven
native types. Run from any directory; --workspace selects the five sibling repos.
"""
from __future__ import annotations

import argparse
from bisect import bisect_right
from collections import defaultdict
from datetime import datetime, timezone
import json
import hashlib
from pathlib import Path
import re
import subprocess
import tomllib

PROJECTS = ("mnsg-custom-fish", "mnsg-enable-boss-rush", "mnsg-extra-options",
            "mnsg-recomp-example", "mnsg-team-up")
SDK_HEADERS = {"modding.h", "recomputils.h", "recompdata.h", "recompconfig.h",
               "recompui.h", "recompui_event_structs.h", "z64recomp_api.h",
               "rt64_extended_gbi.h", "repy_api.h"}
IDENT = re.compile(r"\b[A-Za-z_][A-Za-z_0-9]*\b")
GAME_NAME = re.compile(r"(?:func_[0-9A-Fa-f]+(?:_[0-9A-Fa-f]+)?|D_[0-9A-Fa-f]+(?:_[0-9A-Fa-f]+)?)\Z")
HOOK = re.compile(r"\b(RECOMP_HOOK_RETURN|RECOMP_HOOK)\s*\(")


def blank(text: str) -> str:
    return "".join("\n" if char == "\n" else " " for char in text)


def mask_c(text: str, strings: bool = True) -> str:
    """Replace comments (and optionally literals) with whitespace at exact offsets."""
    pattern = re.compile(r'//[^\n]*|/\*[\s\S]*?\*/|"(?:\\[\s\S]|[^"\\])*"|\'(?:\\[\s\S]|[^\'\\])*\'')
    return pattern.sub(lambda m: blank(m[0]) if strings or m[0].startswith(("//", "/*")) else m[0], text)


def line_at(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def arguments(text: str, opening: int):
    """Return (argument spans, end) for a balanced parenthesized invocation."""
    depth, start, spans, i = 1, opening + 1, [], opening + 1
    while i < len(text):
        if text[i] in "\"'":
            quote = text[i]
            i += 1
            while i < len(text):
                if text[i] == "\\":
                    i += 2
                    continue
                if text[i] == quote:
                    break
                i += 1
        elif text[i] == "(":
            depth += 1
        elif text[i] == ")":
            depth -= 1
            if depth == 0:
                spans.append((start, i))
                return spans, i + 1
        elif text[i] == "," and depth == 1:
            spans.append((start, i))
            start = i + 1
        i += 1
    return [], opening + 1


def macro_definitions(text: str):
    result = {}
    for match in re.finditer(r"(?m)^\s*#\s*define\s+(\w+)\(([^\n)]*)\)", text):
        end = text.find("\n", match.end())
        end = len(text) if end < 0 else end
        while text[match.end():end].rstrip().endswith("\\") and end < len(text):
            next_end = text.find("\n", end + 1)
            end = len(text) if next_end < 0 else next_end
        result[match[1]] = {"params": [x.strip() for x in match[2].split(",")],
                             "body": text[match.end():end].replace("\\\n", "\n"),
                             "start": match.start(), "end": end}
    return result


def hook_specs(body: str, macros: dict, trail=()):
    """Find hook argument expressions, including wrappers around hook macros."""
    found = []
    for match in HOOK.finditer(body):
        spans, _ = arguments(body, body.index("(", match.start()))
        if spans:
            found.append(("hook-return" if match[1].endswith("RETURN") else "hook", body[slice(*spans[0])].strip()))
    for name, macro in macros.items():
        if name in trail or name.startswith("RECOMP_"):
            continue
        for match in re.finditer(r"\b" + re.escape(name) + r"\s*\(", body):
            spans, _ = arguments(body, body.index("(", match.start()))
            if len(spans) != len(macro["params"]):
                continue
            values = dict(zip(macro["params"], [body[slice(*span)].strip() for span in spans]))
            for role, expression in hook_specs(macro["body"], macros, trail + (name,)):
                expression = IDENT.sub(lambda m: values.get(m[0], m[0]), expression)
                found.append((role, expression))
    return found


def extract_references(text: str, known_names: set[str]):
    """Return lexical symbol references/declarations with exact source offsets."""
    comments_masked = mask_c(text, strings=False)
    code = mask_c(text)
    macros = macro_definitions(comments_masked)
    macro_spans = [(item["start"], item["end"]) for item in macros.values()]
    refs, declarations, special_positions, unresolved_hooks = [], [], set(), []

    def is_candidate(name):
        return name in known_names or bool(GAME_NAME.fullmatch(name))

    def add(name, pos, role, **extra):
        refs.append({"name": name, "offset": pos, "line": line_at(text, pos), "role": role, **extra})
        special_positions.add(pos)

    # An extern may span several lines and contain function-pointer parameters.
    declaration_spans = []
    for match in re.finditer(r"\bextern\b[^;{}]*;", code):
        declaration_spans.append((match.start(), match.end()))
        for token in IDENT.finditer(code, match.start(), match.end()):
            if is_candidate(token[0]):
                add(token[0], token.start(), "declared")
                declarations.append({"name": token[0], "offset": token.start(),
                                     "line": line_at(text, match.start()),
                                     "text": comments_masked[match.start():match.end()].strip()})

    # Direct hooks use literal strings; ordinary strings never count as symbols.
    for match in HOOK.finditer(comments_masked):
        if any(start <= match.start() < end for start, end in macro_spans):
            continue
        spans, _ = arguments(comments_masked, comments_masked.index("(", match.start()))
        expression = comments_masked[slice(*spans[0])].strip() if spans else ""
        target = re.fullmatch(r'"([A-Za-z_]\w*)"', expression)
        if target:
            add(target[1], match.start(), "hook-return" if match[1].endswith("RETURN") else "hook")
        else:
            unresolved_hooks.append({"line": line_at(text, match.start()), "expression": expression})

    # Resolve e.g. TRACK_CONGO_PART("func_080066B0_6B9950", 0).
    for name, macro in macros.items():
        specs = hook_specs(macro["body"], macros, (name,))
        if not specs or name.startswith("RECOMP_"):
            continue
        for match in re.finditer(r"\b" + re.escape(name) + r"\s*\(", comments_masked):
            if any(start <= match.start() < end for start, end in macro_spans):
                continue
            spans, _ = arguments(comments_masked, comments_masked.index("(", match.start()))
            values = dict(zip(macro["params"], [comments_masked[slice(*s)].strip() for s in spans]))
            for role, expression in specs:
                expression = IDENT.sub(lambda m: values.get(m[0], m[0]), expression)
                target = re.fullmatch(r'"([A-Za-z_]\w*)"', expression)
                if target:
                    add(target[1], match.start(), role, viaMacro=name)
                else:
                    unresolved_hooks.append({"line": line_at(text, match.start()), "expression": expression, "viaMacro": name})

    # Mark patch definitions distinctly from calls to the patched original name.
    for match in re.finditer(r"\bRECOMP_(?:FORCE_)?PATCH\b\s+[^;{}]*?\b([A-Za-z_]\w*)\s*\(", code):
        if is_candidate(match[1]):
            pos = match.start(1)
            add(match[1], pos, "patched")
            spans, end = arguments(code, code.index("(", pos))
            if spans:
                declarations.append({"name": match[1], "offset": pos, "line": line_at(text, match.start()),
                                     "text": comments_masked[match.start():end].strip() + ";"})

    for token in IDENT.finditer(code):
        name, pos = token[0], token.start()
        if not is_candidate(name) or pos in special_positions:
            continue
        if any(start <= pos < end for start, end in declaration_spans):
            continue
        role = "called" if re.match(r"\s*\(", code[token.end():]) else "referenced"
        add(name, pos, role)
    # One source location/role is enough even when a line mentions a variable twice.
    unique = {}
    for ref in refs:
        unique[(ref["name"], ref["line"], ref["role"])] = ref
    return sorted(unique.values(), key=lambda r: (r["offset"], r["name"], r["role"])), declarations, unresolved_hooks


def source_context(text: str, line: int, role: str):
    lines = text.splitlines()
    start, end = max(0, line - 7), min(len(lines), line + 7)
    # Retain complete short hook callbacks, otherwise a bounded actual excerpt.
    if role in {"hook", "hook-return", "patched"}:
        segment = "\n".join(lines[line - 1:min(len(lines), line + 32)])
        clean = mask_c(segment)
        opening = clean.find("{")
        if opening >= 0:
            depth = 0
            for i in range(opening, len(clean)):
                depth += (clean[i] == "{") - (clean[i] == "}")
                if depth == 0:
                    start = max(0, line - 3)
                    end = line + clean.count("\n", 0, i)
                    break
    return "\n".join(lines[start:end]), start + 1


def load_tables(project: Path):
    entries, table_files = [], []
    for path in sorted((project / "Goemon64RecompSyms").glob("*syms.toml")):
        text = path.read_text()
        parsed = tomllib.loads(text)
        locations = defaultdict(list)
        line_starts = [0] + [match.end() for match in re.finditer("\\n", text)]
        for match in re.finditer(r'\bname\s*=\s*"([^"]+)"', text):
            locations[match[1]].append(bisect_right(line_starts, match.start()))
        table_files.append(str(path.relative_to(project)))
        for section in parsed.get("section", []):
            for field, kind in (("functions", "function"), ("symbols", "variable")):
                for symbol in section.get(field, []):
                    address = symbol.get("vram")
                    rom = None
                    if "rom" in section and address is not None:
                        rom = section["rom"] + address - section.get("vram", address)
                    metadata = {"project": project.name, "path": str(path.relative_to(project)),
                                "line": locations[symbol["name"]].pop(0), "kind": kind,
                                "address": f"0x{address:08X}" if address is not None else None,
                                "size": symbol.get("size"), "section": section.get("name"),
                                "romAddress": f"0x{rom:08X}" if rom is not None else None}
                    extra = {key: value for key, value in symbol.items() if key not in {"name", "vram", "size"}}
                    if extra:
                        metadata["metadata"] = extra
                    entries.append((symbol["name"], metadata))
    return entries, table_files


def git(project: Path, *args):
    proc = subprocess.run(["git", "-C", str(project), *args], text=True, capture_output=True)
    return proc.stdout.strip() if proc.returncode == 0 else None


def scan(workspace: Path, project_names=PROJECTS, snapshot_output: Path | None = None):
    table_by_name, aliases_by_location, project_info = defaultdict(list), defaultdict(set), []
    source_texts, table_counts = {}, {}
    for name in project_names:
        root = workspace / name
        if not root.is_dir():
            raise FileNotFoundError(f"Missing mod repository: {root}")
        table_entries, table_files = load_tables(root)
        if not table_files:
            raise FileNotFoundError(f"Missing Goemon64RecompSyms/*syms.toml in {root}")
        table_counts[name] = len(table_entries)
        for symbol_name, metadata in table_entries:
            table_by_name[symbol_name].append(metadata)
            aliases_by_location[(metadata["kind"], metadata["section"], metadata["address"], metadata["romAddress"])].add(symbol_name)
        sources = sorted(set([*root.glob("src/**/*.c"), *root.glob("src/**/*.h"), *root.glob("src/**/*.inc"),
                              *[p for p in root.glob("include/**/*.h") if p.name not in SDK_HEADERS]]))
        for path in sources:
            source_texts[(name, str(path.relative_to(root)))] = path.read_text()
        project_info.append({"name": name, "commit": git(root, "rev-parse", "HEAD"),
                             "dirty": bool(git(root, "status", "--porcelain")),
                             "remote": git(root, "remote", "get-url", "origin"),
                             "sourceFiles": [str(p.relative_to(root)) for p in sources],
                             "symbolTables": table_files, "symbolCount": 0})
    if snapshot_output:
        snapshots = {}
        for (project, path), content in source_texts.items():
            snapshots[f"{project}/{path}"] = {"project": project, "path": path,
                                           "sha256": hashlib.sha256(content.encode()).hexdigest(), "content": content}
        snapshot_output.parent.mkdir(parents=True, exist_ok=True)
        snapshot_output.write_text(json.dumps(snapshots, indent=2) + "\n")
    symbols, unresolved_hooks = {}, []
    known_names = set(table_by_name)
    for (project, path), text in source_texts.items():
        refs, declarations, hook_errors = extract_references(text, known_names)
        unresolved_hooks.extend({"project": project, "path": path, **item} for item in hook_errors)
        for ref in refs:
            name = ref["name"]
            if name not in symbols:
                sources = table_by_name.get(name, [])
                preferred = next((entry for entry in sources if entry["project"] == project), sources[0] if sources else {})
                kind = preferred.get("kind", "variable" if name.startswith("D_") else "function")
                variants = sorted({(e["kind"], e["address"], e["size"], e["section"], e["romAddress"]) for e in sources}, key=str)
                symbol_aliases = set()
                for e in sources:
                    symbol_aliases.update(aliases_by_location[(e["kind"], e["section"], e["address"], e["romAddress"])])
                symbols[name] = {"name": name, "kind": kind,
                                 **{field: preferred.get(field) for field in ("address", "size", "section", "romAddress")},
                                 "projects": [], "roles": [], "declarations": [], "references": [],
                                 "symbolSources": sources, "aliases": sorted(symbol_aliases - {name}),
                                 "variants": [dict(zip(("kind", "address", "size", "section", "romAddress"), v)) for v in variants],
                                 "conflicts": []}
            symbol = symbols[name]
            if project not in symbol["projects"]:
                symbol["projects"].append(project)
            if ref["role"] not in symbol["roles"]:
                symbol["roles"].append(ref["role"])
            context, context_start = source_context(text, ref["line"], ref["role"])
            symbol["references"].append({"project": project, "path": path,
                                         **{key: value for key, value in ref.items() if key not in {"name", "offset"}},
                                         "context": context, "contextStartLine": context_start})
        for declaration in declarations:
            name = declaration["name"]
            symbols[name]["declarations"].append({"text": declaration["text"], "project": project,
                                                 "path": path, "line": declaration["line"]})
    unresolved = []
    conflicts = []
    declaration_differences = []
    table_texts = {}
    for symbol in symbols.values():
        for source in symbol["symbolSources"]:
            key = (source["project"], source["path"])
            if key not in table_texts:
                content = (workspace / key[0] / key[1]).read_text()
                table_texts[key] = (content.splitlines(), hashlib.sha256(content.encode()).hexdigest())
            lines, digest = table_texts[key]
            start, end = max(0, source["line"] - 3), min(len(lines), source["line"] + 2)
            source["context"] = "\n".join(lines[start:end])
            source["contextStartLine"] = start + 1
            source["sha256"] = digest
        symbol["projects"].sort()
        symbol["roles"].sort()
        if not symbol["symbolSources"]:
            unresolved.append({"name": symbol["name"], "projects": symbol["projects"], "roles": symbol["roles"],
                               "reason": "Referenced in mod C source but absent from all scanned symbol tables."})
        for field in ("kind", "address", "size", "romAddress"):
            values = {entry[field] for entry in symbol["symbolSources"]}
            if len(values) > 1:
                symbol["conflicts"].append({"field": field, "values": sorted(values, key=str)})
        # Keep differing declaration spellings visible. Do not equate typedefs or
        # claim a native ABI mismatch without parsing and proving the C types.
        decl_variants = sorted({re.sub(r"\s+", " ", d["text"]).strip() for d in symbol["declarations"]})
        symbol["declarationVariants"] = decl_variants
        symbol["declarationReviewRequired"] = len(decl_variants) > 1
        if len(decl_variants) > 1:
            declaration_differences.append({"name": symbol["name"], "variants": decl_variants,
                                           "reason": "Mod-side declarations differ; review parameter names, typedef aliases and ABI assumptions before reuse."})
        if symbol["conflicts"]:
            conflicts.append({"name": symbol["name"], "conflicts": symbol["conflicts"]})
    for project in project_info:
        project["symbolCount"] = sum(project["name"] in symbol["projects"] for symbol in symbols.values())
    return {"schemaVersion": 1, "generatedAt": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "projects": project_info, "symbols": sorted(symbols.values(), key=lambda s: (s["kind"], s["name"])),
            "audit": {"sourceFileCount": len(source_texts), "tableEntryCounts": table_counts,
                      "tableSymbolCount": len(table_by_name), "documentedSymbolCount": len(symbols),
                      "functionCount": sum(s["kind"] == "function" for s in symbols.values()),
                      "variableCount": sum(s["kind"] == "variable" for s in symbols.values()),
                      "referenceCount": sum(len(s["references"]) for s in symbols.values()),
                      "macroHookReferenceCount": sum("viaMacro" in r for s in symbols.values() for r in s["references"]),
                      "unresolvedSymbols": sorted(unresolved, key=lambda x: x["name"]), "unresolvedHooks": unresolved_hooks,
                      "projectTableGaps": [{"name": s["name"], "project": project}
                                           for s in symbols.values() for project in s["projects"]
                                           if project not in {entry["project"] for entry in s["symbolSources"]}],
                      "metadataConflicts": conflicts, "sourceDeclarationDifferences": declaration_differences, "excludedSDKHeaders": sorted(SDK_HEADERS),
                      "scope": "All C/header/include-source branches under src/ and mod-owned include/ headers; generated build files, SDK headers, test fixtures and comments are excluded.",
                      "limitations": ["Lexical source inventory, not a compiler or runtime certification.",
                                      "All conditional compilation branches are included; declarations may be unused in a particular build.",
                                      "Variable sizes are null when omitted by the symbol tables.",
                                      "Source prototypes are mod-side declarations; distinct spellings do not prove a native ABI conflict.",
                                      "Numeric address casts and inline assembly-only references are not automatically resolved to symbolic names."]}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--snapshots", type=Path, default=Path(__file__).resolve().parents[1] / "data/source-snapshots.json")
    parser.add_argument("--output", type=Path, default=Path(__file__).resolve().parents[1] / "data/inventory.json")
    args = parser.parse_args()
    inventory = scan(args.workspace, snapshot_output=args.snapshots)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(inventory, indent=2) + "\n")
    audit = inventory["audit"]
    print(f"Indexed {audit['documentedSymbolCount']} symbols ({audit['functionCount']} functions, {audit['variableCount']} variables) across {audit['sourceFileCount']} source files.")
    print(f"{audit['referenceCount']} references; {len(audit['unresolvedSymbols'])} symbols lack table metadata; {len(audit['unresolvedHooks'])} unresolved hooks.")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
