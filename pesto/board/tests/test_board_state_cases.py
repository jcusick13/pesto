from typing import Optional

from pesto.board.move.castle import CastleRights, CastleSide
from pesto.board.piece import (
    BaseMove,
    CastlingMove,
    King,
    Move,
    Pawn,
    Rook,
    SinglePieceMove,
)
from pesto.board.square import Square
from pesto.core.enums import Color

_FindEnPassantTargetCase = tuple[Move, Optional[Square]]


class FindEnPassantTargetCases:
    def case_non_pawn_move(self) -> _FindEnPassantTargetCase:
        move = SinglePieceMove(
            start=Rook(Color.BLACK, Square.A1),
            end=Rook(Color.BLACK, Square.A2),
        )
        exp: Optional[Square] = None
        return move, exp

    def case_pawn_moves_one_square(self) -> _FindEnPassantTargetCase:
        move = SinglePieceMove(
            start=Pawn(Color.WHITE, Square.D6),
            end=Pawn(Color.WHITE, Square.D7),
        )
        exp: Optional[Square] = None
        return move, exp

    def case_pawn_moves_two_squares(self) -> _FindEnPassantTargetCase:
        move = SinglePieceMove(
            start=Pawn(Color.WHITE, Square.C2),
            end=Pawn(Color.WHITE, Square.C4),
        )
        exp = Square.C3
        return move, exp


_UpdateCastleRightsCase = tuple[CastleRights, Move, CastleRights]


class UpdateCastleRightsCases:
    def case_no_castling_occurred(self) -> _UpdateCastleRightsCase:
        castle_rights = exp = CastleRights.new()
        move = SinglePieceMove(
            start=Pawn(Color.WHITE, Square.C2),
            end=Pawn(Color.WHITE, Square.C4),
        )
        return castle_rights, move, exp

    def case_castled_short(self) -> _UpdateCastleRightsCase:
        castle_rights = CastleRights.new()
        move = CastlingMove(
            start=King(Color.WHITE, Square.E1),
            end=King(Color.WHITE, Square.G1),
            castled_rook=BaseMove(
                start=Rook(Color.WHITE, Square.H1), end=Rook(Color.WHITE, Square.F1)
            ),
        )
        exp = CastleRights.new()
        exp.flip(Color.WHITE, CastleSide.SHORT)
        return castle_rights, move, exp

    def case_castled_long(self) -> _UpdateCastleRightsCase:
        castle_rights = CastleRights.new()
        move = CastlingMove(
            start=King(Color.WHITE, Square.E1),
            end=King(Color.WHITE, Square.C1),
            castled_rook=BaseMove(
                start=Rook(Color.WHITE, Square.A1), end=Rook(Color.WHITE, Square.D1)
            ),
        )
        exp = CastleRights.new()
        exp.flip(Color.WHITE, CastleSide.LONG)
        return castle_rights, move, exp


_UpdateHalfmoveClockCase = tuple[int, Move, int]


class UpdateHalfmoveClockCases:
    def case_non_pawn_non_capture_move(self) -> _UpdateHalfmoveClockCase:
        clock = 35
        move = SinglePieceMove(
            start=Rook(Color.BLACK, Square.C4),
            end=Rook(Color.BLACK, Square.F4),
            captures=None,
        )
        exp = 36
        return clock, move, exp

    def case_pawn_non_capture_move(self) -> _UpdateHalfmoveClockCase:
        clock = 2
        move = SinglePieceMove(
            start=Pawn(Color.WHITE, Square.C2),
            end=Pawn(Color.WHITE, Square.C4),
            captures=None,
        )
        exp = 0
        return clock, move, exp

    def case_capture_move(self) -> _UpdateHalfmoveClockCase:
        clock = 22
        move = SinglePieceMove(
            start=Rook(Color.BLACK, Square.C4),
            end=Rook(Color.BLACK, Square.F4),
            captures=Pawn(Color.WHITE, Square.F4),
        )
        exp = 0
        return clock, move, exp
