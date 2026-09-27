---
title: "Initialize a Sudden Impact satellite"
sidebar_label: "func_801F1BD0_5ADAE0"
slug: "/functions/func_801F1BD0_5ADAE0"
description: "This initializer configures one satellite in the Sudden Impact aura."
---

`func_801F1BD0_5ADAE0` · **Function**

This initializer configures one satellite in the Sudden Impact aura.

| Runtime address | ROM address | Section |
| --- | --- | --- |
| `0x801F1BD0` | `0x005ADAE0` | `.file_11` |

Native code size: **244 bytes**.

## Interface

A complete callable prototype has not been established. Use the observation or callback-identity pattern in the example rather than guessing the native arguments.

## How it works

Each satellite uses model 0x1900074C. The native effect creates five satellites.

The initializer binds the object material pointer from its child task +0xA4 through the native segmented material path.

## Usage example

```c
/* Observation: func_801F1BD0_5ADAE0 is an identified native routine. */
/* Its standalone C prototype is not established; do not call it through a guessed declaration. */
```

The example illustrates the native interface and its required state.
