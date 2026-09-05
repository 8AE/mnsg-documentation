---
title: "Update Yae projectile flight and impact"
sidebar_label: "func_801EEDF8_5AAD08"
slug: "/functions/func_801EEDF8_5AAD08"
description: "Common updater for already constructed Yae projectile variants. Its second argument is passed through to the native movement helper: zero selects ordinary acceleration, while one permits native target acquisition and homing."
---

`func_801EEDF8_5AAD08` · **Function**

Common updater for already constructed Yae projectile variants. Its second argument is passed through to the native movement helper: zero selects ordinary acceleration, while one permits native target acquisition and homing.

| Runtime address | ROM address | Section |
| --- | --- | --- |
| `0x801EEDF8` | `0x005AAD08` | `.file_11` |

Native code size: **936 bytes**.

## Signature

```c
extern void func_801EEDF8_5AAD08(void *task, int homing_mode);
```

## How it works

Common updater for already constructed Yae projectile variants. Its second argument is passed through to the native movement helper: zero selects ordinary acceleration, while one permits native target acquisition and homing.

The constructor initializes phase byte +0x60 to zero and halfword lifetime +0x62 to 90. This updater decrements lifetime before motion; phase zero with timer 90 identifies the initial flight update.

Collision changes phase to one and initializes model 0x19000420 from the Yae broad file at uniform scale 0.3. The impact texture sequence advances every three ticks and material alpha decreases by 24 per update.

Four native trail slots start at alpha 240, fade by 30 per update and increase uniform scale by 0.006. Impact completion uses the bound model animation length or exhaustion of the trail slots, then requests manager removal.

The routine obtains its display chain from task +0x18 and owner from +0x5C. Task allocation, multiple records, materials, texture cursors and contact state are constructor preconditions.

## Return value

No return value.

## Usage example

```c
#include "modding.h"

static void *updating_task;
static unsigned char observed_phase;

RECOMP_HOOK("func_801EEDF8_5AAD08")
void observe_update_entry(void *task)
{
    updating_task = task;
}

RECOMP_HOOK_RETURN("func_801EEDF8_5AAD08")
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
