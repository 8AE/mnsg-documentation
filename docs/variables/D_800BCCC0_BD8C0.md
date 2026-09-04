---
title: "System-state interior alias"
sidebar_label: "D_800BCCC0_BD8C0"
slug: "/variables/D_800BCCC0_BD8C0"
description: "Interior address in native system-state storage, used as a base for prepared scene-destination fields."
---

`D_800BCCC0_BD8C0` · **Variable**

Interior address in native system-state storage, used as a base for prepared scene-destination fields.

| Runtime address | ROM address | Section |
| --- | --- | --- |
| `0x800BCCC0` | — | `ABSOLUTE_SYMS` |

## Signature

```c
extern unsigned char D_800BCCC0_BD8C0[];
```

## How it works

The system structure starts at 0x8008CCC0. D_800BCCC0_BD8C0 names the interior address at system base +0x30000; it is not the complete structure base stored in D_8015C5C8_15D1C8.

The prepared destination room is a 16-bit field at this symbol +0xAFE0. The same field is at +0x3AFE0 relative to the full system pointer. Native destination writing uses this interior address to reach the room, position and rotation fields.

Offsets must match the chosen base. Treat the remaining layout as partial; the unsized byte-array declaration does not establish the size of the surrounding structure.

## Known values

### Interior-alias field offsets {#alias-fields}

This exported byte array begins at full-system offset +0x30000. Use the alias-relative offset in this table when indexing D_800BCCC0_BD8C0 directly; adding a full-pointer offset to this alias addresses the wrong memory.

| Alias-relative offset | Full-system offset | Storage type | Meaning |
| --- | --- | --- | --- |
| `0xADCA` | `0x3ADCA` | `uint8_t` | Game-loop timing/control byte; the system-step setter writes 2. |
| `0xADCE` | `0x3ADCE` | `int16_t` | Game-loop/frame counter; a running numeric counter, not a state ID. |
| `0xADD4` | `0x3ADD4` | `uint8_t` | Main system step. See [known main-system steps](./D_8015C5C8_15D1C8.md#known-system-steps). |
| `0xADD5` | `0x3ADD5` | `uint8_t` | Main-step completion/substate byte; the step setter clears it to 0. |
| `0xAE16` | `0x3AE16` | `int16_t` | Native start-sequence gate. Zero is the cleared value used for normal gameplay; nonzero values must retain their native sequence meaning. |
| `0xAE29` | `0x3AE29` | `uint8_t` | Destination-transition marker; the warp destination helper writes 1. |
| `0xAE3A` | `0x3AE3A` | `uint16_t` | Seventh argument of the warp destination helper; individual values are not yet interpreted. |
| `0xAE3C` | `0x3AE3C` | `uint32_t` | Eighth argument of the warp destination helper; individual values are not yet interpreted. |
| `0xAFE0` | `0x3AFE0` | `uint16_t` | Destination room/stage ID. Use the room table on D_800C7AB2. |
| `0xAFE2` | `0x3AFE2` | `int16_t` | Destination player rotation. |
| `0xAFE4` | `0x3AFE4` | `int16_t` | Destination player X position. |
| `0xAFE6` | `0x3AFE6` | `int16_t` | Destination player Y position. |
| `0xAFE8` | `0x3AFE8` | `int16_t` | Destination player Z position. |
| `0xAFEA` | `0x3AFEA` | `int16_t` | Destination camera rotation. |

## Usage example

```c
extern unsigned char D_800BCCC0_BD8C0[];

/* Read only after the native system state has been initialized. */
unsigned short read_static_destination(void)
{
    return *(volatile unsigned short *)(D_800BCCC0_BD8C0 + 0xAFE0);
}
```

Read the prepared destination room with an offset relative to this interior alias. The current room is a separate field exposed by D_800C7AB2.

## Notes

- Do not apply full system-pointer offsets to this interior alias. Adding 0x3AFE0 here reads a different address; use 0xAFE0 for the prepared destination.
- Do not copy or clear this entire opaque block based on the unsized extern declaration.

## Related symbols

- [`D_8015C5C8_15D1C8`](../variables/D_8015C5C8_15D1C8.md)
- [`func_8000607C_6C7C`](../functions/func_8000607C_6C7C.md)
- [`D_800C7AB2`](../variables/D_800C7AB2.md)
