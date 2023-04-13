from pesto.board.enums import Square

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
        exp: set[Square] = set()
        return curr, piece_set, exp

    def case_limited_movement_in_corner(self) -> _TestBishopPsuedoLegalMovesCase:
        curr = Square.G2
        piece_set = {Square.G2, Square.F3}
        exp = {Square.F1, Square.H1, Square.H3}
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
        exp: set[Square] = set()
        return curr, piece_set, exp

    def case_limited_movement_in_corner(self) -> _TestRookPsuedoLegalMovesCase:
        curr = Square.G7
        piece_set = {Square.G7, Square.F7, Square.G6}
        exp = {Square.G8, Square.H7}
        return curr, piece_set, exp
