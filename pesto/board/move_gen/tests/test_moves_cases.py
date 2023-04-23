from typing import Mapping

from pesto.board.move_gen.moves import Move
from pesto.board.square import Square
from pesto.board.piece import Knight, King, Pawn, Piece
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
            piece=King(Color.BLACK, Square.D5),
            start=Square.D5,
            end=Square.D6,
        )
        out_piece_map: Mapping[Square, Piece] = {}
        out_move = in_move  # unused
        exception = True
        return in_piece_map, in_move, out_piece_map, out_move, exception

    def case_exc_move_piece_is_different_than_board_piece(self) -> _TestMakeMoveCase:
        in_piece_map = {Square.D5: King(Color.WHITE, Square.D5)}
        in_move = Move(
            piece=King(Color.BLACK, Square.D5),
            start=Square.D5,
            end=Square.D6,
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
            piece=King(Color.WHITE, Square.D5),
            start=Square.D5,
            end=Square.D6,
        )
        out_piece_map: Mapping[Square, Piece] = {}
        out_move = in_move  # unused
        exception = True
        return in_piece_map, in_move, out_piece_map, out_move, exception

    def case_move_to_unoccupied_square(self) -> _TestMakeMoveCase:
        in_piece_map = {Square.D5: King(Color.WHITE, Square.D5)}
        in_move = Move(
            piece=King(Color.WHITE, Square.D5),
            start=Square.D5,
            end=Square.D6,
        )
        out_piece_map = {Square.D6: King(Color.WHITE, Square.D6)}
        out_move = Move(
            piece=King(Color.WHITE, Square.D6),
            start=Square.D5,
            end=Square.D6,
        )
        exception = False
        return in_piece_map, in_move, out_piece_map, out_move, exception

    def case_move_to_occupied_square(self) -> _TestMakeMoveCase:
        in_piece_map = {
            Square.D5: King(Color.WHITE, Square.D5),
            Square.D6: Pawn(Color.BLACK, Square.D6),
        }
        in_move = Move(
            piece=King(Color.WHITE, Square.D5),
            start=Square.D5,
            end=Square.D6,
            captures=None,
        )
        out_piece_map = {
            Square.D6: King(Color.WHITE, Square.D6),
        }
        out_move = Move(
            piece=King(Color.WHITE, Square.D6),
            start=Square.D5,
            end=Square.D6,
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
            piece=King(Color.WHITE, Square.D6),
            start=Square.D5,
            end=Square.D6,
        )
        out_piece_map: Mapping[Square, Piece] = {}
        exception = True
        return in_piece_map, in_move, out_piece_map, exception

    def case_exc_no_piece_on_square_where_capture_occurred(self) -> _TestUnmakeMoveCase:
        in_piece_map = {Square.D5: King(Color.WHITE, Square.D5)}
        in_move = Move(
            piece=King(Color.WHITE, Square.D6),
            start=Square.D5,
            end=Square.D6,
            captures=Pawn(Color.BLACK, Square.D6),
        )
        out_piece_map: Mapping[Square, Piece] = {}
        exception = True
        return in_piece_map, in_move, out_piece_map, exception

    def case_exc_unexpected_piece_found_on_capture_square(self) -> _TestUnmakeMoveCase:
        in_piece_map = {Square.D6: Knight(Color.WHITE, Square.D6)}
        in_move = Move(
            piece=King(Color.WHITE, Square.D6),
            start=Square.D5,
            end=Square.D6,
            captures=Pawn(Color.BLACK, Square.D6),
        )
        out_piece_map: Mapping[Square, Piece] = {}
        exception = True
        return in_piece_map, in_move, out_piece_map, exception

    def case_revert_move_without_a_capture(self) -> _TestUnmakeMoveCase:
        in_piece_map = {Square.D6: King(Color.WHITE, Square.D6)}
        in_move = Move(
            piece=King(Color.WHITE, Square.D6),
            start=Square.D5,
            end=Square.D6,
        )
        out_piece_map = {Square.D5: King(Color.WHITE, Square.D5)}
        exception = False
        return in_piece_map, in_move, out_piece_map, exception

    def case_revert_move_with_a_capture(self) -> _TestUnmakeMoveCase:
        in_piece_map = {Square.D6: King(Color.WHITE, Square.D6)}
        in_move = Move(
            piece=King(Color.WHITE, Square.D6),
            start=Square.D5,
            end=Square.D6,
            captures=Pawn(Color.BLACK, Square.D6),
        )
        out_piece_map = {
            Square.D5: King(Color.WHITE, Square.D5),
            Square.D6: Pawn(Color.BLACK, Square.D6),
        }
        exception = False
        return in_piece_map, in_move, out_piece_map, exception
