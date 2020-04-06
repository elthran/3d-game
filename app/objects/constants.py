from panda3d.core import BitMask32


class WorldPhysics:
    FRICTION = 150.0


class CharacterTypes:
    HERO = "Hero"
    MONSTER = "Monster"
    NPC = "NPC"


class Masks:
    NONE = BitMask32(0x0)
    HERO = BitMask32(0x1)
    MONSTER = BitMask32(0x2)
    NPC = BitMask32(0x4)

    MASK_HERO_AND_MONSTER = HERO | MONSTER
    MASK_HERO_AND_NPC = HERO | NPC
    MASK_MONSTER_AND_NPC = MONSTER | NPC
    MASK_HERO_MONSTER_AND_NPC = HERO | MONSTER | NPC
