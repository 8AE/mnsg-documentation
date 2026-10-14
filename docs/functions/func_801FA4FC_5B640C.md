---
title: "Record a native room-entry request"
sidebar_label: "func_801FA4FC_5B640C"
slug: "/functions/func_801FA4FC_5B640C"
description: "Stores a room, arrival coordinates, camera value, and marker mode in native transition state."
---

`func_801FA4FC_5B640C` · **Function**

Stores a room, arrival coordinates, camera value, and marker mode in native transition state.

| Runtime address | ROM address | Section |
| --- | --- | --- |
| `0x801FA4FC` | `0x005B640C` | `.file_11` |

Native code size: **168 bytes**.

## Signature

```c
void func_801FA4FC_5B640C(uint16_t room_id, int16_t x, int16_t y, int16_t z, uint16_t camera, char marker_mode);
```

## How it works

Stores the five 16-bit request values in native transition state, then selects marker 1 for a zero marker_mode or marker 4 for any nonzero marker_mode.

The Goemon and Sasuke minigame launchers call this helper with marker_mode 1 after saving the current player position and facing.

## Parameters

| Parameter | Type | Description |
| --- | --- | --- |
| `room_id` | `uint16_t` | Raw destination room ID. The verified minigame callers use 0x01E0 and 0x01E2. |
| `x` | `int16_t` | Raw arrival X value; the verified callers include a negative value. |
| `y` | `int16_t` | Raw arrival Y value. |
| `z` | `int16_t` | Raw arrival Z value; the verified Sasuke caller uses -357. |
| `camera` | `uint16_t` | Raw camera value supplied by the caller; the verified calls use 0 and 0x0060. |
| `marker_mode` | `char` | A zero value stores marker 1; a nonzero value stores marker 4. Broader marker semantics are not established here. |

## Return value

No return value.

## Usage example

```c
#include <stdint.h>

extern void func_801FA4FC_5B640C(uint16_t room_id, int16_t x, int16_t y, int16_t z, uint16_t camera, char marker_mode);

/* These are the transition request values used by the Sasuke launcher. */
void record_sasuke_minigame_entry(void)
{
    func_801FA4FC_5B640C(0x01E2, -213, 0, -357, 0x0060, 1);
}
```

This reproduces the helper's observed field values only. The native Sasuke launcher also snapshots the current player position and facing before making this call.

## Notes

- This helper records transition state; its implementation alone does not establish a complete room transfer or the lifecycle that consumes the fields.
- Use the exact values and surrounding native sequence verified for the intended launcher. Do not treat this call as a generic teleport API.

## Related symbols

- [`func_800370E8_37CE8`](../functions/func_800370E8_37CE8.md)
- [`func_800371B4_37DB4`](../functions/func_800371B4_37DB4.md)
- [`func_801FA420_5B6330`](../functions/func_801FA420_5B6330.md)
