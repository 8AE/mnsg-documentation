---
title: "Stop native sound playback"
sidebar_label: "func_8003A24C_3AE4C"
slug: "/functions/func_8003A24C_3AE4C"
description: "This routine handles a native sound-stop command."
---

`func_8003A24C_3AE4C` · **Function**

This routine handles a native sound-stop command.

| Runtime address | ROM address | Section |
| --- | --- | --- |
| `0x8003A24C` | `0x0003AE4C` | `.main` |

Native code size: **132 bytes**.

## Interface

A complete callable prototype has not been established. Use the observation or callback-identity pattern in the example rather than guessing the native arguments.

## How it works

The sound dispatcher routes command 0x8170 here. The tracked sound ID is its low value, 0x0170.

The native stop state is global by sound ID and does not distinguish which player initiated the sound.

## Usage example

```c
/* Observation: func_8003A24C_3AE4C is an identified native routine. */
/* Its standalone C prototype is not established; do not call it through a guessed declaration. */
```

The example illustrates the native interface and its required state.

## Notes

- A full standalone C calling interface has not been established.
