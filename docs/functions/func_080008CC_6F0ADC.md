---
title: "Read the Ebisumaru HUD countdown in seconds"
sidebar_label: "func_080008CC_6F0ADC"
slug: "/functions/func_080008CC_6F0ADC"
description: "Converts the signed raw HUD timer frames to whole seconds using native signed division."
---

`func_080008CC_6F0ADC` · **Function**

Converts the signed raw HUD timer frames to whole seconds using native signed division.

| Runtime address | ROM address | Section |
| --- | --- | --- |
| `0x080008CC` | `0x006F0ADC` | `.file_42` |

## Signature

```c
int32_t func_080008CC_6F0ADC(void *hud_task);
```

## How it works

Loads the signed 32-bit timer word at HUD task +0x80, divides by 30 with signed integer division, and returns the quotient.

The challenge controller tests this whole-seconds result against zero. With the nonnegative countdown, the failure threshold is fewer than 30 raw frames remaining, not only a raw value of zero.

## Parameters

| Parameter | Type | Description |
| --- | --- | --- |
| `hud_task` | `void *` | HUD task with signed timer word at +0x80. |

## Return value

Signed whole seconds from HUD task +0x80 divided by 30; it does not return the raw frame count.

## Usage example

```c
#include <stdint.h>

extern int32_t func_080008CC_6F0ADC(void *);

int32_t read_hud_countdown_seconds(void *hud_task)
{
    return hud_task ? func_080008CC_6F0ADC(hud_task) : 0;
}
```

Returns whole seconds, not raw timer frames.

## Notes

- This helper reads timer state; it does not advance the scheduled HUD callback or change the countdown.

## Related symbols

- [`func_080005DC_6F07EC`](../functions/func_080005DC_6F07EC.md)
- [`func_080008B8_6F0AC8`](../functions/func_080008B8_6F0AC8.md)
- [`func_08001954_6F1B64`](../functions/func_08001954_6F1B64.md)
