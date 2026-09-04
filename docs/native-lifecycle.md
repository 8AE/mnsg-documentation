---
title: Native lifecycle
slug: /native-lifecycle
description: Work safely with room identity, native actors, callbacks, and loaded resources.
---

Native APIs operate on game-owned state. A valid address is only one part of establishing whether an operation is appropriate.

## Room identity and actor readiness

[`D_800C7AB2`](variables/D_800C7AB2.md) identifies the current room. A change means room-scoped state should be discarded or revalidated. It does not prove that actor initialization or resource loading is complete.

Check the task's object pointer, generation, entity identity, and removal state before using a cached actor. Memory pools can reuse the same address for a different actor.

## Loaded resources

[`func_800141C4_14DC4`](functions/func_800141C4_14DC4.md) searches for a loaded file. Its sentinel matters: missing resources return `(void *)-1`, and file ID zero returns null.

```c
extern void *func_800141C4_14DC4(unsigned int file_id);

int resource_is_ready(unsigned int file_id)
{
    void *resource = func_800141C4_14DC4(file_id);
    return resource != 0 && resource != (void *)-1;
}
```

Do not call resource-dependent routines with an unavailable file. A loader's returned cursor is also not necessarily the resource base: consult the specific loader's return-value contract.

## Scheduler context

Some routines operate implicitly on [`D_8016DAB4_16E6B4`](variables/D_8016DAB4_16E6B4.md), the current task. Changing a callback or deleting a task requires the correct scheduler context. Passing an unrelated object pointer does not make those implicit operations target that object.

## Flags and events

The flag [reader](functions/func_800240DC_24CDC.md), [setter](functions/func_80024038_24C38.md), and [clearer](functions/func_80024088_24C88.md) operate on stored bits. Setting a completion bit does not automatically perform an animation, spawn a reward, write a save, or reconstruct an encounter.

Use native state transitions when the full event sequence is required. Use direct flag operations only when their meaning and surrounding state are established.
