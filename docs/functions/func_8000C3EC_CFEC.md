---
title: "Advance a native message-window text line"
sidebar_label: "func_8000C3EC_CFEC"
slug: "/functions/func_8000C3EC_CFEC"
description: "Moves the selected native window text cursor to the next line."
---

`func_8000C3EC_CFEC` · **Function**

Moves the selected native window text cursor to the next line.

| Runtime address | ROM address | Section |
| --- | --- | --- |
| `0x8000C3EC` | `0x0000CFEC` | `.main` |

Native code size: **68 bytes**.

## Signature

```c
extern void func_8000C3EC_CFEC(int slot);
```

## How it works

Resets the horizontal text cursor and advances the vertical text position by the line-step value stored in the native window.

## Parameters

| Parameter | Type | Description |
| --- | --- | --- |
| `slot` | `int` | Allocated native message-window slot, 0 through 2. |

## Return value

No return value.

## Usage example

```c
extern void func_8000C3EC_CFEC(int slot);

void begin_next_text_line(int slot)
{
    func_8000C3EC_CFEC(slot);
}
```

Call between glyph sequences to place the next sequence on a new native text line.

## Notes

- Use only with an allocated native window slot.

## Related symbols

- [`D_80167C48_168848`](../variables/D_80167C48_168848.md)
- [`func_8000D060_DC60`](../functions/func_8000D060_DC60.md)
