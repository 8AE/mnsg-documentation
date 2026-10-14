---
title: "Create a native sprite queue"
sidebar_label: "func_800103DC_10FDC"
slug: "/functions/func_800103DC_10FDC"
description: "Allocates a persistent native sprite-queue child and its fixed-capacity record buffer."
---

`func_800103DC_10FDC` · **Function**

Allocates a persistent native sprite-queue child and its fixed-capacity record buffer.

| Runtime address | ROM address | Section |
| --- | --- | --- |
| `0x800103DC` | `0x00010FDC` | `.main` |

Native code size: **464 bytes**.

## Signature

```c
extern int func_800103DC_10FDC(void *task, int capacity, unsigned char display_layer);
```

## How it works

Creates a child of native task kind 1 and allocates a backing buffer for the requested record capacity. The global native registry supports at most 16 queues.

The queue persists across collection passes until its storage is explicitly released or scene-level native cleanup runs.

The queue index is consumed by reset, append, finalize, and cleanup calls.

## Parameters

| Parameter | Type | Description |
| --- | --- | --- |
| `task` | `void *` | Native task that owns the queue child. |
| `capacity` | `int` | Number of sprite records requested for this queue's backing buffer. |
| `display_layer` | `unsigned char` | Display layer value passed to the queue child; other layer semantics are not established here. |

## Return value

A queue index on success, or -1 if queue creation or record-buffer allocation fails.

## Usage example

```c
extern int func_800103DC_10FDC(void *task, int capacity, unsigned char display_layer);

int create_hud_sprite_queue(void *task)
{
    return func_800103DC_10FDC(task, 8, 10);
}
```

Create the queue with a native owner task, a capacity no greater than 16, and the layer value required by the caller's draw path.

## Notes

- The queue registry supports at most 16 live queues. Append no more records than this queue's requested capacity; append failure is reported as -1.
- A newly created sprite queue's visibility during a scene's first introductory animation has not been tested.

## Related symbols

- [`func_80010358_10F58`](../functions/func_80010358_10F58.md)
- [`func_800106F0_112F0`](../functions/func_800106F0_112F0.md)
- [`func_800105AC_111AC`](../functions/func_800105AC_111AC.md)
- [`func_80010374_10F74`](../functions/func_80010374_10F74.md)
