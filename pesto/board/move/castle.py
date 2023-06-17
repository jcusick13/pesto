from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from pesto.board.move.attack import square_is_attacked
from pesto.board.piece import BaseMove, CastlingMove, King, Piece, Rook
from pesto.board.square import Square
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

    def set_false(self, color: Color, castle_side: CastleSide) -> None:
        self._rights[color][castle_side] = False

    def set_true(self, color: Color, castle_side: CastleSide) -> None:
        self._rights[color][castle_side] = True


@dataclass
class CastleSquare:
    """Container for identifying king and rook square
    locations before and after castling
    """

    color: Color
    castle_side: CastleSide

    def __post_init__(self) -> None:
        self._color_adjust: int = 0 if self.color == Color.WHITE else 112

    @property
    def king_passthrough_squares(self) -> set[Square]:
        passthrough_idx_map = {CastleSide.SHORT: [5, 6], CastleSide.LONG: [2, 3]}
        squares: set[Square] = set()
        for square_idx in passthrough_idx_map[self.castle_side]:
            squares.add(Square(square_idx + self._color_adjust))
        return squares

    @property
    def rook_passthrough_squares(self) -> set[Square]:
        passthrough_idx_map = {CastleSide.SHORT: [5, 6], CastleSide.LONG: [1, 2, 3]}
        squares: set[Square] = set()
        for square_idx in passthrough_idx_map[self.castle_side]:
            squares.add(Square(square_idx + self._color_adjust))
        return squares

    @property
    def passthrough_squares(self) -> set[Square]:
        """Squares the king and rook pass through"""
        return self.king_passthrough_squares | self.rook_passthrough_squares

    @property
    def rook_start(self) -> Square:
        """Rook location before castling"""
        rook_start_idx_map = {CastleSide.SHORT: 7, CastleSide.LONG: 0}
        return Square(rook_start_idx_map[self.castle_side] + self._color_adjust)

    @property
    def rook_end(self) -> Square:
        """Rook location after castling"""
        rook_end_idx_map = {CastleSide.SHORT: 5, CastleSide.LONG: 3}
        return Square(rook_end_idx_map[self.castle_side] + self._color_adjust)

    @property
    def king_start(self) -> Square:
        """King locaton before castling"""
        return Square(4 + self._color_adjust)

    @property
    def king_end(self) -> Square:
        """King location after castling"""
        king_end_idx_map = {CastleSide.SHORT: 6, CastleSide.LONG: 2}
        return Square(king_end_idx_map[self.castle_side] + self._color_adjust)


def generate_castling_moves(
    piece_map: dict[Square, Piece],
    castle_rights: CastleRights,
    to_move: Color,
) -> set[CastlingMove]:
    """Return a collection of castling move objects if the side `to_move`
    is legally allowed to castle in either direction
    """
    moves: set[CastlingMove] = set()
    opposite_color: Color = Color.WHITE if to_move == Color.BLACK else Color.BLACK
    rights: dict[CastleSide, bool] = castle_rights(color=to_move)

    for castling_side in CastleSide:
        able_to_castle: bool = True

        if rights[castling_side] is True:
            squares = CastleSquare(color=to_move, castle_side=castling_side)

            # Check if the king starts in check
            if square_is_attacked(
                piece_map=piece_map, square=squares.king_start, by=opposite_color
            ):
                able_to_castle = False
                break

            # Check that no pieces are between king and rook
            for square in squares.passthrough_squares:
                if piece_map.get(square) is not None:
                    able_to_castle = False
                    break

            if not able_to_castle:
                continue

            # Check if the king passes through check
            for square in squares.king_passthrough_squares:
                if square_is_attacked(
                    piece_map=piece_map, square=square, by=opposite_color
                ):
                    able_to_castle = False
                    break

            if not able_to_castle:
                continue

            # Able to castle!
            moves.add(
                CastlingMove(
                    start=King(color=to_move, curr=squares.king_start),
                    end=King(color=to_move, curr=squares.king_end),
                    castled_rook=BaseMove(
                        start=Rook(color=to_move, curr=squares.rook_start),
                        end=Rook(color=to_move, curr=squares.rook_end),
                    ),
                )
            )

    return moves
