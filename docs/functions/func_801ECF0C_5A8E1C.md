---
title: "Create a Fire Ryo impact effect"
sidebar_label: "func_801ECF0C_5A8E1C"
slug: "/functions/func_801ECF0C_5A8E1C"
description: "This native routine creates the visual effect used when a Fire Ryo projectile hits."
---

`func_801ECF0C_5A8E1C` · **Function**

This native routine creates the visual effect used when a Fire Ryo projectile hits.

| Runtime address | ROM address | Section |
| --- | --- | --- |
| `0x801ECF0C` | `0x005A8E1C` | `.file_11` |

Native code size: **328 bytes**.

## Interface

A complete callable prototype has not been established. Use the observation or callback-identity pattern in the example rather than guessing the native arguments.

## How it works

The inspected Fire Ryo callback invokes this routine for the impact visual.

The callback also plays positional sound cue 0x029A; the full argument interface for this routine is not established.

## Usage example

```c
/* Observation: func_801ECF0C_5A8E1C is an identified native routine. */
/* Its standalone C prototype is not established; do not call it through a guessed declaration. */
```

The example illustrates the native interface and its required state.
