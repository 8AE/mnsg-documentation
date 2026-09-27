---
title: "Collect a small health pickup"
sidebar_label: "func_80214AEC_5CFFBC"
slug: "/functions/func_80214AEC_5CFFBC"
description: "This health pickup uses the native small-health acquisition cue."
---

`func_80214AEC_5CFFBC` · **Function**

This health pickup uses the native small-health acquisition cue.

| Runtime address | ROM address | Section |
| --- | --- | --- |
| `0x80214AEC` | `0x005CFFBC` | `.file_12` |

Native code size: **96 bytes**.

## Interface

A complete callable prototype has not been established. Use the observation or callback-identity pattern in the example rather than guessing the native arguments.

## How it works

The inspected US callback emits sound cue 0x026C when bit 0x200 is set in the task word at +0x68.

This bit is an event gate in the inspected callback; it is not a standalone sound-ID mapping for every health pickup.

The callback identity is known, but a standalone C prototype is not established.

## Usage example

```c
/* Observation: func_80214AEC_5CFFBC is an identified native routine. */
/* Its standalone C prototype is not established; do not call it through a guessed declaration. */
```

The example illustrates the native interface and its required state.
