---
title: "Static g_system storage"
sidebar_label: "D_800BCCC0_BD8C0"
slug: "/variables/D_800BCCC0_BD8C0"
description: "Static storage for native system state."
---

`D_800BCCC0_BD8C0` · **Variable**

Static storage for native system state.

| Runtime address | ROM address | Section |
| --- | --- | --- |
| `0x800BCCC0` | — | `ABSOLUTE_SYMS` |

## Signature

```c
extern unsigned char D_800BCCC0_BD8C0[];
```

## How it works

Contains system execution, scene destination, UI and related fields. Both this direct storage and the runtime pointer D_8015C5C8 occur in native paths.

Treat the block as an opaque large structure unless a field layout is established. The unsized byte-array declaration is not permission to clear or copy an arbitrary length.

## Usage example

```c
extern unsigned char D_800BCCC0_BD8C0[];

/* Read only while the native system structure is initialized. */
short read_static_destination(void) {
    return *(short *)(D_800BCCC0_BD8C0 + 0x3AFE0);
}
```

Complete C syntax example using the documented native declarations. Integrate it only at the described engine lifecycle boundary; the game supplies symbol definitions and resident resources.

## Notes

- Do not copy or clear this entire opaque block based on the unsized extern declaration.

## Related symbols

- [`D_8015C5C8_15D1C8`](../variables/D_8015C5C8_15D1C8.md)
- [`func_8000607C_6C7C`](../functions/func_8000607C_6C7C.md)
