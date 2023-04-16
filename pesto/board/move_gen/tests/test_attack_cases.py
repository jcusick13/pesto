from typing import Mapping, Optional

from pesto.board.enums import Square
from pesto.board.piece import Bishop, Pawn, Piece, Rook
from pesto.core.enums import Color

_TestSquareIsAttackedCase = tuple[Square, Mapping[Square, Piece], Optional[Color], bool]


class TestSquareIsAttackedCases:
    def case_no_pieces_on_board(self) -> _TestSquareIsAttackedCase:
        square = Square.D4
        piece_map: dict[Square, Piece] = {}
        by: Optional[Color] = None
        exp = False
        return square, piece_map, by, exp

    def case_attacked_once(self) -> _TestSquareIsAttackedCase:
        square = Square.A5
        piece_map = {Square.H5: Rook(Color.BLACK, Square.H5)}
        by: Optional[Color] = None
        exp = True
        return square, piece_map, by, exp

    def case_attacked_once_by_wrong_color(self) -> _TestSquareIsAttackedCase:
        square = Square.C6
        piece_map = {Square.C1: Rook(Color.WHITE, Square.C1)}
        by = Color.BLACK
        exp = False
        return square, piece_map, by, exp

    def case_attacked_multiple_times(self) -> _TestSquareIsAttackedCase:
        square = Square.F2
        piece_map = {
            Square.H4: Bishop(Color.WHITE, Square.H4),
            Square.F6: Rook(Color.WHITE, Square.F6),
        }
        by = Color.WHITE
        exp = True
        return square, piece_map, by, exp

    def case_attacker_is_blocked_by_piece(self) -> _TestSquareIsAttackedCase:
        square = Square.D8
        piece_map = {
            Square.D7: Pawn(Color.BLACK, Square.D7),
            Square.D3: Rook(Color.WHITE, Square.D3),
        }
        by: Optional[Color] = None
        exp = False
        return square, piece_map, by, exp
