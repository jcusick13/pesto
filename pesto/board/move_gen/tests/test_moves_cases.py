from pesto.board.board import CastleRights, CastleSide
from pesto.board.square import Square
from pesto.board.piece import (
    BaseMove,
    CastlingMove,
    Knight,
    King,
    Move,
    Pawn,
    Piece,
    Rook,
    SinglePieceMove,
)
from pesto.core.enums import Color


_TestMakeMoveCase = tuple[
    dict[Square, Piece],
    Move,
    dict[Square, Piece],
    Move,
    bool,
]


class TestMakeMoveCases:
    def case_exc_no_piece_to_move(self) -> _TestMakeMoveCase:
        in_piece_map: dict[Square, Piece] = {}
        in_move = SinglePieceMove(
            start=King(Color.BLACK, Square.D5),
            end=King(Color.BLACK, Square.D6),
        )
        out_piece_map: dict[Square, Piece] = {}
        out_move = in_move  # unused
        exception = True
        return in_piece_map, in_move, out_piece_map, out_move, exception

    def case_exc_no_rook_to_castle(self) -> _TestMakeMoveCase:
        in_piece_map: dict[Square, Piece] = {Square.E1: King(Color.WHITE, Square.E1)}
        in_move = CastlingMove(
            start=King(Color.WHITE, Square.E1),
            end=King(Color.WHITE, Square.G1),
            castled_rook=BaseMove(
                start=Rook(Color.WHITE, Square.H1), end=Rook(Color.WHITE, Square.F1)
            ),
        )
        out_piece_map = in_piece_map
        out_move = in_move
        exception = True
        return in_piece_map, in_move, out_piece_map, out_move, exception

    def case_exc_move_piece_is_different_than_board_piece(self) -> _TestMakeMoveCase:
        in_piece_map: dict[Square, Piece] = {Square.D5: King(Color.WHITE, Square.D5)}
        in_move = SinglePieceMove(
            start=King(Color.BLACK, Square.D5),
            end=King(Color.BLACK, Square.D6),
        )
        out_piece_map: dict[Square, Piece] = {}
        out_move = in_move  # unused
        exception = True
        return in_piece_map, in_move, out_piece_map, out_move, exception

    def case_exc_move_piece_is_diff_than_board_piece_castle(self) -> _TestMakeMoveCase:
        in_piece_map: dict[Square, Piece] = {
            Square.E1: King(Color.WHITE, Square.E1),
            Square.G1: King(Color.BLACK, Square.H1),
        }
        in_move = CastlingMove(
            start=King(Color.WHITE, Square.E1),
            end=King(Color.WHITE, Square.G1),
            castled_rook=BaseMove(
                start=Rook(Color.WHITE, Square.H1), end=Rook(Color.WHITE, Square.F1)
            ),
        )
        out_piece_map = in_piece_map
        out_move = in_move
        exception = True
        return in_piece_map, in_move, out_piece_map, out_move, exception

    def case_exc_attempted_to_capture_own_color_piece(self) -> _TestMakeMoveCase:
        in_piece_map: dict[Square, Piece] = {
            Square.D5: King(Color.WHITE, Square.D5),
            Square.D6: Pawn(Color.WHITE, Square.D6),
        }
        in_move = SinglePieceMove(
            start=King(Color.WHITE, Square.D5),
            end=King(Color.WHITE, Square.D6),
        )
        out_piece_map: dict[Square, Piece] = {}
        out_move = in_move  # unused
        exception = True
        return in_piece_map, in_move, out_piece_map, out_move, exception

    def case_move_to_unoccupied_square(self) -> _TestMakeMoveCase:
        in_piece_map: dict[Square, Piece] = {Square.D5: King(Color.WHITE, Square.D5)}
        in_move = SinglePieceMove(
            start=King(Color.WHITE, Square.D5),
            end=King(Color.WHITE, Square.D6),
        )
        out_piece_map: dict[Square, Piece] = {Square.D6: King(Color.WHITE, Square.D6)}
        out_move = SinglePieceMove(
            start=King(Color.WHITE, Square.D5),
            end=King(Color.WHITE, Square.D6),
        )
        exception = False
        return in_piece_map, in_move, out_piece_map, out_move, exception

    def case_move_to_occupied_square(self) -> _TestMakeMoveCase:
        in_piece_map: dict[Square, Piece] = {
            Square.D5: King(Color.WHITE, Square.D5),
            Square.D6: Pawn(Color.BLACK, Square.D6),
        }
        in_move = SinglePieceMove(
            start=King(Color.WHITE, Square.D5),
            end=King(Color.WHITE, Square.D6),
            captures=None,
        )
        out_piece_map: dict[Square, Piece] = {
            Square.D6: King(Color.WHITE, Square.D6),
        }
        out_move = SinglePieceMove(
            start=King(Color.WHITE, Square.D5),
            end=King(Color.WHITE, Square.D6),
            captures=Pawn(Color.BLACK, Square.D6),
        )
        exception = False
        return in_piece_map, in_move, out_piece_map, out_move, exception

    def case_make_castling_move(self) -> _TestMakeMoveCase:
        in_piece_map: dict[Square, Piece] = {
            Square.E1: King(Color.WHITE, Square.E1),
            Square.H1: Rook(Color.WHITE, Square.H1),
        }
        in_move = CastlingMove(
            start=King(Color.WHITE, Square.E1),
            end=King(Color.WHITE, Square.G1),
            castled_rook=BaseMove(
                start=Rook(Color.WHITE, Square.H1), end=Rook(Color.WHITE, Square.F1)
            ),
        )
        out_piece_map: dict[Square, Piece] = {
            Square.F1: Rook(Color.WHITE, Square.F1),
            Square.G1: King(Color.WHITE, Square.G1),
        }
        out_move = in_move
        exception = False
        return in_piece_map, in_move, out_piece_map, out_move, exception


