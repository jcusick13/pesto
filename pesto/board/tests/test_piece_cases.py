from typing import Mapping

from pesto.board.piece import Bishop, King, Knight, Rook, Pawn, Piece, Queen
from pesto.board.square import Square
from pesto.core.enums import Color

_TestPawnPsuedoLegalMovesCase = tuple[
    Pawn,
    Mapping[Square, Piece],
    set[Square],
]


class TestPawnPsuedoLegalMovesCases:
    def case_white_first_move(self) -> _TestPawnPsuedoLegalMovesCase:
        pawn = Pawn(Color.WHITE, Square.D2)
        pawn.is_first_move = True
        piece_map = {Square.D2: pawn}
        exp = {Square.D3, Square.D4}
        return pawn, piece_map, exp

    def case_black_first_move(self) -> _TestPawnPsuedoLegalMovesCase:
        pawn = Pawn(Color.BLACK, Square.C7)
        pawn.is_first_move = True
        piece_map = {Square.C7: pawn}
        exp = {Square.C6, Square.C5}
        return pawn, piece_map, exp

    def case_white_blocked(self) -> _TestPawnPsuedoLegalMovesCase:
        pawn = Pawn(Color.WHITE, Square.D7)
        pawn.is_first_move = False
        piece_map = {
            Square.D7: pawn,
            Square.D8: Rook(Color.BLACK, Square.D8),
        }
        exp: set[Square] = set()
        return pawn, piece_map, exp

    def case_black_blocked(self) -> _TestPawnPsuedoLegalMovesCase:
        pawn = Pawn(Color.BLACK, Square.A6)
        pawn.is_first_move = False
        piece_map = {
            Square.A6: pawn,
            Square.A5: Rook(Color.WHITE, Square.A5),
        }
        exp: set[Square] = set()
        return pawn, piece_map, exp

    def case_white_capture(self) -> _TestPawnPsuedoLegalMovesCase:
        pawn = Pawn(Color.WHITE, Square.D5)
        pawn.is_first_move = False
        piece_map = {
            Square.D5: pawn,
            Square.C6: Rook(Color.BLACK, Square.C6),
            Square.E6: Rook(Color.BLACK, Square.E6),
        }
        exp = {Square.C6, Square.E6, Square.D6}
        return pawn, piece_map, exp

    def case_black_capture(self) -> _TestPawnPsuedoLegalMovesCase:
        pawn = Pawn(Color.BLACK, Square.G4)
        pawn.is_first_move = False
        piece_map = {
            Square.G4: pawn,
            Square.H3: Rook(Color.WHITE, Square.H3),
            Square.F3: Rook(Color.WHITE, Square.F3),
        }
        exp = {Square.H3, Square.F3, Square.G3}
        return pawn, piece_map, exp

    def case_white_cant_capture_white(self) -> _TestPawnPsuedoLegalMovesCase:
        pawn = Pawn(Color.WHITE, Square.E4)
        pawn.is_first_move = False
        piece_map = {
            Square.E4: pawn,
            Square.D5: Rook(Color.WHITE, Square.D5),
            Square.F5: Rook(Color.WHITE, Square.F5),
        }
        exp = {Square.E5}
        return pawn, piece_map, exp

    def case_black_cant_capture_black(self) -> _TestPawnPsuedoLegalMovesCase:
        pawn = Pawn(Color.BLACK, Square.D6)
        pawn.is_first_move = False
        piece_map = {
            Square.D6: pawn,
            Square.C5: Rook(Color.BLACK, Square.C5),
            Square.E5: Rook(Color.BLACK, Square.E5),
        }
        exp = {Square.D5}
        return pawn, piece_map, exp


_TestKnightPsuedoLegalMovesCase = tuple[
    Knight,
    Mapping[Square, Piece],
    set[Square],
]


