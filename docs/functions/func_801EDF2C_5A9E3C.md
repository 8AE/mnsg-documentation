---
title: "Create a jetpack smoke puff"
sidebar_label: "func_801EDF2C_5A9E3C"
slug: "/functions/func_801EDF2C_5A9E3C"
description: "This helper creates one native puff for the jetpack smoke effect."
---

`func_801EDF2C_5A9E3C` · **Function**

This helper creates one native puff for the jetpack smoke effect.

| Runtime address | ROM address | Section |
| --- | --- | --- |
| `0x801EDF2C` | `0x005A9E3C` | `.file_11` |

Native code size: **304 bytes**.

## Interface

A complete callable prototype has not been established. Use the observation or callback-identity pattern in the example rather than guessing the native arguments.

## How it works

Each puff uses model 0x490026B0, resource 0x152, scale 0.02, white color, and alpha 0xE8.

The puff grows by 0.004 scale units and fades alpha by 0x10 per update.

The puff uses descriptor D_80204AD0 and a material pointer derived from the native object at +0x80 with flag 0x20000000.

While the owner remains in the jetpack action, puff vertical drift follows -0.5 * (2.56410265 - owner task +0xA4). During cleanup, vertical drift is -2.

## Usage example

```c
/* Observation: func_801EDF2C_5A9E3C is an identified native routine. */
/* Its standalone C prototype is not established; do not call it through a guessed declaration. */
```

The example illustrates the native interface and its required state.
