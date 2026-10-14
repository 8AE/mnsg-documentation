---
title: "Turn a task toward an XZ target"
sidebar_label: "func_802196FC_5D4BCC"
slug: "/functions/func_802196FC_5D4BCC"
description: "Steps a task object’s 10-bit yaw toward a target using a caller-supplied turn step."
---

`func_802196FC_5D4BCC` · **Function**

Steps a task object’s 10-bit yaw toward a target using a caller-supplied turn step.

| Runtime address | ROM address | Section |
| --- | --- | --- |
| `0x802196FC` | `0x005D4BCC` | `.file_12` |

## Signature

```c
extern int func_802196FC_5D4BCC(void *task, float target_x, float target_y, float target_z, int turn_step);
```

## How it works

Computes the target yaw from target X/Z and the task object at task +0x18, then changes object yaw at +0x16 by twice the signed turn_step, wrapping to 10 bits.

The target Y argument occupies the native calling-convention slot but is not read. Returns 0 when aligned or snapped to the target, 1 for one yaw direction, and 2 for the other.

## Parameters

| Parameter | Type | Description |
| --- | --- | --- |
| `task` | `void *` | Task whose object pointer is at +0x18. |
| `target_x` | `float` | Target world X coordinate. |
| `target_y` | `float` | Native argument slot; this helper does not use the value. |
| `target_z` | `float` | Target world Z coordinate. |
| `turn_step` | `int` | Signed step; the helper applies twice this value to 10-bit yaw. |

## Return value

Returns 0 when aligned or snapped, 1 or 2 for the two nonzero turn directions.

## Usage example

```c
#include "modding.h"
extern int func_802196FC_5D4BCC(void *task, float target_x, float target_y, float target_z, int turn_step);

int turn_actor(void *task, float x, float y, float z)
{
    if (!task) return 0;
    return func_802196FC_5D4BCC(task, x, y, z, 8);
}
```

The example shows the verified native call shape. Use it only at a lifecycle point where the documented task and state are valid.

## Notes

- The helper requires a valid task object at +0x18. It changes yaw only; callers retain responsibility for target choice and scheduling.

## Related symbols

- [`func_80219448_5D4918`](../functions/func_80219448_5D4918.md)
- [`func_8021BB04_5D6FD4`](../functions/func_8021BB04_5D6FD4.md)
