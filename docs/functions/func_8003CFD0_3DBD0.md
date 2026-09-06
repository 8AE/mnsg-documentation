---
title: "Advance the scenario manager"
sidebar_label: "func_8003CFD0_3DBD0"
slug: "/functions/func_8003CFD0_3DBD0"
description: "Runs one native scenario-manager tick, including interpreter input and dialog status."
---

`func_8003CFD0_3DBD0` · **Function**

Runs one native scenario-manager tick, including interpreter input and dialog status.

| Runtime address | ROM address | Section |
| --- | --- | --- |
| `0x8003CFD0` | `0x0003DBD0` | `.main` |

Native code size: **76 bytes**.

## Signature

```c
extern void func_8003CFD0_3DBD0(void *task, void *object);
```

## How it works

This is the recurring scenario-manager callback installed by its initializer. The ordinary scheduler supplies task and object arguments; this implementation saves but does not otherwise read either argument.

While the byte at 0x801C7930 is nonzero, decrement it and return. Otherwise run the shared scenario interpreter and then update scenario/dialog status.

The manager is part of the gameplay task hierarchy and can be suspended by the same execution mask as gameplay. A controlled custom interaction that suppresses the ordinary scheduler may advance its owned scenario once separately, while retaining the correct current-task/resource context.

Input collection, message-window rendering and choice-cursor drawing have their own native paths. Running this callback alone is not a complete dialog initialization or rendering API.

## Parameters

| Parameter | Type | Description |
| --- | --- | --- |
| `task` | `void *` | Native scenario-manager task supplied by the scheduler; not read by this callback itself. |
| `object` | `void *` | Task object argument supplied by the scheduler; not read by this callback itself. |

## Return value

No return value.

## Usage example

```c
#include "modding.h"

/* Native callback observation; arguments are supplied by the scheduler. */
RECOMP_HOOK("func_8003CFD0_3DBD0")
void observe_scenario_tick(void *task, void *object)
{
    (void)task;
    (void)object;
    /* The native callback continues to advance its own interpreter. */
}
```

Observe the recurring manager boundary without advancing the interpreter a second time.

## Notes

- A manual call must not duplicate a tick already performed by the native scheduler.
- The interpreter uses shared globals and may invoke callbacks or task operations. Verify scenario ownership and current-task context before calling it outside ordinary scheduling.
- This function does not allocate or validate message windows.

## Related symbols

- [`func_80034734_35334`](../functions/func_80034734_35334.md)
- [`D_80077860_78460`](../variables/D_80077860_78460.md)
- [`D_80077858_78458`](../variables/D_80077858_78458.md)
- [`D_8016DAB4_16E6B4`](../variables/D_8016DAB4_16E6B4.md)
