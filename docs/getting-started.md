---
title: Getting started
slug: /getting-started
description: Look up native Goemon functions and variables and use their C interfaces.
---

This reference describes native functions and global variables in the **US recompilation of Mystical Ninja Starring Goemon**. Start with a symbol name, a hexadecimal address, or a behavior you want to understand.

## Find a symbol

Use the search bar or the [symbol explorer](/reference). Exact names such as `func_800240DC_24CDC` and `D_800C7AB2` appear first. You can also search for “room”, “flag”, “animation”, or a partial address.

- [Functions](functions/index.md) describe calls, return values, and native side effects.
- [Variables](variables/index.md) describe storage, types, and valid access patterns.

Variable pages include **Known values** tables where a mapping has been established. These show raw hexadecimal and decimal values alongside their meanings, or field offsets and types for structured storage. Table headings distinguish a stored value from an array index, flag ID, or bit mask. Unlisted values have no established interpretation in this reference.

Start with [room IDs](variables/D_800C7AB2.md#known-values), [save flags and counters](variables/D_8015C608_15D208.md#known-values), or [character values](variables/D_8015C5D8_15D1D8.md#known-values). Known value names are also searchable.

## Understand the interface

Each page explains what the symbol does, how it works, and how to use it from C. Examples include the required declarations. A native pointer or callback may require an already initialized actor, a loaded resource, or a particular game state; read the notes before using it.

The exported symbol name is the linkable name. Keep its full suffix. Different overlay functions can share a runtime address, so use the **symbol name, ROM address, and section together** when identifying a routine.

Some native types and individual state-machine callbacks remain only partly understood. Their pages state the known behavior and the limits of the recovered interface.

## Read a game flag

The flag reader returns a bit mask. Compare it with zero to obtain a Boolean result.

```c
extern int func_800240DC_24CDC(int flag_id);

int game_flag_is_set(unsigned int flag_id)
{
    if (flag_id >= 0x800u) return 0;
    return func_800240DC_24CDC((int)flag_id) != 0;
}
```

[Read the complete flag API](functions/func_800240DC_24CDC.md).

## Observe an update

Your recompilation project's `modding.h` provides the hook macros. An entry hook observes the start of a native function; a return hook runs after it returns. The system-step dispatcher is a useful recurring observation point.

```c
#include "modding.h"

extern unsigned short D_800C7AB2;
static unsigned short observed_room;

RECOMP_HOOK_RETURN("func_80002040_2C40")
void observe_room(void)
{
    observed_room = D_800C7AB2;
}
```

A parameterless observation callback does not establish the native function's own argument list. A replacement declared with `RECOMP_PATCH` must preserve the native ABI and required behavior.

Continue with [native lifecycle](native-lifecycle.md) for room transitions, actor validity, and resource loading.
