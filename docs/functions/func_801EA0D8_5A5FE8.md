---
title: "Update the charged Goemon coin"
sidebar_label: "func_801EA0D8_5A5FE8"
slug: "/functions/func_801EA0D8_5A5FE8"
description: "Updates the existing charged-coin display and native phase machine, including flight, contact, return and removal behavior."
---

`func_801EA0D8_5A5FE8` · **Function**

Updates the existing charged-coin display and native phase machine, including flight, contact, return and removal behavior.

| Runtime address | ROM address | Section |
| --- | --- | --- |
| `0x801EA0D8` | `0x005A5FE8` | `.file_11` |

Native code size: **860 bytes**.

## Signature

```c
extern void func_801EA0D8_5A5FE8(void *task, void *object);
```

## How it works

Updates the existing charged-coin display and native phase machine, including flight, contact, return and removal behavior.

The native constructor initializes phase byte +0x60 and timer halfword +0x62 to zero. The first flight update begins with those values and can immediately change phase after a hit.

Task +0x5C is the owning player, +0x18 is the main display object, and +0x6C/+0x70/+0x74 are the native velocity fields. Additional owned records and attack descriptors must already exist.

## Return value

No return value.

## Usage example

```c
#include "modding.h"

static void *updating_task;
static unsigned char observed_phase;

RECOMP_HOOK("func_801EA0D8_5A5FE8")
void observe_update_entry(void *task)
{
    updating_task = task;
}

RECOMP_HOOK_RETURN("func_801EA0D8_5A5FE8")
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
