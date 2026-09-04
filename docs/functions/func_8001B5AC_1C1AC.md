---
title: "Read the bound model animation length"
sidebar_label: "func_8001B5AC_1C1AC"
slug: "/functions/func_8001B5AC_1C1AC"
description: "Resolves a display object model command and returns its animation frame count."
---

`func_8001B5AC_1C1AC` · **Function**

Resolves a display object model command and returns its animation frame count.

| Runtime address | ROM address | Section |
| --- | --- | --- |
| `0x8001B5AC` | `0x0001C1AC` | `.main` |

Native code size: **248 bytes**.

## Signature

```c
extern float func_8001B5AC_1C1AC(void *model);
```

## How it works

Reads the encoded model pointer at object+0x2C, accepts supported pointer kinds, resolves positive segmented pointers through object segment bases, and returns the low byte of the resolved header as a float.

Unsupported model encodings and a zero model pointer return 0.0. Use a positive result to bound animation frame +0x28 or normalize animation phase.

## Parameters

| Parameter | Type | Description |
| --- | --- | --- |
| `object` | `void *` | Live model/display object with initialized segment bases. |

## Return value

Frame count as float, or 0.0 for unsupported/empty model encodings.

## Usage example

```c
extern float func_8001B5AC_1C1AC(void *model);

/* Caller supplies a live display object with valid resident model bindings. */
void wrap_model_frame(void *object) {
    if (!object) return;
    float count = func_8001B5AC_1C1AC(object);
    if (count > 0.0f) {
        float *frame = (float *)((unsigned char *)object + 0x28);
        if (*frame >= count) *frame = 0.0f;
    }
}
```

Complete C syntax example using the documented native declarations. Integrate it only at the described engine lifecycle boundary; the game supplies symbol definitions and resident resources.

## Notes

- Pass a live display/model object, not a player task.
- The function does not validate that an arbitrary pointer is safe to dereference. Check object lifetime and resource binding first.
- Zero is a valid unsupported/empty model result; never divide by it when normalizing animation phase.

## Related symbols

- [`D_801FC60C_5B851C`](../variables/D_801FC60C_5B851C.md)
- [`func_8000DBF0_E7F0`](../functions/func_8000DBF0_E7F0.md)
- [`D_80203F34_5BFE44`](../variables/D_80203F34_5BFE44.md)
