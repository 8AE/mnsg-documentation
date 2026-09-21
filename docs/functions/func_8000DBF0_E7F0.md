---
title: "Attach a model/display object to a task"
sidebar_label: "func_8000DBF0_E7F0"
slug: "/functions/func_8000DBF0_E7F0"
description: "Allocates and initializes a kind-2 model/display object beneath an engine task."
---

`func_8000DBF0_E7F0` · **Function**

Allocates and initializes a kind-2 model/display object beneath an engine task.

| Runtime address | ROM address | Section |
| --- | --- | --- |
| `0x8000DBF0` | `0x0000E7F0` | `.main` |

Native code size: **276 bytes**.

## Signature

```c
extern void *func_8000DBF0_E7F0(void *task, unsigned int model_ptr, unsigned int anim_ptr,
                                float x, float y, float z,
                                short rot_x, short rot_y, short rot_z,
                                float scale_x, float scale_y, float scale_z,
                                short seg8_file_id, short seg9_file_id);
```

## How it works

Calls func_80035EEC_36AEC(task, 2, 1), then writes position at +0x08/+0x0C/+0x10, signed rotations at +0x14/+0x16/+0x18, scale at +0x1C/+0x20/+0x24, animation frame at +0x28, model command at +0x2C and animation context at +0x30.

Initializes file IDs at +0x34 and +0x3C and runs native segment binding. A zero model command starts hidden. For the clothed playable-character assets, render-mode byte +0x05 must be set explicitly to 2; this allocator does not initialize that byte.

This higher-level constructor explicitly initializes display bytes +0x64 and +0x65 to zero. Other native constructors that allocate through func_80035EEC_36AEC can retain the kind-2 reset value +0x65 = 1, which is also visible.

The third argument at object +0x30 can be a material display list, including a task-owned primitive/environment-color wrapper; its meaning depends on the model renderer. Preserve native texture alpha when duplicating a translucent display object.

The six file/base pairs occupy +0x34/+0x38 through +0x5C/+0x60. The constructor sets segment A file ID (+0x44) from system +0xC2D90 and clears the final three file IDs. Native texture animation may subsequently change a segment base to a frame within a loaded asset.

The first Impact cursor is created by func_801CCA5C_5F7E3C with model command 0x4800A1E0, material D_8020A728_635B08, file 0x4A8, uniform scale 0.2 and render mode 9. Its aim is represented by native X/Y rotations. Model 0x480099F0 with material D_8020A2D0_6356B0 is instead the full-screen damage flash.

The Impact cursor material at D_8020A728_635B08 selects TEXEL0 for both RGB and alpha in both combiner cycles (FCFFFFFF FFFCF279). A primitive-color command alone does not tint it. A color override must also change the RGB combiner while preserving TEXEL0 alpha to retain the transparent reticle silhouette.

Native segment binding skips file-zero pairs without clearing their base pointers, so reused objects may contain stale data. In file_13, FUN_801D32D4 and FUN_801D34D0 also write live animated-texture bases into slots 3..5 without setting file IDs. A zero file ID alone does not prove that a base is unused; resolve the pointer within resident assets and account for the renderer before preserving or discarding it.

Some native translucent materials are per-task display-list wrappers. func_8000E030_EC30 writes a 32-byte wrapper at task +0xC8: a material-list call, primitive RGBA, environment RGBA and an end command. It writes back the data cache and returns task +0xC8. Its ten arguments are task, material, primitive R/G/B/A and environment R/G/B/A; each color channel is packed into one byte. Native effects can tag the returned address with 0x60000000. The primitive and environment alpha values are independent.

## Parameters

| Parameter | Type | Description |
| --- | --- | --- |
| `task` | `void *` | Owning native task. |
| `model_ptr` | `unsigned int` | Encoded model-command pointer; zero starts hidden. |
| `anim_ptr` | `unsigned int` | Animation/render context pointer. |
| `x, y, z` | `float` | World position. |
| `rot_x, rot_y, rot_z` | `short` | Native signed-angle rotations. |
| `scale_x, scale_y, scale_z` | `float` | Scale on each axis. |
| `seg8_file_id, seg9_file_id` | `short` | File IDs used to initialize object segment bindings. |

## Return value

Display object pointer, or null on allocation failure.

## Usage example

```c
extern void *func_8000DBF0_E7F0(void *task, unsigned int model_ptr, unsigned int anim_ptr,
                                float x, float y, float z,
                                short rot_x, short rot_y, short rot_z,
                                float scale_x, float scale_y, float scale_z,
                                short seg8_file_id, short seg9_file_id);

void *create_hidden_model(void *task, float x, float y, float z) {
    if (!task) return 0;
    void *object = func_8000DBF0_E7F0(
        task, 0, 0xC01FC680u, x, y, z,
        0, 0, 0, 0.1f, 0.1f, 0.1f, 0, 0);
    if (object) ((unsigned char *)object)[5] = 2;
    return object;
}
```

Complete C syntax example using the documented native declarations. Integrate it only at the described engine lifecycle boundary; the game supplies symbol definitions and resident resources.

## Notes

- Supply a valid task before calling: the native function reaches its allocator before its null-task branch.
- The animation-context constant and object mode in this example are specific to the clothed Goemon character assets.
- This object provides visual rendering only. It does not create player input, collision, AI or character behavior.
- An Impact cursor clone must be created while the file_13 overlay and file 0x4A8 are resident. Do not substitute the damage-flash mesh or force its alpha opaque: it covers the screen.
- Check asset residency before constructing an object. A missing native file resolver can reach a deliberate fault; a nonzero file number alone does not prove the resource is loaded.

## Related symbols

- [`func_80034E08_35A08`](../functions/func_80034E08_35A08.md)
- [`func_80035EEC_36AEC`](../functions/func_80035EEC_36AEC.md)
- [`func_8001B5AC_1C1AC`](../functions/func_8001B5AC_1C1AC.md)
