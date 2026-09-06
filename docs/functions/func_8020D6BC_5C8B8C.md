---
title: "Load normal stage resources"
sidebar_label: "func_8020D6BC_5C8B8C"
slug: "/functions/func_8020D6BC_5C8B8C"
description: "Loads normal stage resources before later actor and effect setup."
---

`func_8020D6BC_5C8B8C` · **Function**

Loads normal stage resources before later actor and effect setup.

| Runtime address | ROM address | Section |
| --- | --- | --- |
| `0x8020D6BC` | `0x005C8B8C` | `.file_12` |

Native code size: **104 bytes**.

## Interface

A complete callable prototype has not been established. Use the observation or callback-identity pattern in the example rather than guessing the native arguments.

## How it works

Return from this routine provides a boundary after ordinary stage resources have completed loading. Additional native file resources can then be looked up or loaded through the scene registry.

The complete internal loading sequence and native argument/return signature are not established here. A zero-argument return hook does not imply that the native function has no parameters.

An entry hook can invalidate state tied to the preceding stage before resources are rebuilt. A return hook observes completion of this stage-resource load, including a new visit that reloads the same numeric room ID. Later player/actor initialization still needs its own validity checks.

Identified as the gameplay stage resource-loading routine. Its return is an appropriate boundary for acquiring additional resident render resources after the normal scene resources are available.

Treat registry pointers and scene allocations as belonging to the current stage. Invalidate retained scene pointers before loading or binding resources for another stage. The complete native implementation is not reproduced here.

## Usage example

```c
#include "modding.h"
extern void *func_800141C4_14DC4(unsigned int);
extern void *func_80013B14_14714(unsigned int);

RECOMP_HOOK_RETURN("func_8020D6BC_5C8B8C")
void prepare_ryo_effect_resource(void)
{
    void *p = func_800141C4_14DC4(0x3B);
    if (!p || p == (void *)(unsigned long)0xFFFFFFFFu)
        func_80013B14_14714(0x3B);
}
```

The example shows the documented native data layout or call sequence. Use it only while the relevant game state and resources are valid.

## Notes

- Do not use the return hook alone as proof that the local player is alive, ordinary gameplay has resumed, or interactive UI is safe to open.
- Loading broad resources from a render/update callback can collide with the native resource lifecycle.
- Overlay addresses and cached resource pointers cease to be valid across stage teardown.

## Related symbols

- [`func_80013B14_14714`](../functions/func_80013B14_14714.md)
- [`func_800141C4_14DC4`](../functions/func_800141C4_14DC4.md)
- [`D_80167FC0_168BC0`](../variables/D_80167FC0_168BC0.md)
