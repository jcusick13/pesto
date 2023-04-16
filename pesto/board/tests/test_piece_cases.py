from pesto.board.enums import Square
from pesto.core.enums import Color

_TestPawnPsuedoLegalMovesCase = tuple[
    Color,
    Square,
    set[Square],
    bool,
    bool,
    bool,
    set[Square],
]


class TestPawnPsuedoLegalMovesCases:
    def case_white_first_move(self) -> _TestPawnPsuedoLegalMovesCase:
        color = Color.WHITE
        curr = Square.D2
        piece_set = {Square.D2}
        first_move = True
        ep_l = ep_r = False
        exp = {Square.D3, Square.D4}
        return color, curr, piece_set, first_move, ep_l, ep_r, exp

    def case_black_first_move(self) -> _TestPawnPsuedoLegalMovesCase:
        color = Color.BLACK
        curr = Square.C7
        piece_set = {Square.C7}
        first_move = True
        ep_l = ep_r = False
        exp = {Square.C6, Square.C5}
        return color, curr, piece_set, first_move, ep_l, ep_r, exp

    def case_white_blocked(self) -> _TestPawnPsuedoLegalMovesCase:
        color = Color.WHITE
        curr = Square.D7
        piece_set = {Square.D7, Square.D8}
        first_move = ep_l = ep_r = False
        exp: set[Square] = set()
        return color, curr, piece_set, first_move, ep_l, ep_r, exp

    def case_black_blocked(self) -> _TestPawnPsuedoLegalMovesCase:
        color = Color.BLACK
        curr = Square.A6
        piece_set = {Square.A6, Square.A5}
        first_move = ep_l = ep_r = False
        exp: set[Square] = set()
        return color, curr, piece_set, first_move, ep_l, ep_r, exp

    def case_white_capture(self) -> _TestPawnPsuedoLegalMovesCase:
        color = Color.WHITE
        curr = Square.D5
        piece_set = {Square.D5, Square.C6, Square.E6}
        first_move = ep_l = ep_r = False
        exp = {Square.C6, Square.E6, Square.D6}
        return color, curr, piece_set, first_move, ep_l, ep_r, exp

    def case_black_capture(self) -> _TestPawnPsuedoLegalMovesCase:
        color = Color.BLACK
        curr = Square.G4
        piece_set = {Square.G4, Square.H3, Square.F3}
        first_move = ep_l = ep_r = False
        exp = {Square.H3, Square.F3, Square.G3}
        return color, curr, piece_set, first_move, ep_l, ep_r, exp

    def case_white_en_passant(self) -> _TestPawnPsuedoLegalMovesCase:
        color = Color.WHITE
        curr = Square.G5
        piece_set = {Square.G5, Square.F5, Square.H5}
        first_move = False
        ep_l = ep_r = True
        exp = {Square.G6, Square.F6, Square.H6}
        return color, curr, piece_set, first_move, ep_l, ep_r, exp

    def case_black_en_passant(self) -> _TestPawnPsuedoLegalMovesCase:
        color = Color.BLACK
        curr = Square.D4
        piece_set = {Square.D4, Square.C4, Square.E4}
        first_move = False
        ep_l = ep_r = True
        exp = {Square.D3, Square.C3, Square.E3}
        return color, curr, piece_set, first_move, ep_l, ep_r, exp


_TestKnightPsuedoLegalMovesCase = tuple[
    Square,
    set[Square],
    set[Square],
]


