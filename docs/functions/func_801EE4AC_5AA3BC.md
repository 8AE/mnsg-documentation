---
title: "Initialize an effect child task"
sidebar_label: "func_801EE4AC_5AA3BC"
slug: "/functions/func_801EE4AC_5AA3BC"
description: "Sets the owner and kind fields used by native effect descendant scans."
---

`func_801EE4AC_5AA3BC` · **Function**

Sets the owner and kind fields used by native effect descendant scans.

| Runtime address | ROM address | Section |
| --- | --- | --- |
| `0x801EE4AC` | `0x005AA3BC` | `.file_11` |

Native code size: **52 bytes**.

## Interface

A complete callable prototype has not been established. Use the observation or callback-identity pattern in the example rather than guessing the native arguments.

## How it works

Sets task +0x64 to the effect selector and clears task +0x65.

Copies the owner manager pointer to task +0x84 and copies manager +0x5C into child task +0x5C.

These fields let the flat-list descendant scan recognize a new child before its first scheduled update.

## Usage example

```c
/* Observation: func_801EE4AC_5AA3BC initializes effect task fields. */
/* Its standalone C prototype is not established; do not call it through a guessed declaration. */
```

The example illustrates the native interface and its required state.

## Notes

- The standalone C prototype is not established.
