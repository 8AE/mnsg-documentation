---
title: "Read a game flag"
sidebar_label: "func_800240DC_24CDC"
slug: "/functions/func_800240DC_24CDC"
description: "Tests one bit in the game's packed flag bank at D_8015C608_15D208. Returns zero when the flag is clear, or the bit mask when it is set. Use this to query progression, encounter, and event state without changing it."
---

`func_800240DC_24CDC` · **Function**

Tests one bit in the game's packed flag bank at D_8015C608_15D208. Returns zero when the flag is clear, or the bit mask when it is set. Use this to query progression, encounter, and event state without changing it.

| Runtime address | ROM address | Section |
| --- | --- | --- |
| `0x800240DC` | `0x00024CDC` | `.main` |

Native code size: **80 bytes**.

## Signature

```c
extern int func_800240DC_24CDC(int flag_id);
```

## How it works

For a nonnegative flag ID, the function selects byte (flag_id / 8) & 0xFF, then ANDs it with 1 << (flag_id & 7). Consequently a set bit can return 1, 2, 4, 8, 16, 32, 64, or 128. The native return is not a normalized Boolean.

The bank covers 256 bytes, or 2,048 bit positions. The native implementation masks the byte index rather than validating the input. IDs at or above 0x800 alias earlier bytes; negative arguments follow the compiler's signed division and remainder path and are not meaningful public inputs.

Use the reader to query encounter-active, defeated, reward, or other documented progression flags. Reading a bit does not execute the event associated with it.

## Parameters

| Parameter | Type | Description |
| --- | --- | --- |
| `flag_id` | `int` | Bit index into the game flag bank. Pass a known game flag in the range 0x000–0x7FF, not a byte offset or bit mask. |

## Return value

Zero if clear; the nonzero bit mask if set. Compare the result with zero.

## Usage example

```c
extern int func_800240DC_24CDC(int flag_id);

/* Query a known flag ID supplied by your encounter logic. */
static int game_flag_is_set(unsigned int flag_id)
{
    if (flag_id >= 0x800u) {
        return 0;
    }
    return func_800240DC_24CDC((int)flag_id) != 0;
}
```

This wrapper validates the bank range and normalizes the native mask to 0 or 1. The game owns the flag bank; the wrapper only reads it.

## Notes

- Do not compare a set flag with == 1; flags whose bit position is not zero return larger masks.
- The native function does not bounds-check IDs. Confirm what a flag controls before relying on it.

## Native implementation

Live Ghidra decompilation of resident address 0x800240DC, captured 2026-09-04. Displayed logic is simplified for nonnegative IDs; the native function also contains signed division/remainder adjustments.

```c
/* Equivalent logic for valid, nonnegative IDs; not a replacement patch. */
unsigned int byte_index = ((unsigned int)flag_id >> 3) & 0xFFu;
unsigned int mask = 1u << ((unsigned int)flag_id & 7u);
return D_8015C608_15D208[byte_index] & mask;
```

## Related symbols

- [`func_80024038_24C38`](../functions/func_80024038_24C38.md)
- [`func_80024088_24C88`](../functions/func_80024088_24C88.md)
- [`D_8015C608_15D208`](../variables/D_8015C608_15D208.md)
- [`D_800C7AB2`](../variables/D_800C7AB2.md)