class TestKnightPsuedoLegalMovesCases:
    def case_center_of_empty_board(self) -> _TestKnightPsuedoLegalMovesCase:
        knight = Knight(Color.BLACK, Square.E4)
        piece_map = {Square.E4: knight}
        exp = {
            # fmt: off
            Square.F6, Square.G5, Square.G3, Square.F2,
            Square.D2, Square.C3, Square.C5, Square.D6,
            # fmt: on
        }
        return knight, piece_map, exp

    def case_edge_of_empty_board(self) -> _TestKnightPsuedoLegalMovesCase:
        knight = Knight(Color.WHITE, Square.B8)
        piece_map = {Square.B8: knight}
        exp = {Square.A6, Square.C6, Square.D7}
        return knight, piece_map, exp

    def case_completely_surrounded(self) -> _TestKnightPsuedoLegalMovesCase:
        knight = Knight(Color.BLACK, Square.E4)
        piece_map = {
            Square.E4: knight,
            Square.D3: Rook(Color.WHITE, Square.D3),
            Square.E3: Rook(Color.WHITE, Square.E3),
            Square.F3: Rook(Color.WHITE, Square.F3),
            Square.D4: Rook(Color.WHITE, Square.D4),
            Square.F4: Rook(Color.WHITE, Square.F4),
            Square.D5: Rook(Color.WHITE, Square.D5),
            Square.E5: Rook(Color.WHITE, Square.E5),
            Square.F5: Rook(Color.WHITE, Square.F5),
        }
        exp = {
            # fmt: off
            Square.F6, Square.G5, Square.G3, Square.F2,
            Square.D2, Square.C3, Square.C5, Square.D6,
            # fmt: on
        }
        return knight, piece_map, exp

    def case_cant_capture_same_color(self) -> _TestKnightPsuedoLegalMovesCase:
        knight = Knight(Color.WHITE, Square.E4)
        piece_map = {
            Square.E4: knight,
            Square.F6: Rook(Color.WHITE, Square.F6),
            Square.G5: Rook(Color.WHITE, Square.G5),
            Square.G3: Rook(Color.WHITE, Square.G3),
            Square.F2: Rook(Color.WHITE, Square.F2),
            Square.D2: Rook(Color.WHITE, Square.D2),
            Square.C3: Rook(Color.WHITE, Square.C3),
            Square.C5: Rook(Color.WHITE, Square.C5),
            Square.D6: Rook(Color.WHITE, Square.D6),
        }
        exp: set[Square] = set()
        return knight, piece_map, exp


_TestBishopPsuedoLegalMovesCase = tuple[
    Bishop,
    Mapping[Square, Piece],
    set[Square],
]


class TestBishopPsuedoLegalMovesCases:
    def case_center_of_empty_board(self) -> _TestBishopPsuedoLegalMovesCase:
        bishop = Bishop(Color.BLACK, Square.E5)
        piece_map = {Square.E5: bishop}
        exp = {
            # fmt: off
            Square.A1, Square.B2, Square.C3, Square.D4, Square.F6, Square.G7, Square.H8,
            Square.B8, Square.C7, Square.D6, Square.F4, Square.G3, Square.H2,
            # fmt: on
        }
        return bishop, piece_map, exp

    def case_edge_of_empty_board(self) -> _TestBishopPsuedoLegalMovesCase:
        bishop = Bishop(Color.WHITE, Square.B7)
        piece_map = {Square.B7: bishop}
        exp = {
            # fmt: off
            Square.A6, Square.C8,
            Square.A8, Square.C6, Square.D5, Square.E4, Square.F3, Square.G2, Square.H1,
            # fmt: on
        }
        return bishop, piece_map, exp

    def case_completely_surrounded(self) -> _TestBishopPsuedoLegalMovesCase:
        bishop = Bishop(Color.WHITE, Square.E3)
        piece_map = {
            Square.E3: bishop,
            Square.D2: Rook(Color.BLACK, Square.D2),
            Square.D4: Rook(Color.BLACK, Square.D4),
            Square.F4: Rook(Color.BLACK, Square.F4),
            Square.F2: Rook(Color.BLACK, Square.F2),
        }
        exp = piece_map.keys() - {bishop.curr}
        return bishop, piece_map, exp

    def case_cant_capture_same_color(self) -> _TestBishopPsuedoLegalMovesCase:
        bishop = Bishop(Color.BLACK, Square.E3)
        piece_map = {
            Square.E3: bishop,
            Square.D2: Rook(Color.BLACK, Square.D2),
            Square.D4: Rook(Color.BLACK, Square.D4),
            Square.F4: Rook(Color.BLACK, Square.F4),
            Square.F2: Rook(Color.BLACK, Square.F2),
        }
        exp: set[Square] = set()
        return bishop, piece_map, exp

    def case_limited_movement_in_corner(self) -> _TestBishopPsuedoLegalMovesCase:
        bishop = Bishop(Color.BLACK, Square.G2)
        piece_map = {
            Square.G2: bishop,
            Square.F3: Rook(Color.WHITE, Square.F3),
        }
        exp = {Square.F1, Square.H1, Square.H3, Square.F3}
        return bishop, piece_map, exp


_TestRookPsuedoLegalMovesCase = tuple[
    Rook,
    Mapping[Square, Piece],
    set[Square],
]


