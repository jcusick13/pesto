from enum import Enum


class Square(Enum):
    """Represents square indices on a 0x88 (16x8) board"""

    A1: int = 0
    B1: int = 1
    C1: int = 2
    D1: int = 3
    E1: int = 4
    F1: int = 5
    G1: int = 6
    H1: int = 7
    A2: int = 16
    B2: int = 17
    C2: int = 18
    D2: int = 19
    E2: int = 20
    F2: int = 21
    G2: int = 22
    H2: int = 23
    A3: int = 32
    B3: int = 33
    C3: int = 34
    D3: int = 35
    E3: int = 36
    F3: int = 37
    G3: int = 38
    H3: int = 39
    A4: int = 48
    B4: int = 49
    C4: int = 50
    D4: int = 51
    E4: int = 52
    F4: int = 53
    G4: int = 54
    H4: int = 55
    A5: int = 64
    B5: int = 65
    C5: int = 66
    D5: int = 67
    E5: int = 68
    F5: int = 69
    G5: int = 70
    H5: int = 71
    A6: int = 80
    B6: int = 81
    C6: int = 82
    D6: int = 83
    E6: int = 84
    F6: int = 85
    G6: int = 86
    H6: int = 87
    A7: int = 96
    B7: int = 97
    C7: int = 98
    D7: int = 99
    E7: int = 100
    F7: int = 101
    G7: int = 102
    H7: int = 103
    A8: int = 112
    B8: int = 113
    C8: int = 114
    D8: int = 115
    E8: int = 116
    F8: int = 117
    G8: int = 118
    H8: int = 119


def str_to_square(string: str) -> Square:
    """Maps a string in algebraic notation to a `Square`"""
    if len(string) != 2:
        raise ValueError(f"Expected a single square, received {string}")
    return Square[string.upper()]