class TestKnightPsuedoLegalMovesCases:
    def case_center_of_empty_board(self) -> _TestKnightPsuedoLegalMovesCase:
        curr = Square.E4
        piece_set = {Square.E4}
        exp = {
            # fmt: off
            Square.F6, Square.G5, Square.G3, Square.F2,
            Square.D2, Square.C3, Square.C5, Square.D6,
            # fmt: on
        }
        return curr, piece_set, exp

    def case_edge_of_empty_board(self) -> _TestKnightPsuedoLegalMovesCase:
        curr = Square.B8
        piece_set = {Square.B8}
        exp = {Square.A6, Square.C6, Square.D7}
        return curr, piece_set, exp

    def case_completely_surrounded(self) -> _TestKnightPsuedoLegalMovesCase:
        curr = Square.E4
        piece_set = {
            # fmt: off
            Square.D3, Square.E3, Square.F3, Square.D4,
            Square.F4, Square.D5, Square.E5, Square.F5
            # fmt: on
        }
        exp = {
            # fmt: off
            Square.F6, Square.G5, Square.G3, Square.F2,
            Square.D2, Square.C3, Square.C5, Square.D6,
            # fmt: on
        }
        return curr, piece_set, exp


_TestBishopPsuedoLegalMovesCase = tuple[
    Square,
    set[Square],
    set[Square],
]


class TestBishopPsuedoLegalMovesCases:
    def case_center_of_empty_board(self) -> _TestBishopPsuedoLegalMovesCase:
        curr = Square.E5
        piece_set = {Square.E5}
        exp = {
            # fmt: off
            Square.A1, Square.B2, Square.C3, Square.D4, Square.F6, Square.G7, Square.H8,
            Square.B8, Square.C7, Square.D6, Square.F4, Square.G3, Square.H2,
            # fmt: on
        }
        return curr, piece_set, exp

    def case_edge_of_empty_board(self) -> _TestBishopPsuedoLegalMovesCase:
        curr = Square.B7
        piece_set = {Square.B7}
        exp = {
            # fmt: off
            Square.A6, Square.C8,
            Square.A8, Square.C6, Square.D5, Square.E4, Square.F3, Square.G2, Square.H1,
            # fmt: on
        }
        return curr, piece_set, exp

    def case_completely_surrounded(self) -> _TestBishopPsuedoLegalMovesCase:
        curr = Square.E3
        piece_set = {Square.E3, Square.D2, Square.D4, Square.F4, Square.F2}
        exp = piece_set - {curr}
        return curr, piece_set, exp

    def case_limited_movement_in_corner(self) -> _TestBishopPsuedoLegalMovesCase:
        curr = Square.G2
        piece_set = {Square.G2, Square.F3}
        exp = {Square.F1, Square.H1, Square.H3, Square.F3}
        return curr, piece_set, exp


_TestRookPsuedoLegalMovesCase = tuple[
    Square,
    set[Square],
    set[Square],
]


class TestRookPsuedoLegalMovesCases:
    def case_center_of_empty_board(self) -> _TestRookPsuedoLegalMovesCase:
        curr = Square.D4
        piece_set = {Square.D4}
        exp = {
            # fmt: off
            Square.D1, Square.D2, Square.D3, Square.D5, Square.D6, Square.D7, Square.D8,
            Square.A4, Square.B4, Square.C4, Square.E4, Square.F4, Square.G4, Square.H4,
            # fmt: on
        }
        return curr, piece_set, exp

    def case_edge_of_empty_board(self) -> _TestRookPsuedoLegalMovesCase:
        curr = Square.H8
        piece_set = {Square.H8}
        exp = {
            # fmt: off
            Square.H7, Square.H6, Square.H5, Square.H4, Square.H3, Square.H2, Square.H1,
            Square.A8, Square.B8, Square.C8, Square.D8, Square.E8, Square.F8, Square.G8,
            # fmt: on
        }
        return curr, piece_set, exp

    def case_completely_surrounded(self) -> _TestRookPsuedoLegalMovesCase:
        curr = Square.D4
        piece_set = {Square.D4, Square.D5, Square.E4, Square.D3, Square.C4}
        exp = piece_set - {curr}
        return curr, piece_set, exp

    def case_limited_movement_in_corner(self) -> _TestRookPsuedoLegalMovesCase:
        curr = Square.G7
        piece_set = {Square.G7, Square.F7, Square.G6}
        exp = {Square.G8, Square.H7, Square.F7, Square.G6}
        return curr, piece_set, exp


