---
title: "Process native player damage and contact reactions"
sidebar_label: "func_801D9E9C_595DAC"
slug: "/functions/func_801D9E9C_595DAC"
description: "Handles death state, environmental hazards and the incoming native contact for a fully initialized playable player."
---

`func_801D9E9C_595DAC` · **Function**

Handles death state, environmental hazards and the incoming native contact for a fully initialized playable player.

| Runtime address | ROM address | Section |
| --- | --- | --- |
| `0x801D9E9C` | `0x00595DAC` | `.file_11` |

Native code size: **2016 bytes**.

## Signature

```c
extern int func_801D9E9C_595DAC(void *player);
```

## How it works

Checks zero health, floor hazards and crushing before consulting the attacker pointer at player task +0x38. A nonzero result therefore does not identify a particular contact or prove health was lost.

For an ordinary type-1 attacker, reads attacker +0x18 as an object pointer, byte +0x4C as hit kind and byte +0x6D as damage. The object world X/Y/Z at +0x08/+0x0C/+0x10 establish hurt direction. One damage unit is the ordinary half-heart baseline.

Routes ordinary hits through native armour, player action/context, health loss, hurt animation and direction handling. Sudden Impact vulnerability can double the health loss. An armour-blocked hit can start invulnerability even while the function returns zero.

The inspected type-1 paths do not retain their attacker descriptor. Type 2 is different: interaction paths can retain the attacker in player +0xE0. Do not generalize type-1 lifetime behavior to every hit kind.

The normal player pre-update calls func_801E8E24_5A4D34(player, 1) after a nonzero result to cancel eligible owned projectile tasks.

## Return value

Integer native reaction indicator. Nonzero triggers the normal caller's projectile cleanup; zero can still accompany armour absorption and newly started recovery.

## Usage example

```c
#include "modding.h"

static const void *observed_incoming_attacker;

RECOMP_HOOK("func_801D9E9C_595DAC")
void observe_player_damage_intake(void *player)
{
    const unsigned char *task = player;
    if (!task) return;
    observed_incoming_attacker = *(void *const *)(task + 0x38);
}
```

The example illustrates the native interface and its required state.

## Notes

- Requires the real playable task, live work/object/projectile-list fields and initialized gameplay/save state. A standalone visual actor is not a valid receiver.
- The routine does not reproduce all of its caller availability checks. Normal intake is gated by work +0x69, the control-state bytes and native contact/invulnerability state.
- An observer must preserve existing native attacker records and environmental-hit priority. A second call can process state changes beyond the intended contact.
- Return value is a native reaction/cleanup indicator, not a damage amount or a complete accepted-hit boolean. Compare health and recovery state when those distinctions matter.

## Related symbols

- [`func_801CB824_587734`](../functions/func_801CB824_587734.md)
- [`func_801E8E24_5A4D34`](../functions/func_801E8E24_5A4D34.md)
- [`func_801DCD48_598C58`](../functions/func_801DCD48_598C58.md)
- [`D_801FC604_5B8514`](../variables/D_801FC604_5B8514.md)
