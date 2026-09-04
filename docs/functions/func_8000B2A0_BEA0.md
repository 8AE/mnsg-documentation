---
title: "Consume saved spawn configuration"
sidebar_label: "func_8000B2A0_BEA0"
slug: "/functions/func_8000B2A0_BEA0"
description: "Copies saved spawn configuration into native destination state."
---

`func_8000B2A0_BEA0` · **Function**

Copies saved spawn configuration into native destination state.

| Runtime address | ROM address | Section |
| --- | --- | --- |
| `0x8000B2A0` | `0x0000BEA0` | `.main` |

Native code size: **196 bytes**.

## Interface

A complete callable prototype has not been established. Use the observation or callback-identity pattern in the example rather than guessing the native arguments.

## How it works

Copies the saved room at base+0x204, player rotation at +0x208, three coordinate shorts at +0x20A/+0x20C/+0x20E and camera rotation at +0x210 into system destination fields.

Also runs region/substage and load bookkeeping helpers and prepares transition counters. An entry hook is the boundary for updating validated save spawn fields immediately before this copy.

## Usage example

```c
#include "modding.h"

RECOMP_HOOK("func_8000B2A0_BEA0")
void before_spawn_consumption(void) {
    /* Reapply already-validated save spawn settings here. */
}
```

Complete C syntax example using the documented native declarations. Integrate it only at the described engine lifecycle boundary; the game supplies symbol definitions and resident resources.

## Notes

- Avoid launching or resetting a save recursively from this hook.

## Related symbols

- [`D_8015C608_15D208`](../variables/D_8015C608_15D208.md)
- [`func_8000B5D0_C1D0`](../functions/func_8000B5D0_C1D0.md)