_TestUnmakeMoveCase = tuple[
    dict[Square, Piece],
    Move,
    dict[Square, Piece],
    bool,
]


class TestUnmakeMoveCases:
    def case_exc_piece_found_on_move_start_square(self) -> _TestUnmakeMoveCase:
        in_piece_map: dict[Square, Piece] = {
            Square.D5: Pawn(Color.WHITE, Square.D5),
            Square.D6: King(Color.WHITE, Square.D6),
        }
        in_move = SinglePieceMove(
            start=King(Color.WHITE, Square.D5),
            end=King(Color.WHITE, Square.D6),
        )
        out_piece_map: dict[Square, Piece] = {}
        exception = True
        return in_piece_map, in_move, out_piece_map, exception

    def case_exc_main_piece_was_not_found_on_end_square(self) -> _TestUnmakeMoveCase:
        in_piece_map: dict[Square, Piece] = {Square.D6: Pawn(Color.WHITE, Square.D6)}
        in_move = SinglePieceMove(
            start=King(Color.WHITE, Square.D5),
            end=King(Color.WHITE, Square.D6),
        )
        out_piece_map: dict[Square, Piece] = {}
        exception = True
        return in_piece_map, in_move, out_piece_map, exception

    def case_exc_no_piece_on_square_where_capture_occurred(self) -> _TestUnmakeMoveCase:
        in_piece_map: dict[Square, Piece] = {Square.D5: King(Color.WHITE, Square.D5)}
        in_move = SinglePieceMove(
            start=King(Color.WHITE, Square.D5),
            end=King(Color.WHITE, Square.D6),
            captures=Pawn(Color.BLACK, Square.D6),
        )
        out_piece_map: dict[Square, Piece] = {}
        exception = True
        return in_piece_map, in_move, out_piece_map, exception

    def case_revert_move_without_a_capture(self) -> _TestUnmakeMoveCase:
        in_piece_map: dict[Square, Piece] = {Square.D6: King(Color.WHITE, Square.D6)}
        in_move = SinglePieceMove(
            start=King(Color.WHITE, Square.D5),
            end=King(Color.WHITE, Square.D6),
        )
        out_piece_map: dict[Square, Piece] = {Square.D5: King(Color.WHITE, Square.D5)}
        exception = False
        return in_piece_map, in_move, out_piece_map, exception

    def case_revert_move_with_a_capture(self) -> _TestUnmakeMoveCase:
        in_piece_map: dict[Square, Piece] = {Square.D6: King(Color.WHITE, Square.D6)}
        in_move = SinglePieceMove(
            start=King(Color.WHITE, Square.D5),
            end=King(Color.WHITE, Square.D6),
            captures=Pawn(Color.BLACK, Square.D6),
        )
        out_piece_map: dict[Square, Piece] = {
            Square.D5: King(Color.WHITE, Square.D5),
            Square.D6: Pawn(Color.BLACK, Square.D6),
        }
        exception = False
        return in_piece_map, in_move, out_piece_map, exception

    def case_revert_a_castling_move(self) -> _TestUnmakeMoveCase:
        in_piece_map: dict[Square, Piece] = {
            Square.F1: Rook(Color.WHITE, Square.F1),
            Square.G1: King(Color.WHITE, Square.G1),
        }
        in_move = CastlingMove(
            start=King(Color.WHITE, Square.E1),
            end=King(Color.WHITE, Square.G1),
            castled_rook=BaseMove(
                start=Rook(Color.WHITE, Square.H1), end=Rook(Color.WHITE, Square.F1)
            ),
        )
        out_piece_map: dict[Square, Piece] = {
            Square.E1: King(Color.WHITE, Square.E1),
            Square.H1: Rook(Color.WHITE, Square.H1),
        }
        exception = False
        return in_piece_map, in_move, out_piece_map, exception


