---
title: "Update a Fire Ryo projectile"
sidebar_label: "func_801ECCF0_5A8C00"
slug: "/functions/func_801ECCF0_5A8C00"
description: "This callback advances the native Fire Ryo projectile and handles its impact effect."
---

`func_801ECCF0_5A8C00` · **Function**

This callback advances the native Fire Ryo projectile and handles its impact effect.

| Runtime address | ROM address | Section |
| --- | --- | --- |
| `0x801ECCF0` | `0x005A8C00` | `.file_11` |

Native code size: **540 bytes**.

## Interface

A complete callable prototype has not been established. Use the observation or callback-identity pattern in the example rather than guessing the native arguments.

## How it works

The first update advances age and velocity. During ages 2 through 59, the callback performs a raycast for impact.

On impact it creates a visual effect, plays positional cue 0x029A, changes task phase +0x60 to 1, and begins fading the effect by 0x10 per update.

A hard 60-tick lifetime ends the projectile path.

The callback invokes a native collision helper. Its full collision behavior is not established here.

## Usage example

```c
/* Observation: func_801ECCF0_5A8C00 is an identified native callback. */
/* Its standalone C prototype is not established; do not call it through a guessed declaration. */
```

The example illustrates the native interface and its required state.

## Notes

- The collision path is part of native gameplay behavior and must not be replayed as a display-only remote effect.
