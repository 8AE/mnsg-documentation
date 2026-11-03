---
title: "Update the native chain-pipe head"
sidebar_label: "func_801EA0D8_5A5FE8"
slug: "/functions/func_801EA0D8_5A5FE8"
description: "Advances the playable chain-pipe head through extension, retraction, latched travel and completion, including native world collision and marker placement."
---

`func_801EA0D8_5A5FE8` · **Function**

Advances the playable chain-pipe head through extension, retraction, latched travel and completion, including native world collision and marker placement.

| Runtime address | ROM address | Section |
| --- | --- | --- |
| `0x801EA0D8` | `0x005A5FE8` | `.file_11` |

Native code size: **860 bytes**.

## Signature

```c
extern void func_801EA0D8_5A5FE8(void *task, void *object);
```

## How it works

The task is the chain-pipe head. Task +0x5C is its playable owner, +0x18 is the head display object, and +0xBC is the targeting-marker object. The constructor must have initialized the associated links and attack state.

Unsigned phase byte +0x60 uses 0 for extension, 1 for retraction, 2 for a latched endpoint and 3 for completion. Phase 3 sets native removal-request byte +0x65.

At entry it clears native collision slots +0x34 and +0x38. Collision observations needed before this reset must be copied at the scanner boundary rather than read after the head update.

Extension advances the head with velocity fields +0x6C/+0x70/+0x74 and performs a native world query. A world hit that is not the native chain-block entity 0x196 causes retraction and reverses those velocity components.

Retraction counts down the halfword at +0x62, returns the head to its stored player-relative hand offset and marks completion. Latched phase 2 refreshes that rotated hand offset and marks completion when the distance from playable object to head endpoint is at most approximately 8.660254 world units.

The endpoint remains fixed after latch. The update copies head XYZ to the targeting marker; marker visibility also depends on the native targeting path.

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

- This native gameplay update requires complete chain-head state. Do not call it as a spawner or replay it on a display-only player.
- The owner, head object, marker object and native attack state must be live. Preserve ordinary native cleanup and never retain their addresses across task-pool reuse.
- The native entry clears collision slots. Hook timing changes whether a previously registered collision can still be observed.
- Native pull travel is horizontal after the latch helper's initial Y snap. Copying a new endpoint alone does not update the stored movement heading.

## Related symbols

- [`func_801E9AE0_5A59F0`](../functions/func_801E9AE0_5A59F0.md)
- [`func_801EA4E8_5A63F8`](../functions/func_801EA4E8_5A63F8.md)
- [`func_801EA5E4_5A64F4`](../functions/func_801EA5E4_5A64F4.md)
- [`func_801F4C20_5B0B30`](../functions/func_801F4C20_5B0B30.md)
