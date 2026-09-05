---
title: "Update the Sasuke kunai effect"
sidebar_label: "func_801EFBDC_5ABAEC"
slug: "/functions/func_801EFBDC_5ABAEC"
description: "Common updater for existing thrown/fired Sasuke weapon variants. The native wrapper supplies a trail-slot count and an unsigned 16-bit emission interval."
---

`func_801EFBDC_5ABAEC` · **Function**

Common updater for existing thrown/fired Sasuke weapon variants. The native wrapper supplies a trail-slot count and an unsigned 16-bit emission interval.

| Runtime address | ROM address | Section |
| --- | --- | --- |
| `0x801EFBDC` | `0x005ABAEC` | `.file_11` |

Native code size: **920 bytes**.

## Signature

```c
extern void func_801EFBDC_5ABAEC(void *task, int trail_count, unsigned short trail_interval);
```

## How it works

Common updater for existing thrown/fired Sasuke weapon variants. The native wrapper supplies a trail-slot count and an unsigned 16-bit emission interval.

The constructor initializes phase byte +0x60 to zero and lifetime halfword +0x62 to 60. The updater decrements lifetime and advances the main object by task velocity +0x6C/+0x70/+0x74.

Contact or world collision changes phase to the native layered impact effect. Its two material layers advance animation and fade alpha by 12 per update before the manager removes the task.

Phase zero with timer 60 identifies entry to the first flight update. A returned phase change means the object is already in impact, rather than an initial flight pose.

## Return value

No return value.

## Usage example

```c
#include "modding.h"

static void *updating_task;
static unsigned char observed_phase;

RECOMP_HOOK("func_801EFBDC_5ABAEC")
void observe_update_entry(void *task)
{
    updating_task = task;
}

RECOMP_HOOK_RETURN("func_801EFBDC_5ABAEC")
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
