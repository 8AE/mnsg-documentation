---
title: "Stage actor allocation scale"
sidebar_label: "D_80239AFC_5F4FCC"
slug: "/variables/D_80239AFC_5F4FCC"
description: "Floating-point uniform scale value used by the native stage-actor allocation path."
---

`D_80239AFC_5F4FCC` · **Variable**

Floating-point uniform scale value used by the native stage-actor allocation path.

| Runtime address | ROM address | Section |
| --- | --- | --- |
| `0x80239AFC` | `0x005F4FCC` | `.file_12` |

## Signature

```c
extern float D_80239AFC_5F4FCC;
```

## How it works

The actor manager supplies this value as all three scale arguments to func_8003555C_3615C while iterating stage actor instances.

The persistent actor instance branch uses the adjacent scale value at 0x80239AF8. The numeric value of D_80239AFC has not been verified here.

Passed as x,y,z scale to func_8003555C when constructing a room actor before instance-specific initialization.

The demonstrated read role is established. A broader configuration/ownership role for writes is not.

## Usage example

```c
extern float D_80239AFC_5F4FCC;

float default_enemy_spawn_scale(void)
{
    return D_80239AFC_5F4FCC;
}
```

The example shows the documented native data layout or call sequence. Use it only while the relevant game state and resources are valid.

## Notes

- This is native scene/overlay state. Validate actor IDs and resource lifetime; do not assume an unsized extern provides bounds.

## Related symbols

- [`func_80218A54_5D3F24`](../functions/func_80218A54_5D3F24.md)
- [`func_8003555C_3615C`](../functions/func_8003555C_3615C.md)
