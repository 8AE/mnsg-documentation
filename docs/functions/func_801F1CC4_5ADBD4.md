---
title: "Update a Sudden Impact aura satellite"
sidebar_label: "func_801F1CC4_5ADBD4"
slug: "/functions/func_801F1CC4_5ADBD4"
description: "This callback updates one of the native satellite effects around the aura."
---

`func_801F1CC4_5ADBD4` · **Function**

This callback updates one of the native satellite effects around the aura.

| Runtime address | ROM address | Section |
| --- | --- | --- |
| `0x801F1CC4` | `0x005ADBD4` | `.file_11` |

Native code size: **624 bytes**.

## Interface

A complete callable prototype has not been established. Use the observation or callback-identity pattern in the example rather than guessing the native arguments.

## How it works

The constructor creates five satellites using model 0x1900074C.

The callback reads owner pose/action state and updates its visual effect.

The effect object material pointer is derived from the task-local material list at task +0xA4.

## Usage example

```c
/* Observation: func_801F1CC4_5ADBD4 is an identified native routine. */
/* Its standalone C prototype is not established; do not call it through a guessed declaration. */
```

The example illustrates the native interface and its required state.

## Notes

- The callback depends on a live owner and its current pose/action.
- The live appearance of the effect has not been verified.
- The RSP material list must resolve within original 8 MiB RDRAM; an extended CPU task address may not be GPU-readable.
