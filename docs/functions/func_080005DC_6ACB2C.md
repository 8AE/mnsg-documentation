---
title: "Rotate an active spike chain"
sidebar_label: "func_080005DC_6ACB2C"
slug: "/functions/func_080005DC_6ACB2C"
description: "Advances the active spike-chain object rotation."
---

`func_080005DC_6ACB2C` · **Function**

Advances the active spike-chain object rotation.

| Runtime address | ROM address | Section |
| --- | --- | --- |
| `0x080005DC` | `0x006ACB2C` | `.file_24` |

Native code size: **20 bytes**.

## Interface

A complete callable prototype has not been established. Use the observation or callback-identity pattern in the example rather than guessing the native arguments.

## How it works

Adds the 32-bit angular step at task +0xD0 to the unsigned 16-bit object yaw at +0x16.

The active spike-chain family uses actor and entity ID 0x198. Common actor post-processing follows the angular update.

## Parameters

| Parameter | Type | Description |
| --- | --- | --- |
| `task` | `void *` | Live native actor task; the scheduler places the current task in D_8016DAB4_16E6B4. |
| `object` | `void *` | Native object associated with the task, normally the pointer at task +0x18; included where the two-argument callback declaration is established. |

## Return value

No return value is used by the documented task-callback convention.

## Usage example

```c
#include "modding.h"

static unsigned short last_entity;

RECOMP_HOOK("func_080005DC_6ACB2C")
void observe_native_state(void *task)
{
    if (!task) return;
    last_entity = *(volatile unsigned short *)((char *)task + 0x5E);
}
```

Observe entry into this native routine and sample the task entity field. The original function continues executing in its normal scheduler context.

## Notes

- The native callback applies one angular step per invocation.
- Resolve the full ROM-qualified overlay symbol; a shared 0x080... address alone does not identify the loaded routine.
- Use a live task of the documented family. Task pointers and callback slots follow the 32-bit target ABI.

## Related symbols

- [`D_8016DAB4_16E6B4`](../variables/D_8016DAB4_16E6B4.md)
