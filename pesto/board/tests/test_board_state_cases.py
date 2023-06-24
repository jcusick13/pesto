from typing import Optional

from pesto.board.move.castle import CastleRights, CastleSide
from pesto.board.piece import (
    BaseMove,
    CastlingMove,
    King,
    Knight,
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
        castle_rights.set_false(Color.WHITE, CastleSide.LONG)
        move = CastlingMove(
            start=King(Color.WHITE, Square.E1),
            end=King(Color.WHITE, Square.G1),
            castled_rook=BaseMove(
                start=Rook(Color.WHITE, Square.H1), end=Rook(Color.WHITE, Square.F1)
            ),
        )
        exp = CastleRights.new()
        exp.set_false(Color.WHITE, CastleSide.SHORT)
        exp.set_false(Color.WHITE, CastleSide.LONG)
        return castle_rights, move, exp

    def case_castled_long(self) -> _UpdateCastleRightsCase:
        castle_rights = CastleRights.new()
        castle_rights.set_false(Color.WHITE, CastleSide.SHORT)
        move = CastlingMove(
            start=King(Color.WHITE, Square.E1),
            end=King(Color.WHITE, Square.C1),
            castled_rook=BaseMove(
                start=Rook(Color.WHITE, Square.A1), end=Rook(Color.WHITE, Square.D1)
            ),
        )
        exp = CastleRights.new()
        exp.set_false(Color.WHITE, CastleSide.SHORT)
        exp.set_false(Color.WHITE, CastleSide.LONG)
        return castle_rights, move, exp

    def case_moved_queen_rook(self) -> _UpdateCastleRightsCase:
        castle_rights = CastleRights.new()
        move = SinglePieceMove(
            start=Rook(Color.WHITE, Square.A1),
            end=Rook(Color.WHITE, Square.C1),
        )
        exp = CastleRights.new()
        exp.set_false(Color.WHITE, CastleSide.LONG)
        return castle_rights, move, exp

    def case_moved_king_rook(self) -> _UpdateCastleRightsCase:
        castle_rights = CastleRights.new()
        move = SinglePieceMove(
            start=Rook(Color.BLACK, Square.H8),
            end=Rook(Color.BLACK, Square.G8),
        )
        exp = CastleRights.new()
        exp.set_false(Color.BLACK, CastleSide.SHORT)
        return castle_rights, move, exp

    def case_moved_king(self) -> _UpdateCastleRightsCase:
        castle_rights = CastleRights.new()
        move = SinglePieceMove(
            start=King(Color.WHITE, Square.E1),
            end=King(Color.WHITE, Square.F1),
        )
        exp = CastleRights.new()
        exp.set_false(Color.WHITE, CastleSide.SHORT)
        exp.set_false(Color.WHITE, CastleSide.LONG)
        return castle_rights, move, exp

    def case_king_rook_moved_a_second_time(self) -> _UpdateCastleRightsCase:
        castle_rights = CastleRights(
            _rights={
                Color.WHITE: {CastleSide.SHORT: False, CastleSide.LONG: True},
                Color.BLACK: {CastleSide.SHORT: True, CastleSide.LONG: True},
            }
        )
        move = SinglePieceMove(
            start=Rook(Color.WHITE, Square.G1), end=Rook(Color.WHITE, Square.F1)
        )
        exp = castle_rights
        return castle_rights, move, exp

    def case_lose_castle_right_when_rook_captured(self) -> _UpdateCastleRightsCase:
        castle_rights = CastleRights.new()
        move = SinglePieceMove(
            start=Knight(Color.BLACK, Square.F2),
            end=Knight(Color.BLACK, Square.H1),
            captures=Rook(Color.WHITE, Square.H1),
        )
        exp = CastleRights.new()
        exp.set_false(Color.WHITE, CastleSide.SHORT)
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
