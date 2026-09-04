---
title: "Current room actor instance pointer"
sidebar_label: "D_8015CDDC"
slug: "/variables/D_8015CDDC"
description: "Pointer to the room actor instance currently being processed by native spawning."
---

`D_8015CDDC` · **Variable**

Pointer to the room actor instance currently being processed by native spawning.

| Runtime address | ROM address | Section |
| --- | --- | --- |
| `0x8015CDDC` | — | `ABSOLUTE_SYMS` |

## Signature

```c
extern void *D_8015CDDC;
```

## How it works

The actor manager assigns this scratch pointer as it iterates persistent and stage actor instance arrays.

The partial instance layout is signed short xyz position, signed short pitch/yaw/roll, definition pointer at +0x0C and spawned byte at +0x10.

Can be compared with the func_80218A54 instance argument to establish that a callback belongs to the current room-spawn context.

It is shared transient context, not a permanent pointer identifying every spawned actor.

## Known values

### Actor instance fields {#instance-fields}

Offsets are relative to the actor instance pointed to by this variable, not to the pointer storage. A null definition pointer terminates the instance list during native actor-manager traversal.

| Offset | Storage type | Meaning |
| --- | --- | --- |
| `+0x00 / +0x02 / +0x04` | `int16_t` × 3 | Spawn position X, Y and Z. |
| `+0x06 / +0x08 / +0x0A` | `int16_t` × 3 | Spawn rotation: pitch, yaw and roll. |
| `+0x0C` | 32-bit pointer | Actor definition record; zero terminates the native instance list. |
| `+0x10` | `uint8_t` | Spawn-state byte. A full raw-value interpretation is not established. |

## Usage example

```c
extern void *D_8015CDDC;

int is_current_room_spawn(void *instance)
{
    return instance && D_8015CDDC == instance;
}
```

The example shows the documented native data layout or call sequence. Use it only while the relevant game state and resources are valid.

## Notes

- This is current-spawn context, not a list of every live actor. Nested spawn work can replace it.
- This is native scene/overlay state. Validate actor IDs and resource lifetime; do not assume an unsized extern provides bounds.

## Related symbols

- [`func_80218A54_5D3F24`](../functions/func_80218A54_5D3F24.md)
- [`func_8003555C_3615C`](../functions/func_8003555C_3615C.md)
- [`D_8015CDE0`](../variables/D_8015CDE0.md)
