from enum import Enum


class Color(Enum):
    WHITE: int = 0
    BLACK: int = 1


class PieceType(Enum):
    NULL: int = 0
    PAWN: int = 1
    KNIGHT: int = 2
    BISHOP: int = 3
    ROOK: int = 4
    QUEEN: int = 5
    KING: int = 6
