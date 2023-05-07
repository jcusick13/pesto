from typing import Mapping

from pesto.board.move_gen.moves import Move
from pesto.board.piece import Bishop, King, Knight, Pawn, Piece, Rook
from pesto.board.square import Square
from pesto.core.enums import Color

_TestLegalMoveGeneratorCase = tuple[Mapping[Square, Piece], Color, list[Move]]


class TestLegalMoveGeneratorCases:
    def case_no_legal_moves(self) -> _TestLegalMoveGeneratorCase:
        """King is trapped in corner"""
        piece_map = {
            Square.A1: King(Color.WHITE, Square.A1),
            Square.H2: Rook(Color.BLACK, Square.H2),
            Square.B8: Rook(Color.BLACK, Square.B8),
        }
        to_move = Color.WHITE
        exp: list[Move] = []
        return piece_map, to_move, exp

    def case_no_legal_moves_piece_is_pinned(self) -> _TestLegalMoveGeneratorCase:
        """King is stalemated and lone piece in front of it is pinned"""
        piece_map = {
            Square.H8: King(Color.BLACK, Square.H8),
            Square.H7: Knight(Color.BLACK, Square.H7),
            Square.H1: Rook(Color.WHITE, Square.H1),
            Square.G1: Rook(Color.WHITE, Square.G1),
        }
        to_move = Color.BLACK
        exp: list[Move] = []
        return piece_map, to_move, exp

    def case_single_legal_non_king_move(self) -> _TestLegalMoveGeneratorCase:
        """King is trapped in corner, though one pawn is free to move"""
        pawn = Pawn(Color.WHITE, Square.E4)
        pawn.is_first_move = False

        piece_map = {
            Square.A1: King(Color.WHITE, Square.A1),
            Square.H2: Rook(Color.BLACK, Square.H2),
            Square.B8: Rook(Color.BLACK, Square.B8),
            Square.E4: pawn,
        }
        to_move = Color.WHITE
        exp = [
            Move(start=Pawn(Color.WHITE, Square.E4), end=Pawn(Color.WHITE, Square.E5))
        ]
        return piece_map, to_move, exp

    def case_single_legal_king_move(self) -> _TestLegalMoveGeneratorCase:
        """King is trapped along the a-file"""
        piece_map = {
            Square.A8: King(Color.BLACK, Square.A8),
            Square.B1: Rook(Color.WHITE, Square.B1),
        }
        to_move = Color.BLACK
        exp = [
            Move(start=King(Color.BLACK, Square.A8), end=King(Color.BLACK, Square.A7))
        ]
        return piece_map, to_move, exp

    def case_multiple_legal_moves(self) -> _TestLegalMoveGeneratorCase:
        pawn = Pawn(Color.WHITE, Square.B6)
        pawn.is_first_move = False
        piece_map = {
            Square.A8: King(Color.WHITE, Square.A8),
            Square.B6: pawn,
            Square.D6: Bishop(Color.BLACK, Square.D6),
        }
        to_move = Color.WHITE
        exp = [
            Move(start=King(Color.WHITE, Square.A8), end=King(Color.WHITE, Square.A7)),
            Move(start=King(Color.WHITE, Square.A8), end=King(Color.WHITE, Square.B7)),
            Move(start=Pawn(Color.WHITE, Square.B6), end=Pawn(Color.WHITE, Square.B7)),
        ]
        return piece_map, to_move, exp
