from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Optional

from pesto.board.square import Square, str_to_square
from pesto.board.piece import Bishop, King, Knight, Rook, Pawn, Piece, Queen
from pesto.core.enums import Color


class CastleSide(Enum):
    SHORT: str = "short"
    LONG: str = "long"


@dataclass
class CastleRights:
    _rights: dict[Color, dict[CastleSide, bool]]

    @classmethod
    def new(cls) -> CastleRights:
        """Initialize a `CastleRights` object representing game start"""
        return CastleRights(
            _rights={
                Color.WHITE: {CastleSide.SHORT: True, CastleSide.LONG: True},
                Color.BLACK: {CastleSide.SHORT: True, CastleSide.LONG: True},
            }
        )

    @classmethod
    def none(cls) -> CastleRights:
        """Initialize a `CastleRights` object where no one has rights"""
        return CastleRights(
            _rights={
                Color.WHITE: {CastleSide.SHORT: False, CastleSide.LONG: False},
                Color.BLACK: {CastleSide.SHORT: False, CastleSide.LONG: False},
            }
        )

    def __call__(self, color: Color) -> dict[CastleSide, bool]:
        return self._rights[color]

    def flip(self, color: Color, castle_side: CastleSide) -> None:
        """Flips the boolean flag for the given `color` and `castle`"""
        self._rights[color][castle_side] = not self._rights[color][castle_side]


@dataclass
class Board:
    ply: int
    halfmove_clock: int
    to_move: Color
    piece_map: dict[Square, Piece]
    castle_rights: CastleRights
    en_passant_target: Optional[Square]

    @classmethod
    def new(cls) -> Board:
        """Create a new board at the starting game position"""
        return Board(
            ply=1,
            halfmove_clock=0,
            to_move=Color.WHITE,
            piece_map=starting_piece_map(),
            castle_rights=CastleRights.new(),
            en_passant_target=None,
        )

    @classmethod
    def from_fen(cls, fen: str) -> Board:
        """Construct a new `Board` from a FEN string"""
        (
            pieces,
            color,
            castling,
            en_passant,
            halfmove_clock,
            fullmove_count,
        ) = fen.split()

        to_move = Color.WHITE if color == "w" else Color.BLACK
        ply = (int(fullmove_count) * 2) - 1
        if to_move == Color.BLACK:
            ply += 1

        return Board(
            ply=ply,
            halfmove_clock=int(halfmove_clock),
            to_move=to_move,
            piece_map=_parse_fen_piece_map(pieces),
            castle_rights=_parse_fen_castling_rights(castling),
            en_passant_target=_parse_fen_en_passant_target(en_passant),
        )


def _parse_fen_piece_map(string: str) -> dict[Square, Piece]:
    """Maps the piece location string segment of a FEN string
    into a piece map
    """
    piece_map: dict[Square, Piece] = {}
    letter_map = {
        "B": Bishop,
        "K": King,
        "N": Knight,
        "P": Pawn,
        "Q": Queen,
        "R": Rook,
    }

    ranks = string.split("/")
    rank_idx: int
    pieces: str
    for rank_idx, pieces in enumerate(reversed(ranks)):
        file_idx = 0
        piece: str
        for piece in pieces:
            if piece.isdigit():
                file_idx += int(piece)
                continue

            color = Color.WHITE if piece.isupper() else Color.BLACK
            square = Square((rank_idx * 16) + file_idx)
            piece_map[square] = letter_map[piece.upper()].new(
                color=color,
                curr=square,
            )
            file_idx += 1

    return piece_map


def _parse_fen_en_passant_target(string: str) -> Optional[Square]:
    """Maps the en passant string segment of a FEN string into
    a `Square`, if one is present
    """
    if string == "-":
        return None

    return str_to_square(string)


def _parse_fen_castling_rights(string: str) -> CastleRights:
    """Maps the castling string segment of a FEN string into
    a `CastleRights` object
    """
    castle_rights = CastleRights(
        _rights={
            Color.WHITE: {CastleSide.SHORT: False, CastleSide.LONG: False},
            Color.BLACK: {CastleSide.SHORT: False, CastleSide.LONG: False},
        }
    )
    if string == "-":
        return castle_rights

    char_map: dict[str, tuple[Color, CastleSide]] = {
        "K": (Color.WHITE, CastleSide.SHORT),
        "Q": (Color.WHITE, CastleSide.LONG),
        "k": (Color.BLACK, CastleSide.SHORT),
        "q": (Color.BLACK, CastleSide.LONG),
    }
    for char in string:
        color, castle_side = char_map[char]
        castle_rights.flip(color, castle_side)

    return castle_rights


def starting_piece_map() -> dict[Square, Piece]:
    return {
        Square.A1: Rook(Color.WHITE, Square.A1),
        Square.B1: Knight(Color.WHITE, Square.B1),
        Square.C1: Bishop(Color.WHITE, Square.C1),
        Square.D1: Queen(Color.WHITE, Square.D1),
        Square.E1: King(Color.WHITE, Square.E1),
        Square.F1: Bishop(Color.WHITE, Square.F1),
        Square.G1: Knight(Color.WHITE, Square.G1),
        Square.H1: Rook(Color.WHITE, Square.H1),
        Square.A2: Pawn(Color.WHITE, Square.A2),
        Square.B2: Pawn(Color.WHITE, Square.B2),
        Square.C2: Pawn(Color.WHITE, Square.C2),
        Square.D2: Pawn(Color.WHITE, Square.D2),
        Square.E2: Pawn(Color.WHITE, Square.E2),
        Square.F2: Pawn(Color.WHITE, Square.F2),
        Square.G2: Pawn(Color.WHITE, Square.G2),
        Square.H2: Pawn(Color.WHITE, Square.H2),
        Square.A8: Rook(Color.BLACK, Square.A8),
        Square.B8: Knight(Color.BLACK, Square.B8),
        Square.C8: Bishop(Color.BLACK, Square.C8),
        Square.D8: Queen(Color.BLACK, Square.D8),
        Square.E8: King(Color.BLACK, Square.E8),
        Square.F8: Bishop(Color.BLACK, Square.F8),
        Square.G8: Knight(Color.BLACK, Square.G8),
        Square.H8: Rook(Color.BLACK, Square.H8),
        Square.A7: Pawn(Color.BLACK, Square.A7),
        Square.B7: Pawn(Color.BLACK, Square.B7),
        Square.C7: Pawn(Color.BLACK, Square.C7),
        Square.D7: Pawn(Color.BLACK, Square.D7),
        Square.E7: Pawn(Color.BLACK, Square.E7),
        Square.F7: Pawn(Color.BLACK, Square.F7),
        Square.G7: Pawn(Color.BLACK, Square.G7),
        Square.H7: Pawn(Color.BLACK, Square.H7),
    }
