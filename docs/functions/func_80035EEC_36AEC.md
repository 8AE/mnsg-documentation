---
title: "Allocate task-owned pool records"
sidebar_label: "func_80035EEC_36AEC"
slug: "/functions/func_80035EEC_36AEC"
description: "Allocates a bounded chain of native records and appends them to a task."
---

`func_80035EEC_36AEC` · **Function**

Allocates a bounded chain of native records and appends them to a task.

| Runtime address | ROM address | Section |
| --- | --- | --- |
| `0x80035EEC` | `0x00036AEC` | `.main` |

Native code size: **240 bytes**.

## Signature

```c
extern void *func_80035EEC_36AEC(void *task, short kind, unsigned int count);
```

## How it works

Uses count & 0xFF and checks the requested kind capacity minus its active count. Each record is obtained through func_80035D8C. Task+0x18 holds the list head and task+0x1C the tail.

The first allocated record is returned. A later allocation failure returns null even if earlier records have already been appended, so this is not an all-or-nothing transaction.

## Parameters

| Parameter | Type | Description |
| --- | --- | --- |
| `task` | `void *` | Valid owning task with native record-list fields. |
| `kind` | `short` | Native pool-record kind. |
| `count` | `unsigned int` | Requested record count; native code uses the low byte. |

## Return value

First allocated record; null for zero count, capacity failure or pool exhaustion.

## Usage example

```c
extern void *func_80035EEC_36AEC(void *task, short kind, unsigned int count);

/* task must be a live native owner with an initialized record list. */
void *allocate_task_display_record(void *task) {
    if (!task) return 0;
    return func_80035EEC_36AEC(task, 2, 1);
}
```

Complete C syntax example using the documented native declarations. Integrate it only at the described engine lifecycle boundary; the game supplies symbol definitions and resident resources.

## Notes

- Count is truncated to eight bits; 256 becomes zero.
- A mid-loop failure returns null after earlier records have already been appended. It is not an all-or-nothing allocator.
- Raising a limit alone does not create more free-list backing records.

## Related symbols

- [`func_80035D8C_3698C`](../functions/func_80035D8C_3698C.md)
- [`func_8000DBF0_E7F0`](../functions/func_8000DBF0_E7F0.md)
- [`D_8006D350_6DF50`](../variables/D_8006D350_6DF50.md)
