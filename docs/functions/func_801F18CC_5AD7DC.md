---
title: "Initialize the main Sudden Impact aura"
sidebar_label: "func_801F18CC_5AD7DC"
slug: "/functions/func_801F18CC_5AD7DC"
description: "This initializer configures the main visual model for the Sudden Impact aura."
---

`func_801F18CC_5AD7DC` · **Function**

This initializer configures the main visual model for the Sudden Impact aura.

| Runtime address | ROM address | Section |
| --- | --- | --- |
| `0x801F18CC` | `0x005AD7DC` | `.file_11` |

Native code size: **216 bytes**.

## Interface

A complete callable prototype has not been established. Use the observation or callback-identity pattern in the example rather than guessing the native arguments.

## How it works

The main aura model is 0x190006B8. The effect uses resource 0x152 and character asset 0x120.

The initializer binds the object material pointer from its child task +0xA4 through the native segmented material path.

## Usage example

```c
/* Observation: func_801F18CC_5AD7DC is an identified native routine. */
/* Its standalone C prototype is not established; do not call it through a guessed declaration. */
```

The example illustrates the native interface and its required state.
