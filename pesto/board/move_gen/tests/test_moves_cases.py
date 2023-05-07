from typing import Mapping

from pesto.board.board import CastleRights, CastleSide
from pesto.board.move_gen.moves import Move
from pesto.board.square import Square
from pesto.board.piece import Knight, King, Pawn, Piece, Rook
from pesto.core.enums import Color


_TestMakeMoveCase = tuple[
    Mapping[Square, Piece],
    Move,
    Mapping[Square, Piece],
    Move,
    bool,
]


class TestMakeMoveCases:
    def case_exc_no_piece_to_move(self) -> _TestMakeMoveCase:
        in_piece_map: Mapping[Square, Piece] = {}
        in_move = Move(
            start=King(Color.BLACK, Square.D5),
            end=King(Color.BLACK, Square.D6),
        )
        out_piece_map: Mapping[Square, Piece] = {}
        out_move = in_move  # unused
        exception = True
        return in_piece_map, in_move, out_piece_map, out_move, exception

    def case_exc_move_piece_is_different_than_board_piece(self) -> _TestMakeMoveCase:
        in_piece_map = {Square.D5: King(Color.WHITE, Square.D5)}
        in_move = Move(
            start=King(Color.BLACK, Square.D5),
            end=King(Color.BLACK, Square.D6),
        )
        out_piece_map: Mapping[Square, Piece] = {}
        out_move = in_move  # unused
        exception = True
        return in_piece_map, in_move, out_piece_map, out_move, exception

    def case_exc_attempted_to_capture_own_color_piece(self) -> _TestMakeMoveCase:
        in_piece_map = {
            Square.D5: King(Color.WHITE, Square.D5),
            Square.D6: Pawn(Color.WHITE, Square.D6),
        }
        in_move = Move(
            start=King(Color.WHITE, Square.D5),
            end=King(Color.WHITE, Square.D6),
        )
        out_piece_map: Mapping[Square, Piece] = {}
        out_move = in_move  # unused
        exception = True
        return in_piece_map, in_move, out_piece_map, out_move, exception

    def case_move_to_unoccupied_square(self) -> _TestMakeMoveCase:
        in_piece_map = {Square.D5: King(Color.WHITE, Square.D5)}
        in_move = Move(
            start=King(Color.WHITE, Square.D5),
            end=King(Color.WHITE, Square.D6),
        )
        out_piece_map = {Square.D6: King(Color.WHITE, Square.D6)}
        out_move = Move(
            start=King(Color.WHITE, Square.D5),
            end=King(Color.WHITE, Square.D6),
        )
        exception = False
        return in_piece_map, in_move, out_piece_map, out_move, exception

    def case_move_to_occupied_square(self) -> _TestMakeMoveCase:
        in_piece_map = {
            Square.D5: King(Color.WHITE, Square.D5),
            Square.D6: Pawn(Color.BLACK, Square.D6),
        }
        in_move = Move(
            start=King(Color.WHITE, Square.D5),
            end=King(Color.WHITE, Square.D6),
            captures=None,
        )
        out_piece_map = {
            Square.D6: King(Color.WHITE, Square.D6),
        }
        out_move = Move(
            start=King(Color.WHITE, Square.D5),
            end=King(Color.WHITE, Square.D6),
            captures=Pawn(Color.BLACK, Square.D6),
        )
        exception = False
        return in_piece_map, in_move, out_piece_map, out_move, exception


_TestUnmakeMoveCase = tuple[
    Mapping[Square, Piece],
    Move,
    Mapping[Square, Piece],
    bool,
]


class TestUnmakeMoveCases:
    def case_exc_piece_found_on_move_start_square(self) -> _TestUnmakeMoveCase:
        in_piece_map = {
            Square.D5: Pawn(Color.WHITE, Square.D5),
            Square.D6: King(Color.WHITE, Square.D6),
        }
        in_move = Move(
            start=King(Color.WHITE, Square.D5),
            end=King(Color.WHITE, Square.D6),
        )
        out_piece_map: Mapping[Square, Piece] = {}
        exception = True
        return in_piece_map, in_move, out_piece_map, exception

    def case_exc_no_piece_on_square_where_capture_occurred(self) -> _TestUnmakeMoveCase:
        in_piece_map = {Square.D5: King(Color.WHITE, Square.D5)}
        in_move = Move(
            start=King(Color.WHITE, Square.D5),
            end=King(Color.WHITE, Square.D6),
            captures=Pawn(Color.BLACK, Square.D6),
        )
        out_piece_map: Mapping[Square, Piece] = {}
        exception = True
        return in_piece_map, in_move, out_piece_map, exception

    def case_exc_unexpected_piece_found_on_capture_square(self) -> _TestUnmakeMoveCase:
        in_piece_map = {Square.D6: Knight(Color.WHITE, Square.D6)}
        in_move = Move(
            start=King(Color.WHITE, Square.D5),
            end=King(Color.WHITE, Square.D6),
            captures=Pawn(Color.BLACK, Square.D6),
        )
        out_piece_map: Mapping[Square, Piece] = {}
        exception = True
        return in_piece_map, in_move, out_piece_map, exception

    def case_revert_move_without_a_capture(self) -> _TestUnmakeMoveCase:
        in_piece_map = {Square.D6: King(Color.WHITE, Square.D6)}
        in_move = Move(
            start=King(Color.WHITE, Square.D5),
            end=King(Color.WHITE, Square.D6),
        )
        out_piece_map = {Square.D5: King(Color.WHITE, Square.D5)}
        exception = False
        return in_piece_map, in_move, out_piece_map, exception

    def case_revert_move_with_a_capture(self) -> _TestUnmakeMoveCase:
        in_piece_map = {Square.D6: King(Color.WHITE, Square.D6)}
        in_move = Move(
            start=King(Color.WHITE, Square.D5),
            end=King(Color.WHITE, Square.D6),
            captures=Pawn(Color.BLACK, Square.D6),
        )
        out_piece_map = {
            Square.D5: King(Color.WHITE, Square.D5),
            Square.D6: Pawn(Color.BLACK, Square.D6),
        }
        exception = False
        return in_piece_map, in_move, out_piece_map, exception