_TestMakeAndUnmakeMoveCases = tuple[
    dict[Square, Piece],
    Move,
]


class TestMakeAndUnmakeMoveCases:
    def case_single_king_move(self) -> _TestMakeAndUnmakeMoveCases:
        start_map: dict[Square, Piece] = {
            Square.E4: King(Color.BLACK, Square.E4),
            Square.E5: Pawn(Color.WHITE, Square.E5),
        }
        move = SinglePieceMove(
            start=King(Color.BLACK, Square.E4),
            end=King(Color.BLACK, Square.E5),
        )
        return start_map, move

    def case_en_passant(self) -> _TestMakeAndUnmakeMoveCases:
        pawn = Pawn(Color.WHITE, Square.B5)
        start_map: dict[Square, Piece] = {
            Square.C5: Pawn(Color.BLACK, Square.C5),
            Square.B4: King(Color.WHITE, Square.B4),
            Square.B5: pawn,
        }
        move = SinglePieceMove(
            start=pawn,
            end=Pawn(Color.WHITE, Square.C6),
            captures=Pawn(Color.BLACK, Square.C5),
        )
        return start_map, move


_TestGenerateCastlingMovesCase = tuple[
    dict[Square, Piece],
    CastleRights,
    Color,
    set[CastlingMove],
]


class TestGenerateCastlingMovesCases:
    def case_side_to_move_has_no_castle_rights(self) -> _TestGenerateCastlingMovesCase:
        piece_map: dict[Square, Piece] = {}
        castle_rights = CastleRights(
            _rights={
                Color.WHITE: {CastleSide.SHORT: False, CastleSide.LONG: False},
                Color.BLACK: {CastleSide.SHORT: True, CastleSide.LONG: True},
            }
        )
        to_move = Color.WHITE
        exp_moves: set[CastlingMove] = set()

        return piece_map, castle_rights, to_move, exp_moves

    def case_able_to_castle_short(self) -> _TestGenerateCastlingMovesCase:
        piece_map: dict[Square, Piece] = {
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
        exp_moves = {
            CastlingMove(
                start=King(Color.BLACK, Square.E8),
                end=King(Color.BLACK, Square.G8),
                castled_rook=BaseMove(
                    start=Rook(Color.BLACK, Square.H8),
                    end=Rook(Color.BLACK, Square.F8),
                ),
            )
        }
        return piece_map, castle_rights, to_move, exp_moves

    def case_able_to_castle_long(self) -> _TestGenerateCastlingMovesCase:
        piece_map: dict[Square, Piece] = {
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
        exp_moves = {
            CastlingMove(
                start=King(Color.BLACK, Square.E8),
                end=King(Color.BLACK, Square.C8),
                castled_rook=BaseMove(
                    start=Rook(Color.BLACK, Square.A8), end=Rook(Color.BLACK, Square.D8)
                ),
            ),
        }
        return piece_map, castle_rights, to_move, exp_moves

    def case_cant_castle_through_check(self) -> _TestGenerateCastlingMovesCase:
        piece_map: dict[Square, Piece] = {
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
        exp_moves: set[CastlingMove] = set()
        return piece_map, castle_rights, to_move, exp_moves

    def case_cant_castle_ending_in_check(self) -> _TestGenerateCastlingMovesCase:
        piece_map: dict[Square, Piece] = {
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
        exp_moves = {
            CastlingMove(
                start=King(Color.WHITE, Square.E1),
                end=King(Color.WHITE, Square.G1),
                castled_rook=BaseMove(
                    start=Rook(Color.WHITE, Square.H1), end=Rook(Color.WHITE, Square.F1)
                ),
            )
        }
        return piece_map, castle_rights, to_move, exp_moves

    def case_cant_castle_through_another_piece(self) -> _TestGenerateCastlingMovesCase:
        piece_map: dict[Square, Piece] = {
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
        exp_moves: set[CastlingMove] = set()
        return piece_map, castle_rights, to_move, exp_moves
