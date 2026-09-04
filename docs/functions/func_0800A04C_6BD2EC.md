---
title: "Emit Congo breath flames"
sidebar_label: "func_0800A04C_6BD2EC"
slug: "/functions/func_0800A04C_6BD2EC"
description: "Emits Congo breath flames according to the native world-frame phase."
---

`func_0800A04C_6BD2EC` · **Function**

Emits Congo breath flames according to the native world-frame phase.

| Runtime address | ROM address | Section |
| --- | --- | --- |
| `0x0800A04C` | `0x006BD2EC` | `.file_29` |

Native code size: **476 bytes**.

## Interface

A complete callable prototype has not been established. Use the observation or callback-identity pattern in the example rather than guessing the native arguments.

## How it works

Uses world_frame % 15. Phase 0 emits at forward offset 60 with flags 0x10; phase 5 uses offset 55 and flags 0x20; phase 10 uses offset 58 and flags 0x40. Other phases emit nothing.

Allocates a kind-10 child at owner-local offset (0,35,forward_offset), uses initializer func_08000DCC_6B406C and installs resource file 0x1D and owner context.

## Parameters

| Parameter | Type | Description |
| --- | --- | --- |
| `task` | `void *` | Native task supplied at routine entry. Only this consumed argument is established here; additional native parameters have not been confirmed. |

## Return value

No return value is used by the documented task-callback convention.

## Usage example

```c
#include "modding.h"

static unsigned short last_entity;

RECOMP_HOOK("func_0800A04C_6BD2EC")
void observe_native_state(void *task)
{
    if (!task) return;
    last_entity = *(volatile unsigned short *)((char *)task + 0x5E);
}
```

Observe entry into this native routine and sample the task entity field. The original function continues executing in its normal scheduler context.

## Notes

- The phase is based on the shared world clock, so repeated invocations on the same eligible frame can duplicate the same emission.
- Resolve the full ROM-qualified overlay symbol; a shared 0x080... address alone does not identify the loaded routine.
- Use a live task of the documented family. Task pointers and callback slots follow the 32-bit target ABI.

## Related symbols

- [`D_8016DAB4_16E6B4`](../variables/D_8016DAB4_16E6B4.md)
