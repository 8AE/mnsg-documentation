---
title: "Update the Ebisumaru camera effect"
sidebar_label: "func_801EBAA8_5A79B8"
slug: "/functions/func_801EBAA8_5A79B8"
description: "Common update body for native camera-effect variants. The offset vector, player animation frame threshold and initial pitch are supplied by the small variant callbacks."
---

`func_801EBAA8_5A79B8` · **Function**

Common update body for native camera-effect variants. The offset vector, player animation frame threshold and initial pitch are supplied by the small variant callbacks.

| Runtime address | ROM address | Section |
| --- | --- | --- |
| `0x801EBAA8` | `0x005A79B8` | `.file_11` |

Native code size: **444 bytes**.

## Signature

```c
extern void func_801EBAA8_5A79B8(void *task, float x, float y, float z, float start_frame, unsigned short pitch);
```

## How it works

Common update body for native camera-effect variants. The offset vector, player animation frame threshold and initial pitch are supplied by the small variant callbacks.

Phase byte +0x60 starts at zero. While waiting for the required owner animation frame, the object pose is not yet initialized. Once the threshold is reached, the routine transforms the offset relative to the owner, sets rotations and advances phase to one.

Phase one fades the existing material alpha by 24 per update. Completion marks removal and advances phase again. The effect is stationary after its initial pose; unrelated task work fields must not be interpreted as projectile velocity.

The initializer checks the owner action and changes owner feedback and sound state. It is an update for a fully constructed task, not an independent visual constructor.

## Return value

No return value.

## Usage example

```c
#include "modding.h"

static void *updating_task;
static unsigned char observed_phase;

RECOMP_HOOK("func_801EBAA8_5A79B8")
void observe_update_entry(void *task)
{
    updating_task = task;
}

RECOMP_HOOK_RETURN("func_801EBAA8_5A79B8")
void observe_update_return(void)
{
    if (updating_task)
        observed_phase = ((const unsigned char *)updating_task)[0x60];
    updating_task = 0;
}
```

Read-only entry/return observation of the existing native update. Save the task argument at entry: a return hook cannot assume that the original argument registers survived the native call. Native task validity and ownership must still be checked before any subsequent operation.

## Notes

- The routine updates an existing native actor and its complete work state. Do not call it as a generic spawner or use it on a display-only task.
- The native manager processes removal requests after the update. Do not retain task or object addresses across destruction or storage reuse without checking their lifecycle.
- The common update is reached through native variant callbacks. Preserve every native argument if directly calling the function; an observation hook may read only the first argument.

## Related symbols

- [`func_80034A10_35610`](../functions/func_80034A10_35610.md)
- [`func_801E8E24_5A4D34`](../functions/func_801E8E24_5A4D34.md)
- [`func_80035EEC_36AEC`](../functions/func_80035EEC_36AEC.md)
