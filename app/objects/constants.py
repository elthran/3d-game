from panda3d.core import BitMask32


class WorldPhysics:
    FRICTION = 150.0


class Keys:
    W = "w"
    S = "s"
    A = "a"
    D = "d"
    F = "f"
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"
    MOUSE_LEFT = "mouse_left"
    MOUSE_RIGHT = "mouse_right"


class CharacterTypes:
    HERO = "Hero"
    MONSTER = "Monster"
    NPC = "NPC"


class Masks:
    NONE = BitMask32(0x0)
    HERO = BitMask32(0x1)
    MONSTER = BitMask32(0x2)
    NPC = BitMask32(0x4)

    HERO_AND_MONSTER = HERO | MONSTER
    HERO_AND_NPC = HERO | NPC
    MONSTER_AND_NPC = MONSTER | NPC
    HERO_MONSTER_AND_NPC = HERO | MONSTER | NPC


class States:
    MENU = 'menu'
    RUNNING = 'running'
    QUIT = 'quit'