_TestQueenPsuedoLegalMovesCase = tuple[
    Square,
    set[Square],
    set[Square],
]


class TestQueenPsuedoLegalMovesCases:
    def case_center_of_empty_board(self) -> _TestQueenPsuedoLegalMovesCase:
        curr = Square.D5
        piece_set = {Square.D5}
        exp = {
            # fmt: off
            Square.D1, Square.D2, Square.D3, Square.D4, Square.D6, Square.D7, Square.D8,
            Square.A5, Square.B5, Square.C5, Square.E5, Square.F5, Square.G5, Square.H5,
            Square.A2, Square.B3, Square.C4, Square.E6, Square.F7, Square.G8,
            Square.A8, Square.B7, Square.C6, Square.E4, Square.F3, Square.G2, Square.H1,
            # fmt: on
        }
        return curr, piece_set, exp

    def case_edge_of_empty_board(self) -> _TestQueenPsuedoLegalMovesCase:
        curr = Square.G2
        piece_set = {Square.G2}
        exp = {
            # fmt: off
            Square.A2, Square.B2, Square.C2, Square.D2, Square.E2, Square.F2, Square.H2,
            Square.G1, Square.G3, Square.G4, Square.G5, Square.G6, Square.G7, Square.G8,
            Square.A8, Square.B7, Square.C6, Square.D5, Square.E4, Square.F3, Square.H1,
            Square.F1, Square.H3,
            # fmt: on
        }
        return curr, piece_set, exp

    def case_completely_surrounded(self) -> _TestQueenPsuedoLegalMovesCase:
        curr = Square.C4
        piece_set = {
            # fmt: off
            Square.C4, Square.C5, Square.D5, Square.D4, Square.D3,
            Square.C3, Square.B3, Square.B4, Square.B5,
            # fmt: on
        }
        exp = piece_set - {curr}
        return curr, piece_set, exp

    def case_limited_movement_in_corner(self) -> _TestQueenPsuedoLegalMovesCase:
        curr = Square.B7
        piece_set = {Square.A6, Square.B7, Square.C8, Square.B6, Square.C6, Square.C7}
        exp = {
            # fmt: off
            Square.A8, Square.A7, Square.B8, Square.A6,
            Square.C8, Square.B6, Square.C6, Square.C7,
            # fmt: on
        }
        return curr, piece_set, exp


_TestKingPsuedoLegalMovesCase = tuple[
    Square,
    set[Square],
    set[Square],
]


class TestKingPsuedoLegalMovesCases:
    def case_center_of_empty_board(self) -> _TestKingPsuedoLegalMovesCase:
        curr = Square.D5
        piece_set = {Square.D5}
        exp = {
            # fmt: off
            Square.C4, Square.D4, Square.E4, Square.C5,
            Square.E5, Square.C6, Square.D6, Square.E6,
            # fmt: on
        }
        return curr, piece_set, exp

    def case_edge_of_empty_board(self) -> _TestKingPsuedoLegalMovesCase:
        curr = Square.H1
        piece_set = {Square.H1}
        exp = {Square.G1, Square.G2, Square.H2}
        return curr, piece_set, exp

    def case_completely_surrounded(self) -> _TestKingPsuedoLegalMovesCase:
        curr = Square.B6
        piece_set = {
            # fmt: off
            Square.A5, Square.B5, Square.C5, Square.A6,
            Square.C6, Square.A7, Square.B7, Square.C7, Square.B6
        }
        exp = piece_set - {curr}
        return curr, piece_set, exp

    def case_limited_movement_in_corner(self) -> _TestKingPsuedoLegalMovesCase:
        curr = Square.H8
        piece_set = {Square.H8, Square.G7, Square.H7}
        exp = {Square.G8, Square.G7, Square.H7}
        return curr, piece_set, exp
