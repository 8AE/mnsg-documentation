---
title: "Replace model display pointers"
sidebar_label: "func_8001C3E0_1CFE0"
slug: "/functions/func_8001C3E0_1CFE0"
description: "Applies a display-pointer replacement table to a bound model tree."
---

`func_8001C3E0_1CFE0` · **Function**

Applies a display-pointer replacement table to a bound model tree.

| Runtime address | ROM address | Section |
| --- | --- | --- |
| `0x8001C3E0` | `0x0001CFE0` | `.main` |

Native code size: **680 bytes**.

## Signature

```c
extern int func_8001C3E0_1CFE0(void *object, unsigned int model_ptr,
                               const void *replacement_table);
```

## How it works

Traverses model data and replaces matching display pointers. The native character appearance path uses this for transformations such as Goemon Sudden Impact hair.

Replacement mutates pointed-to model data. To customize one instance without affecting other instances, bind that object to a private writable action-data copy before applying the replacement table.

## Parameters

| Parameter | Type | Description |
| --- | --- | --- |
| `object` | `void *` | Display object with valid model bindings. |
| `model_ptr` | `unsigned int` | Model pointer/selector; the renderer passes zero for its bound model. |
| `replacement_table` | `const void *` | Stock display-pointer replacement table. |

## Return value

Integer success result as tested by the recovered call pattern; exact additional values are not established.

## Usage example

```c
extern void *D_80204048_5BFF58[];

extern int func_8001C3E0_1CFE0(void *object, unsigned int model_ptr,
                               const void *replacement_table);

/* object must bind a private, writable Goemon action-model copy. */
int apply_private_sudden_impact(void *object) {
    if (!object) return 0;
    return func_8001C3E0_1CFE0(object, 0, D_80204048_5BFF58[1]);
}
```

Complete C syntax example using the documented native declarations. Integrate it only at the described engine lifecycle boundary; the game supplies symbol definitions and resident resources.

## Notes

- This mutates model data. Never use it against shared immutable action caches when multiple models need independent appearance.
- Model pointer zero is the call pattern used after the object has been bound; do not infer it means any arbitrary object is valid.

## Related symbols

- [`D_80204048_5BFF58`](../variables/D_80204048_5BFF58.md)
- [`D_80203F34_5BFE44`](../variables/D_80203F34_5BFE44.md)
