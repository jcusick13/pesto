from typing import Mapping, Optional

from pesto.board.piece import Bishop, King, Knight, Move, Rook, Pawn, Piece, Queen
from pesto.board.square import Square
from pesto.core.enums import Color

_TestPawnPsuedoLegalMovesCase = tuple[
    Pawn,
    Mapping[Square, Piece],
    Optional[Square],
    set[Move],
]


class TestPawnPsuedoLegalMovesCases:
    def case_white_first_move(self) -> _TestPawnPsuedoLegalMovesCase:
        pawn = Pawn(Color.WHITE, Square.D2)
        pawn.is_first_move = True
        piece_map = {Square.D2: pawn}
        ep_square: Optional[Square] = None
        exp = {
            Move(pawn, Pawn(Color.WHITE, Square.D3)),
            Move(pawn, Pawn(Color.WHITE, Square.D4)),
        }
        return pawn, piece_map, ep_square, exp

    def case_black_first_move(self) -> _TestPawnPsuedoLegalMovesCase:
        pawn = Pawn(Color.BLACK, Square.C7)
        pawn.is_first_move = True
        piece_map = {Square.C7: pawn}
        ep_square: Optional[Square] = None
        exp = {
            Move(pawn, Pawn(Color.BLACK, Square.C6)),
            Move(pawn, Pawn(Color.BLACK, Square.C5)),
        }
        return pawn, piece_map, ep_square, exp

    def case_white_blocked(self) -> _TestPawnPsuedoLegalMovesCase:
        pawn = Pawn(Color.WHITE, Square.D7)
        pawn.is_first_move = False
        piece_map = {
            Square.D7: pawn,
            Square.D8: Rook(Color.BLACK, Square.D8),
        }
        ep_square: Optional[Square] = None
        exp: set[Move] = set()
        return pawn, piece_map, ep_square, exp

    def case_black_blocked(self) -> _TestPawnPsuedoLegalMovesCase:
        pawn = Pawn(Color.BLACK, Square.A6)
        pawn.is_first_move = False
        piece_map = {
            Square.A6: pawn,
            Square.A5: Rook(Color.WHITE, Square.A5),
        }
        ep_square: Optional[Square] = None
        exp: set[Move] = set()
        return pawn, piece_map, ep_square, exp

    def case_white_capture(self) -> _TestPawnPsuedoLegalMovesCase:
        pawn = Pawn(Color.WHITE, Square.D5)
        pawn.is_first_move = False
        piece_map = {
            Square.D5: pawn,
            Square.C6: Rook(Color.BLACK, Square.C6),
            Square.E6: Rook(Color.BLACK, Square.E6),
        }
        ep_square: Optional[Square] = None
        exp = {
            Move(pawn, Pawn(Color.WHITE, Square.C6)),
            Move(pawn, Pawn(Color.WHITE, Square.E6)),
            Move(pawn, Pawn(Color.WHITE, Square.D6)),
        }
        return pawn, piece_map, ep_square, exp

    def case_black_capture(self) -> _TestPawnPsuedoLegalMovesCase:
        pawn = Pawn(Color.BLACK, Square.G4)
        pawn.is_first_move = False
        piece_map = {
            Square.G4: pawn,
            Square.H3: Rook(Color.WHITE, Square.H3),
            Square.F3: Rook(Color.WHITE, Square.F3),
        }
        ep_square: Optional[Square] = None
        exp = {
            Move(pawn, Pawn(Color.BLACK, Square.H3)),
            Move(pawn, Pawn(Color.BLACK, Square.F3)),
            Move(pawn, Pawn(Color.BLACK, Square.G3)),
        }
        return pawn, piece_map, ep_square, exp

    def case_white_cant_capture_white(self) -> _TestPawnPsuedoLegalMovesCase:
        pawn = Pawn(Color.WHITE, Square.E4)
        pawn.is_first_move = False
        piece_map = {
            Square.E4: pawn,
            Square.D5: Rook(Color.WHITE, Square.D5),
            Square.F5: Rook(Color.WHITE, Square.F5),
        }
        ep_square: Optional[Square] = None
        exp = {Move(pawn, Pawn(Color.WHITE, Square.E5))}
        return pawn, piece_map, ep_square, exp

    def case_black_cant_capture_black(self) -> _TestPawnPsuedoLegalMovesCase:
        pawn = Pawn(Color.BLACK, Square.D6)
        pawn.is_first_move = False
        piece_map = {
            Square.D6: pawn,
            Square.C5: Rook(Color.BLACK, Square.C5),
            Square.E5: Rook(Color.BLACK, Square.E5),
        }
        ep_square: Optional[Square] = None
        exp = {Move(pawn, Pawn(Color.BLACK, Square.D5))}
        return pawn, piece_map, ep_square, exp

    def case_white_promotes(self) -> _TestPawnPsuedoLegalMovesCase:
        pawn = Pawn(Color.WHITE, Square.D7)
        pawn.is_first_move = False
        piece_map = {Square.D7: pawn}
        ep_square: Optional[Square] = None
        exp = {
            Move(pawn, Knight(Color.WHITE, Square.D8)),
            Move(pawn, Bishop(Color.WHITE, Square.D8)),
            Move(pawn, Rook(Color.WHITE, Square.D8)),
            Move(pawn, Queen(Color.WHITE, Square.D8)),
        }
        return pawn, piece_map, ep_square, exp

    def case_black_promotes(self) -> _TestPawnPsuedoLegalMovesCase:
        pawn = Pawn(Color.BLACK, Square.E2)
        pawn.is_first_move = False
        piece_map = {Square.E2: pawn}
        ep_square: Optional[Square] = None
        exp = {
            Move(pawn, Knight(Color.BLACK, Square.E1)),
            Move(pawn, Bishop(Color.BLACK, Square.E1)),
            Move(pawn, Rook(Color.BLACK, Square.E1)),
            Move(pawn, Queen(Color.BLACK, Square.E1)),
        }
        return pawn, piece_map, ep_square, exp

    def case_white_captures_en_passant(self) -> _TestPawnPsuedoLegalMovesCase:
        pawn = Pawn(Color.WHITE, Square.A5)
        pawn.is_first_move = False
        target_pawn = Pawn(Color.BLACK, Square.B5)
        piece_map = {Square.A5: pawn, Square.B5: target_pawn}
        ep_square = Square.B6
        exp = {
            Move(pawn, Pawn(Color.WHITE, Square.A6)),
            Move(pawn, Pawn(Color.WHITE, Square.B6), captures=target_pawn),
        }
        return pawn, piece_map, ep_square, exp

    def case_black_captures_en_passant(self) -> _TestPawnPsuedoLegalMovesCase:
        pawn = Pawn(Color.BLACK, Square.B4)
        pawn.is_first_move = False
        target_pawn = Pawn(Color.WHITE, Square.C4)
        piece_map = {Square.B4: pawn, Square.C4: target_pawn}
        ep_square = Square.C3
        exp = {
            Move(pawn, Pawn(Color.BLACK, Square.B3)),
            Move(pawn, Pawn(Color.BLACK, Square.C3), captures=target_pawn),
        }
        return pawn, piece_map, ep_square, exp


