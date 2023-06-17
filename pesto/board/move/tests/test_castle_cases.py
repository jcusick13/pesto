from pesto.board.move.castle import CastleRights, CastleSide, CastlingMove
from pesto.board.piece import BaseMove, King, Knight, Piece, Rook
from pesto.board.square import Square
from pesto.core.enums import Color

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
            Square.D8: Rook(Color.BLACK, Square.D8),
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

    def case_cant_castle_starting_in_check(self) -> _TestGenerateCastlingMovesCase:
        piece_map: dict[Square, Piece] = {
            Square.H8: Rook(Color.BLACK, Square.H8),
            Square.E8: King(Color.BLACK, Square.E8),
            Square.A8: King(Color.BLACK, Square.A8),
            Square.F6: Knight(Color.WHITE, Square.F6),
        }
        castle_rights = CastleRights.new()
        to_move = Color.BLACK
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

    def case_castle_when_rook_not_king_passes_through_check(
        self,
    ) -> _TestGenerateCastlingMovesCase:
        piece_map: dict[Square, Piece] = {
            Square.H8: Rook(Color.BLACK, Square.H8),
            Square.E8: King(Color.BLACK, Square.E8),
            Square.A8: Rook(Color.BLACK, Square.A8),
            Square.D7: Knight(Color.WHITE, Square.D7),
        }
        castle_rights = CastleRights(
            _rights={
                Color.WHITE: {CastleSide.SHORT: False, CastleSide.LONG: False},
                Color.BLACK: {CastleSide.SHORT: True, CastleSide.LONG: True},
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
            )
        }
        return piece_map, castle_rights, to_move, exp_moves