class TestRookPsuedoLegalMovesCases:
    def case_center_of_empty_board(self) -> _TestRookPsuedoLegalMovesCase:
        rook = Rook(Color.WHITE, Square.D4)
        piece_map = {Square.D4: rook}
        exp = {
            # fmt: off
            Square.D1, Square.D2, Square.D3, Square.D5, Square.D6, Square.D7, Square.D8,
            Square.A4, Square.B4, Square.C4, Square.E4, Square.F4, Square.G4, Square.H4,
            # fmt: on
        }
        return rook, piece_map, exp

    def case_edge_of_empty_board(self) -> _TestRookPsuedoLegalMovesCase:
        rook = Rook(Color.BLACK, Square.H8)
        piece_map = {Square.H8: rook}
        exp = {
            # fmt: off
            Square.H7, Square.H6, Square.H5, Square.H4, Square.H3, Square.H2, Square.H1,
            Square.A8, Square.B8, Square.C8, Square.D8, Square.E8, Square.F8, Square.G8,
            # fmt: on
        }
        return rook, piece_map, exp

    def case_completely_surrounded(self) -> _TestRookPsuedoLegalMovesCase:
        rook = Rook(Color.BLACK, Square.D4)
        piece_map = {
            Square.D4: rook,
            Square.D5: Rook(Color.WHITE, Square.D5),
            Square.E4: Rook(Color.WHITE, Square.E4),
            Square.D3: Rook(Color.WHITE, Square.D3),
            Square.C4: Rook(Color.WHITE, Square.C4),
        }
        exp = piece_map.keys() - {rook.curr}
        return rook, piece_map, exp

    def case_cant_capture_same_color(self) -> _TestRookPsuedoLegalMovesCase:
        rook = Rook(Color.WHITE, Square.D4)
        piece_map = {
            Square.D4: rook,
            Square.D5: Rook(Color.WHITE, Square.D5),
            Square.E4: Rook(Color.WHITE, Square.E4),
            Square.D3: Rook(Color.WHITE, Square.D3),
            Square.C4: Rook(Color.WHITE, Square.C4),
        }
        exp: set[Square] = set()
        return rook, piece_map, exp

    def case_limited_movement_in_corner(self) -> _TestRookPsuedoLegalMovesCase:
        rook = Rook(Color.WHITE, Square.G7)
        piece_map = {
            Square.G7: rook,
            Square.F7: Rook(Color.BLACK, Square.F7),
            Square.G6: Rook(Color.BLACK, Square.G6),
        }
        exp = {Square.G8, Square.H7, Square.F7, Square.G6}
        return rook, piece_map, exp


_TestQueenPsuedoLegalMovesCase = tuple[
    Queen,
    Mapping[Square, Piece],
    set[Square],
]


class TestQueenPsuedoLegalMovesCases:
    def case_center_of_empty_board(self) -> _TestQueenPsuedoLegalMovesCase:
        queen = Queen(Color.WHITE, Square.D5)
        piece_map = {Square.D5: queen}
        exp = {
            # fmt: off
            Square.D1, Square.D2, Square.D3, Square.D4, Square.D6, Square.D7, Square.D8,
            Square.A5, Square.B5, Square.C5, Square.E5, Square.F5, Square.G5, Square.H5,
            Square.A2, Square.B3, Square.C4, Square.E6, Square.F7, Square.G8,
            Square.A8, Square.B7, Square.C6, Square.E4, Square.F3, Square.G2, Square.H1,
            # fmt: on
        }
        return queen, piece_map, exp

    def case_edge_of_empty_board(self) -> _TestQueenPsuedoLegalMovesCase:
        queen = Queen(Color.WHITE, Square.G2)
        piece_map = {Square.G2: queen}
        exp = {
            # fmt: off
            Square.A2, Square.B2, Square.C2, Square.D2, Square.E2, Square.F2, Square.H2,
            Square.G1, Square.G3, Square.G4, Square.G5, Square.G6, Square.G7, Square.G8,
            Square.A8, Square.B7, Square.C6, Square.D5, Square.E4, Square.F3, Square.H1,
            Square.F1, Square.H3,
            # fmt: on
        }
        return queen, piece_map, exp

    def case_completely_surrounded(self) -> _TestQueenPsuedoLegalMovesCase:
        queen = Queen(Color.WHITE, Square.C4)
        piece_map = {
            Square.C4: queen,
            Square.C5: Rook(Color.BLACK, Square.C5),
            Square.D5: Rook(Color.BLACK, Square.D5),
            Square.D4: Rook(Color.BLACK, Square.D4),
            Square.D3: Rook(Color.BLACK, Square.D3),
            Square.C3: Rook(Color.BLACK, Square.C3),
            Square.B3: Rook(Color.BLACK, Square.B3),
            Square.B4: Rook(Color.BLACK, Square.B4),
            Square.B5: Rook(Color.BLACK, Square.B5),
        }
        exp = piece_map.keys() - {queen.curr}
        return queen, piece_map, exp

    def case_cant_capture_same_color(self) -> _TestQueenPsuedoLegalMovesCase:
        queen = Queen(Color.BLACK, Square.C4)
        piece_map = {
            Square.C4: queen,
            Square.C5: Rook(Color.BLACK, Square.C5),
            Square.D5: Rook(Color.BLACK, Square.D5),
            Square.D4: Rook(Color.BLACK, Square.D4),
            Square.D3: Rook(Color.BLACK, Square.D3),
            Square.C3: Rook(Color.BLACK, Square.C3),
            Square.B3: Rook(Color.BLACK, Square.B3),
            Square.B4: Rook(Color.BLACK, Square.B4),
            Square.B5: Rook(Color.BLACK, Square.B5),
        }
        exp: set[Square] = set()
        return queen, piece_map, exp

    def case_limited_movement_in_corner(self) -> _TestQueenPsuedoLegalMovesCase:
        queen = Queen(Color.WHITE, Square.B7)
        piece_map = {
            Square.B7: queen,
            Square.A6: Rook(Color.BLACK, Square.A6),
            Square.C8: Rook(Color.BLACK, Square.C8),
            Square.B6: Rook(Color.BLACK, Square.B6),
            Square.C6: Rook(Color.BLACK, Square.C6),
            Square.C7: Rook(Color.BLACK, Square.C7),
        }
        exp = {
            # fmt: off
            Square.A8, Square.A7, Square.B8, Square.A6,
            Square.C8, Square.B6, Square.C6, Square.C7,
            # fmt: on
        }
        return queen, piece_map, exp