_TestKnightPsuedoLegalMovesCase = tuple[
    Knight,
    Mapping[Square, Piece],
    set[Move],
]


class TestKnightPsuedoLegalMovesCases:
    def case_center_of_empty_board(self) -> _TestKnightPsuedoLegalMovesCase:
        knight = Knight(Color.BLACK, Square.E4)
        piece_map = {Square.E4: knight}
        exp = {
            Move(knight, Knight(Color.BLACK, Square.F6)),
            Move(knight, Knight(Color.BLACK, Square.G5)),
            Move(knight, Knight(Color.BLACK, Square.G3)),
            Move(knight, Knight(Color.BLACK, Square.F2)),
            Move(knight, Knight(Color.BLACK, Square.D2)),
            Move(knight, Knight(Color.BLACK, Square.C3)),
            Move(knight, Knight(Color.BLACK, Square.C5)),
            Move(knight, Knight(Color.BLACK, Square.D6)),
        }
        return knight, piece_map, exp

    def case_edge_of_empty_board(self) -> _TestKnightPsuedoLegalMovesCase:
        knight = Knight(Color.WHITE, Square.B8)
        piece_map = {Square.B8: knight}
        exp = {
            Move(knight, Knight(Color.WHITE, Square.A6)),
            Move(knight, Knight(Color.WHITE, Square.C6)),
            Move(knight, Knight(Color.WHITE, Square.D7)),
        }
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
            Move(knight, Knight(Color.BLACK, Square.F6)),
            Move(knight, Knight(Color.BLACK, Square.G5)),
            Move(knight, Knight(Color.BLACK, Square.G3)),
            Move(knight, Knight(Color.BLACK, Square.F2)),
            Move(knight, Knight(Color.BLACK, Square.D2)),
            Move(knight, Knight(Color.BLACK, Square.C3)),
            Move(knight, Knight(Color.BLACK, Square.C5)),
            Move(knight, Knight(Color.BLACK, Square.D6)),
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
        exp: set[Move] = set()
        return knight, piece_map, exp


