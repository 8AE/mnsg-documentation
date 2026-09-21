---
title: "Animate and retire an equipment shine"
sidebar_label: "func_80213A9C_5CEF6C"
slug: "/functions/func_80213A9C_5CEF6C"
description: "Advances local shine color state and deletes the current effect task when its termination byte is nonzero."
---

`func_80213A9C_5CEF6C` · **Function**

Advances local shine color state and deletes the current effect task when its termination byte is nonzero.

| Runtime address | ROM address | Section |
| --- | --- | --- |
| `0x80213A9C` | `0x005CEF6C` | `.file_12` |

Native code size: **132 bytes**.

## Signature

```c
extern void func_80213A9C_5CEF6C(void *task);
```

## How it works

Updates the shine using its local color/cycle bytes +0xD4 and +0xD5.

A nonzero byte at task +0xD0 triggers deletion through the current-task lifecycle. Equipment pickup callbacks signal this byte on their own shine.

## Usage example

```c
#include "modding.h"

static volatile unsigned char observed_value;

RECOMP_HOOK("func_80213A9C_5CEF6C")
void observe_native_state(void *task)
{
    if (!task) return;
    observed_value = *(volatile unsigned char *)((char *)task + 0xD0);
}
```

The normal scheduler still performs animation and deletion once.

## Notes

- This continuation depends on the current scheduled task. Do not call it directly to retire a different effect.
- Preserve local color and texture-animation state; the termination byte is a lifecycle signal, not an animation phase.

## Related symbols

- [`func_802139E0_5CEEB0`](../functions/func_802139E0_5CEEB0.md)
