---
title: "Prepend display records to a task"
sidebar_label: "func_80035DFC_369FC"
slug: "/functions/func_80035DFC_369FC"
description: "Allocates and prepends a chain of records to a task display list."
---

`func_80035DFC_369FC` · **Function**

Allocates and prepends a chain of records to a task display list.

| Runtime address | ROM address | Section |
| --- | --- | --- |
| `0x80035DFC` | `0x000369FC` | `.main` |

Native code size: **240 bytes**.

## Signature

```c
extern void *func_80035DFC_369FC(void *task, short kind, unsigned int count);
```

## How it works

Uses the low eight bits of count, compares the native per-kind capacity against the signed 16-bit active count, then pops records through func_80035D8C.

Prepends each record through task +0x18; initializes the tail at +0x1C only for an empty list. This differs from the appending allocator func_80035EEC.

The capacity table alone does not provide backing records. A failure during a multi-record operation can leave earlier records attached to the task.

## Return value

First allocated record, or null when capacity/allocation fails.

## Usage example

```c
extern void *func_80035DFC_369FC(void *task, short kind, unsigned int count);

void *prepend_one_display(void *task) {
    return task ? func_80035DFC_369FC(task, 2, 1) : 0;
}
```

The example illustrates the native interface and its required state.

## Notes

- Only pass a valid native kind index and a live task. Caller-specific initialization is still required.
