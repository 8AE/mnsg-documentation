---
title: "Active kind-2 pool count"
sidebar_label: "D_8016DADC_16E6DC"
slug: "/variables/D_8016DADC_16E6DC"
description: "Active kind-2 display/model allocation count."
---

`D_8016DADC_16E6DC` · **Variable**

Active kind-2 display/model allocation count.

| Runtime address | ROM address | Section |
| --- | --- | --- |
| `0x8016DADC` | — | `ABSOLUTE_SYMS` |

## Signature

```c
extern short D_8016DADC_16E6DC;
```

## How it works

This address aliases element 2 of D_8016DAD8_16E6D8. The single-record allocator compares it with the kind-2 capacity before taking another free record.

## Known values

### Active model/display count {#count-values}

This signed 16-bit value aliases D_8016DAD8_16E6D8[2]. Compare it to the kind-2 capacity; it is not a flag or a telemetry request count.

| Stored value | Meaning |
| --- | --- |
| `0` | No active kind-2 records according to the native active-allocation counter. |
| Positive signed count | That many kind-2 records are active. |
| Negative signed value | Not a valid ordinary active count; no special negative state is established. |

## Usage example

```c
extern unsigned short D_8006D350_6DF50[];

extern short D_8016DADC_16E6DC;

int remaining_display_allowance(void) {
    return (int)D_8006D350_6DF50[2] - D_8016DADC_16E6DC;
}
```

Complete C syntax example using the documented native declarations. Integrate it only at the described engine lifecycle boundary; the game supplies symbol definitions and resident resources.

## Notes

- Treat engine counters as read-only outside a verified allocator patch; release paths depend on consistency.

## Related symbols

- [`D_8016DAD8_16E6D8`](../variables/D_8016DAD8_16E6D8.md)
- [`func_80036448_37048`](../functions/func_80036448_37048.md)
