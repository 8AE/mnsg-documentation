---
title: "Update a transformation visual child"
sidebar_label: "func_801F14BC_5AD3CC"
slug: "/functions/func_801F14BC_5AD3CC"
description: "Updates one visual child associated with the Mini Ebisumaru and Yae Mermaid effect."
---

`func_801F14BC_5AD3CC` · **Function**

Updates one visual child associated with the Mini Ebisumaru and Yae Mermaid effect.

| Runtime address | ROM address | Section |
| --- | --- | --- |
| `0x801F14BC` | `0x005AD3CC` | `.file_11` |

Native code size: **292 bytes**.

## Interface

A complete callable prototype has not been established. Use the observation or callback-identity pattern in the example rather than guessing the native arguments.

## How it works

The callback reads the owner pose and uses it to update the child visual.

The selector-0x22 effect creates four visual children.

The callback rewrites the child task-owned material list at +0xA4 on each update; a separate graphics-visible copy must be refreshed after these native updates.

## Usage example

```c
/* Observation: func_801F14BC_5AD3CC updates a selector-0x22 visual child. */
/* Its standalone C prototype is not established; do not call it through a guessed declaration. */
```

The example illustrates the native interface and its required state.

## Notes

- The callback depends on a live owner actor and pose.
- The child appearance has not been verified in a live scene.
- The task-local material list is GPU-readable only if its address resolves within original 8 MiB RDRAM.
