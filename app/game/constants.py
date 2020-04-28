from panda3d.core import BitMask32


class WorldPhysics:
    FRICTION = 150.0


class Keys:
    A = "a"
    B = "b"
    C = "c"
    D = "d"
    E = "e"
    F = "f"
    G = "g"
    H = "h"
    I = "i"
    J = "j"
    K = "k"
    L = "l"
    M = "m"
    N = "n"
    O = "o"
    P = "p"
    Q = "q"
    R = "r"
    S = "s"
    T = "t"
    U = "u"
    V = "v"
    W = "w"
    X = "x"
    Y = "y"
    Z = "z"
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