_TestGenerateCastlingMovesCase = tuple[
    Mapping[Square, Piece],
    CastleRights,
    Color,
    list[Move],
]


class TestGenerateCastlingMovesCases:
    def case_side_to_move_has_no_castle_rights(self) -> _TestGenerateCastlingMovesCase:
        piece_map: Mapping[Square, Piece] = {}
        castle_rights = CastleRights(
            _rights={
                Color.WHITE: {CastleSide.SHORT: False, CastleSide.LONG: False},
                Color.BLACK: {CastleSide.SHORT: True, CastleSide.LONG: True},
            }
        )
        to_move = Color.WHITE
        exp_moves: list[Move] = []

        return piece_map, castle_rights, to_move, exp_moves

    def case_able_to_castle_short(self) -> _TestGenerateCastlingMovesCase:
        piece_map = {
            Square.E8: King(Color.BLACK, Square.E8),
            Square.H8: Rook(Color.BLACK, Square.H8),
        }
        castle_rights = CastleRights(
            _rights={
                Color.WHITE: {CastleSide.SHORT: False, CastleSide.LONG: False},
                Color.BLACK: {CastleSide.SHORT: True, CastleSide.LONG: False},
            }
        )
        to_move = Color.BLACK
        exp_moves = [
            Move(start=King(Color.BLACK, Square.E8), end=King(Color.BLACK, Square.G8)),
            Move(start=Rook(Color.BLACK, Square.H8), end=Rook(Color.BLACK, Square.F8)),
        ]
        return piece_map, castle_rights, to_move, exp_moves

    def case_able_to_castle_long(self) -> _TestGenerateCastlingMovesCase:
        piece_map = {
            Square.E8: King(Color.BLACK, Square.E8),
            Square.A8: Rook(Color.BLACK, Square.A8),
        }
        castle_rights = CastleRights(
            _rights={
                Color.WHITE: {CastleSide.SHORT: False, CastleSide.LONG: False},
                Color.BLACK: {CastleSide.SHORT: False, CastleSide.LONG: True},
            }
        )
        to_move = Color.BLACK
        exp_moves = [
            Move(start=King(Color.BLACK, Square.E8), end=King(Color.BLACK, Square.C8)),
            Move(start=Rook(Color.BLACK, Square.A8), end=Rook(Color.BLACK, Square.D8)),
        ]
        return piece_map, castle_rights, to_move, exp_moves

    def case_cant_castle_through_check(self) -> _TestGenerateCastlingMovesCase:
        piece_map = {
            Square.E1: King(Color.WHITE, Square.E1),
            Square.A1: Rook(Color.WHITE, Square.A1),
            Square.B8: Rook(Color.BLACK, Square.B8),
        }
        castle_rights = CastleRights(
            _rights={
                Color.WHITE: {CastleSide.SHORT: False, CastleSide.LONG: True},
                Color.BLACK: {CastleSide.SHORT: False, CastleSide.LONG: False},
            }
        )
        to_move = Color.WHITE
        exp_moves: list[Move] = []
        return piece_map, castle_rights, to_move, exp_moves

    def case_cant_castle_ending_in_check(self) -> _TestGenerateCastlingMovesCase:
        piece_map = {
            Square.E1: King(Color.WHITE, Square.E1),
            Square.A1: Rook(Color.WHITE, Square.A1),
            Square.H1: Rook(Color.WHITE, Square.H1),
            Square.C8: Rook(Color.BLACK, Square.C8),  # prevents long castling
        }
        castle_rights = CastleRights(
            _rights={
                Color.WHITE: {CastleSide.SHORT: True, CastleSide.LONG: True},
                Color.BLACK: {CastleSide.SHORT: False, CastleSide.LONG: False},
            }
        )
        to_move = Color.WHITE
        exp_moves = [
            Move(start=King(Color.WHITE, Square.E1), end=King(Color.WHITE, Square.G1)),
            Move(start=Rook(Color.WHITE, Square.H1), end=Rook(Color.WHITE, Square.F1)),
        ]
        return piece_map, castle_rights, to_move, exp_moves

    def case_cant_castle_through_another_piece(self) -> _TestGenerateCastlingMovesCase:
        piece_map = {
            Square.E1: King(Color.WHITE, Square.E1),
            Square.A1: Rook(Color.WHITE, Square.A1),
            Square.B1: Knight(Color.WHITE, Square.B1),
        }
        castle_rights = CastleRights(
            _rights={
                Color.WHITE: {CastleSide.SHORT: False, CastleSide.LONG: True},
                Color.BLACK: {CastleSide.SHORT: False, CastleSide.LONG: True},
            }
        )
        to_move = Color.WHITE
        exp_moves: list[Move] = []
        return piece_map, castle_rights, to_move, exp_moves