_TestKingPsuedoLegalMovesCase = tuple[
    King,
    Mapping[Square, Piece],
    set[Square],
]


class TestKingPsuedoLegalMovesCases:
    def case_center_of_empty_board(self) -> _TestKingPsuedoLegalMovesCase:
        king = King(Color.BLACK, Square.D5)
        piece_map = {Square.D5: king}
        exp = {
            # fmt: off
            Square.C4, Square.D4, Square.E4, Square.C5,
            Square.E5, Square.C6, Square.D6, Square.E6,
            # fmt: on
        }
        return king, piece_map, exp

    def case_edge_of_empty_board(self) -> _TestKingPsuedoLegalMovesCase:
        king = King(Color.WHITE, Square.H1)
        piece_map = {Square.H1: king}
        exp = {Square.G1, Square.G2, Square.H2}
        return king, piece_map, exp

    def case_completely_surrounded(self) -> _TestKingPsuedoLegalMovesCase:
        king = King(Color.WHITE, Square.B6)
        piece_map = {
            Square.B6: king,
            Square.A5: Rook(Color.BLACK, Square.A5),
            Square.B5: Rook(Color.BLACK, Square.B5),
            Square.C5: Rook(Color.BLACK, Square.C5),
            Square.A6: Rook(Color.BLACK, Square.A6),
            Square.C6: Rook(Color.BLACK, Square.C6),
            Square.A7: Rook(Color.BLACK, Square.A7),
            Square.B7: Rook(Color.BLACK, Square.B7),
            Square.C7: Rook(Color.BLACK, Square.C7),
        }
        exp = piece_map.keys() - {king.curr}
        return king, piece_map, exp

    def case_cant_capture_same_color(self) -> _TestKingPsuedoLegalMovesCase:
        king = King(Color.BLACK, Square.B6)
        piece_map = {
            Square.B6: king,
            Square.A5: Rook(Color.BLACK, Square.A5),
            Square.B5: Rook(Color.BLACK, Square.B5),
            Square.C5: Rook(Color.BLACK, Square.C5),
            Square.A6: Rook(Color.BLACK, Square.A6),
            Square.C6: Rook(Color.BLACK, Square.C6),
            Square.A7: Rook(Color.BLACK, Square.A7),
            Square.B7: Rook(Color.BLACK, Square.B7),
            Square.C7: Rook(Color.BLACK, Square.C7),
        }
        exp: set[Square] = set()
        return king, piece_map, exp

    def case_limited_movement_in_corner(self) -> _TestKingPsuedoLegalMovesCase:
        king = King(Color.BLACK, Square.H8)
        piece_map = {
            Square.H8: king,
            Square.G7: Rook(Color.WHITE, Square.G7),
            Square.H7: Rook(Color.WHITE, Square.H7),
        }
        exp = {Square.G8, Square.G7, Square.H7}
        return king, piece_map, exp
