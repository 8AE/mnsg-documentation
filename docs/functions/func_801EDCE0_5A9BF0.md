---
title: "Update Sasuke jetpack smoke"
sidebar_label: "func_801EDCE0_5A9BF0"
slug: "/functions/func_801EDCE0_5A9BF0"
description: "This callback emits and cleans up Sasuke’s player-owned jetpack smoke effect."
---

`func_801EDCE0_5A9BF0` · **Function**

This callback emits and cleans up Sasuke’s player-owned jetpack smoke effect.

| Runtime address | ROM address | Section |
| --- | --- | --- |
| `0x801EDCE0` | `0x005A9BF0` | `.file_11` |

Native code size: **588 bytes**.

## Interface

A complete callable prototype has not been established. Use the observation or callback-identity pattern in the example rather than guessing the native arguments.

## How it works

While the owner action is 0x9B, the callback emits puffs at two-tick intervals.

On exit it clears owner player-work at +0x86, queues global stop cue 0x814F, and marks the emitter state at +0x60 as 2.

The jet smoke descriptor D_80204BF8 contains three 0x8000 rotation halfwords at +0x20, +0x22, and +0x24.

The callback passes those values through func_801EE750_5AA660 and func_801EE688_5AA598 into child object rotation fields +0x14, +0x16, and +0x18. The descriptor selects model 0x490026B0 with mode 10; this jet puff model also follows the 0x40000000 camera-facing renderer branch.

## Usage example

```c
/* Observation: func_801EDCE0_5A9BF0 is an identified native routine. */
/* Its standalone C prototype is not established; do not call it through a guessed declaration. */
```

The example illustrates the native interface and its required state.

## Notes

- The callback changes local player-work and queues a global sound-stop command. Do not replay it for a remote player.
- The live appearance of the effect has not been verified.
