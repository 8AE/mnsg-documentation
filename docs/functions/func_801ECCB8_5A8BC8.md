---
title: "Dispatch Fire Ryo action"
sidebar_label: "func_801ECCB8_5A8BC8"
slug: "/functions/func_801ECCB8_5A8BC8"
description: "This player action dispatches the Fire Ryo selector through its native projectile setup and trail path."
---

`func_801ECCB8_5A8BC8` · **Function**

This player action dispatches the Fire Ryo selector through its native projectile setup and trail path.

| Runtime address | ROM address | Section |
| --- | --- | --- |
| `0x801ECCB8` | `0x005A8BC8` | `.file_11` |

Native code size: **56 bytes**.

## Interface

A complete callable prototype has not been established. Use the observation or callback-identity pattern in the example rather than guessing the native arguments.

## How it works

Selector 0x12 passes through this dispatcher.

The path calls func_801E8F50_5A4E60 with the manager and selector 0x12, and invokes func_801ED1F0_5A9100 for the Fire Ryo trail.

## Usage example

```c
/* Observation: func_801ECCB8_5A8BC8 is an identified native routine. */
/* Its standalone C prototype is not established; do not call it through a guessed declaration. */
```

The example illustrates the native interface and its required state.