_TestBishopPsuedoLegalMovesCase = tuple[
    Bishop,
    Mapping[Square, Piece],
    set[Move],
]


class TestBishopPsuedoLegalMovesCases:
    def case_center_of_empty_board(self) -> _TestBishopPsuedoLegalMovesCase:
        bishop = Bishop(Color.BLACK, Square.E5)
        piece_map = {Square.E5: bishop}
        exp = {
            Move(bishop, Bishop(Color.BLACK, Square.A1)),
            Move(bishop, Bishop(Color.BLACK, Square.B2)),
            Move(bishop, Bishop(Color.BLACK, Square.C3)),
            Move(bishop, Bishop(Color.BLACK, Square.D4)),
            Move(bishop, Bishop(Color.BLACK, Square.F6)),
            Move(bishop, Bishop(Color.BLACK, Square.G7)),
            Move(bishop, Bishop(Color.BLACK, Square.H8)),
            Move(bishop, Bishop(Color.BLACK, Square.B8)),
            Move(bishop, Bishop(Color.BLACK, Square.C7)),
            Move(bishop, Bishop(Color.BLACK, Square.D6)),
            Move(bishop, Bishop(Color.BLACK, Square.F4)),
            Move(bishop, Bishop(Color.BLACK, Square.G3)),
            Move(bishop, Bishop(Color.BLACK, Square.H2)),
        }
        return bishop, piece_map, exp

    def case_edge_of_empty_board(self) -> _TestBishopPsuedoLegalMovesCase:
        bishop = Bishop(Color.WHITE, Square.B7)
        piece_map = {Square.B7: bishop}
        exp = {
            Move(bishop, Bishop(Color.WHITE, Square.A6)),
            Move(bishop, Bishop(Color.WHITE, Square.C8)),
            Move(bishop, Bishop(Color.WHITE, Square.A8)),
            Move(bishop, Bishop(Color.WHITE, Square.C6)),
            Move(bishop, Bishop(Color.WHITE, Square.D5)),
            Move(bishop, Bishop(Color.WHITE, Square.E4)),
            Move(bishop, Bishop(Color.WHITE, Square.F3)),
            Move(bishop, Bishop(Color.WHITE, Square.G2)),
            Move(bishop, Bishop(Color.WHITE, Square.H1)),
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
        exp = {
            Move(bishop, Bishop(Color.WHITE, Square.D2)),
            Move(bishop, Bishop(Color.WHITE, Square.D4)),
            Move(bishop, Bishop(Color.WHITE, Square.F4)),
            Move(bishop, Bishop(Color.WHITE, Square.F2)),
        }
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
        exp: set[Move] = set()
        return bishop, piece_map, exp

    def case_limited_movement_in_corner(self) -> _TestBishopPsuedoLegalMovesCase:
        bishop = Bishop(Color.BLACK, Square.G2)
        piece_map = {
            Square.G2: bishop,
            Square.F3: Rook(Color.WHITE, Square.F3),
        }
        exp = {
            Move(bishop, Bishop(Color.BLACK, Square.F1)),
            Move(bishop, Bishop(Color.BLACK, Square.H1)),
            Move(bishop, Bishop(Color.BLACK, Square.H3)),
            Move(bishop, Bishop(Color.BLACK, Square.F3)),
        }
        return bishop, piece_map, exp


_TestRookPsuedoLegalMovesCase = tuple[
    Rook,
    Mapping[Square, Piece],
    set[Move],
]


class TestRookPsuedoLegalMovesCases:
    def case_center_of_empty_board(self) -> _TestRookPsuedoLegalMovesCase:
        rook = Rook(Color.WHITE, Square.D4)
        piece_map = {Square.D4: rook}
        exp = {
            Move(rook, Rook(Color.WHITE, Square.D1)),
            Move(rook, Rook(Color.WHITE, Square.D2)),
            Move(rook, Rook(Color.WHITE, Square.D3)),
            Move(rook, Rook(Color.WHITE, Square.D5)),
            Move(rook, Rook(Color.WHITE, Square.D6)),
            Move(rook, Rook(Color.WHITE, Square.D7)),
            Move(rook, Rook(Color.WHITE, Square.D8)),
            Move(rook, Rook(Color.WHITE, Square.A4)),
            Move(rook, Rook(Color.WHITE, Square.B4)),
            Move(rook, Rook(Color.WHITE, Square.C4)),
            Move(rook, Rook(Color.WHITE, Square.E4)),
            Move(rook, Rook(Color.WHITE, Square.F4)),
            Move(rook, Rook(Color.WHITE, Square.G4)),
            Move(rook, Rook(Color.WHITE, Square.H4)),
        }
        return rook, piece_map, exp

    def case_edge_of_empty_board(self) -> _TestRookPsuedoLegalMovesCase:
        rook = Rook(Color.BLACK, Square.H8)
        piece_map = {Square.H8: rook}
        exp = {
            Move(rook, Rook(Color.BLACK, Square.H7)),
            Move(rook, Rook(Color.BLACK, Square.H6)),
            Move(rook, Rook(Color.BLACK, Square.H5)),
            Move(rook, Rook(Color.BLACK, Square.H4)),
            Move(rook, Rook(Color.BLACK, Square.H3)),
            Move(rook, Rook(Color.BLACK, Square.H2)),
            Move(rook, Rook(Color.BLACK, Square.H1)),
            Move(rook, Rook(Color.BLACK, Square.A8)),
            Move(rook, Rook(Color.BLACK, Square.B8)),
            Move(rook, Rook(Color.BLACK, Square.C8)),
            Move(rook, Rook(Color.BLACK, Square.D8)),
            Move(rook, Rook(Color.BLACK, Square.E8)),
            Move(rook, Rook(Color.BLACK, Square.F8)),
            Move(rook, Rook(Color.BLACK, Square.G8)),
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
        exp = {
            Move(rook, Rook(Color.BLACK, Square.D5)),
            Move(rook, Rook(Color.BLACK, Square.E4)),
            Move(rook, Rook(Color.BLACK, Square.D3)),
            Move(rook, Rook(Color.BLACK, Square.C4)),
        }
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
        exp: set[Move] = set()
        return rook, piece_map, exp

    def case_limited_movement_in_corner(self) -> _TestRookPsuedoLegalMovesCase:
        rook = Rook(Color.WHITE, Square.G7)
        piece_map = {
            Square.G7: rook,
            Square.F7: Rook(Color.BLACK, Square.F7),
            Square.G6: Rook(Color.BLACK, Square.G6),
        }
        exp = {
            Move(rook, Rook(Color.WHITE, Square.G8)),
            Move(rook, Rook(Color.WHITE, Square.H7)),
            Move(rook, Rook(Color.WHITE, Square.F7)),
            Move(rook, Rook(Color.WHITE, Square.G6)),
        }
        return rook, piece_map, exp


_TestQueenPsuedoLegalMovesCase = tuple[
    Queen,
    Mapping[Square, Piece],
    set[Move],
]


class TestQueenPsuedoLegalMovesCases:
    def case_center_of_empty_board(self) -> _TestQueenPsuedoLegalMovesCase:
        queen = Queen(Color.WHITE, Square.D5)
        piece_map = {Square.D5: queen}
        exp = {
            Move(queen, Queen(Color.WHITE, Square.D1)),
            Move(queen, Queen(Color.WHITE, Square.D2)),
            Move(queen, Queen(Color.WHITE, Square.D3)),
            Move(queen, Queen(Color.WHITE, Square.D4)),
            Move(queen, Queen(Color.WHITE, Square.D6)),
            Move(queen, Queen(Color.WHITE, Square.D7)),
            Move(queen, Queen(Color.WHITE, Square.D8)),
            Move(queen, Queen(Color.WHITE, Square.A5)),
            Move(queen, Queen(Color.WHITE, Square.B5)),
            Move(queen, Queen(Color.WHITE, Square.C5)),
            Move(queen, Queen(Color.WHITE, Square.E5)),
            Move(queen, Queen(Color.WHITE, Square.F5)),
            Move(queen, Queen(Color.WHITE, Square.G5)),
            Move(queen, Queen(Color.WHITE, Square.H5)),
            Move(queen, Queen(Color.WHITE, Square.A2)),
            Move(queen, Queen(Color.WHITE, Square.B3)),
            Move(queen, Queen(Color.WHITE, Square.C4)),
            Move(queen, Queen(Color.WHITE, Square.E6)),
            Move(queen, Queen(Color.WHITE, Square.F7)),
            Move(queen, Queen(Color.WHITE, Square.G8)),
            Move(queen, Queen(Color.WHITE, Square.A8)),
            Move(queen, Queen(Color.WHITE, Square.B7)),
            Move(queen, Queen(Color.WHITE, Square.C6)),
            Move(queen, Queen(Color.WHITE, Square.E4)),
            Move(queen, Queen(Color.WHITE, Square.F3)),
            Move(queen, Queen(Color.WHITE, Square.G2)),
            Move(queen, Queen(Color.WHITE, Square.H1)),
        }
        return queen, piece_map, exp

    def case_edge_of_empty_board(self) -> _TestQueenPsuedoLegalMovesCase:
        queen = Queen(Color.WHITE, Square.G2)
        piece_map = {Square.G2: queen}
        exp = {
            Move(queen, Queen(Color.WHITE, Square.A2)),
            Move(queen, Queen(Color.WHITE, Square.B2)),
            Move(queen, Queen(Color.WHITE, Square.C2)),
            Move(queen, Queen(Color.WHITE, Square.D2)),
            Move(queen, Queen(Color.WHITE, Square.E2)),
            Move(queen, Queen(Color.WHITE, Square.F2)),
            Move(queen, Queen(Color.WHITE, Square.H2)),
            Move(queen, Queen(Color.WHITE, Square.G1)),
            Move(queen, Queen(Color.WHITE, Square.G3)),
            Move(queen, Queen(Color.WHITE, Square.G4)),
            Move(queen, Queen(Color.WHITE, Square.G5)),
            Move(queen, Queen(Color.WHITE, Square.G6)),
            Move(queen, Queen(Color.WHITE, Square.G7)),
            Move(queen, Queen(Color.WHITE, Square.G8)),
            Move(queen, Queen(Color.WHITE, Square.A8)),
            Move(queen, Queen(Color.WHITE, Square.B7)),
            Move(queen, Queen(Color.WHITE, Square.C6)),
            Move(queen, Queen(Color.WHITE, Square.D5)),
            Move(queen, Queen(Color.WHITE, Square.E4)),
            Move(queen, Queen(Color.WHITE, Square.F3)),
            Move(queen, Queen(Color.WHITE, Square.H1)),
            Move(queen, Queen(Color.WHITE, Square.F1)),
            Move(queen, Queen(Color.WHITE, Square.H3)),
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
        exp = {
            Move(queen, Queen(Color.WHITE, Square.C5)),
            Move(queen, Queen(Color.WHITE, Square.D5)),
            Move(queen, Queen(Color.WHITE, Square.D4)),
            Move(queen, Queen(Color.WHITE, Square.D3)),
            Move(queen, Queen(Color.WHITE, Square.C3)),
            Move(queen, Queen(Color.WHITE, Square.B3)),
            Move(queen, Queen(Color.WHITE, Square.B4)),
            Move(queen, Queen(Color.WHITE, Square.B5)),
        }
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
        exp: set[Move] = set()
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
            Move(queen, Queen(Color.WHITE, Square.A8)),
            Move(queen, Queen(Color.WHITE, Square.A7)),
            Move(queen, Queen(Color.WHITE, Square.B8)),
            Move(queen, Queen(Color.WHITE, Square.A6)),
            Move(queen, Queen(Color.WHITE, Square.C8)),
            Move(queen, Queen(Color.WHITE, Square.B6)),
            Move(queen, Queen(Color.WHITE, Square.C6)),
            Move(queen, Queen(Color.WHITE, Square.C7)),
        }
        return queen, piece_map, exp


_TestKingPsuedoLegalMovesCase = tuple[
    King,
    Mapping[Square, Piece],
    set[Move],
]


class TestKingPsuedoLegalMovesCases:
    def case_center_of_empty_board(self) -> _TestKingPsuedoLegalMovesCase:
        king = King(Color.BLACK, Square.D5)
        piece_map = {Square.D5: king}
        exp = {
            Move(king, King(Color.BLACK, Square.C4)),
            Move(king, King(Color.BLACK, Square.D4)),
            Move(king, King(Color.BLACK, Square.E4)),
            Move(king, King(Color.BLACK, Square.C5)),
            Move(king, King(Color.BLACK, Square.E5)),
            Move(king, King(Color.BLACK, Square.C6)),
            Move(king, King(Color.BLACK, Square.D6)),
            Move(king, King(Color.BLACK, Square.E6)),
        }
        return king, piece_map, exp

    def case_edge_of_empty_board(self) -> _TestKingPsuedoLegalMovesCase:
        king = King(Color.WHITE, Square.H1)
        piece_map = {Square.H1: king}
        exp = {
            Move(king, King(Color.WHITE, Square.G1)),
            Move(king, King(Color.WHITE, Square.G2)),
            Move(king, King(Color.WHITE, Square.H2)),
        }
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
        exp = {
            Move(king, King(Color.WHITE, Square.A5)),
            Move(king, King(Color.WHITE, Square.B5)),
            Move(king, King(Color.WHITE, Square.C5)),
            Move(king, King(Color.WHITE, Square.A6)),
            Move(king, King(Color.WHITE, Square.C6)),
            Move(king, King(Color.WHITE, Square.A7)),
            Move(king, King(Color.WHITE, Square.B7)),
            Move(king, King(Color.WHITE, Square.C7)),
        }
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
        exp: set[Move] = set()
        return king, piece_map, exp

    def case_limited_movement_in_corner(self) -> _TestKingPsuedoLegalMovesCase:
        king = King(Color.BLACK, Square.H8)
        piece_map = {
            Square.H8: king,
            Square.G7: Rook(Color.WHITE, Square.G7),
            Square.H7: Rook(Color.WHITE, Square.H7),
        }
        exp = {
            Move(king, King(Color.BLACK, Square.G8)),
            Move(king, King(Color.BLACK, Square.G7)),
            Move(king, King(Color.BLACK, Square.H7)),
        }
        return king, piece_map, exp
