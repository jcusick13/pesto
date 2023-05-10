# pylint: disable=duplicate-code

from pesto.board.board import Board, CastleRights, CastleSide
from pesto.board.piece import Bishop, King, Knight, Rook, Pawn, Queen
from pesto.board.square import Square
from pesto.core.enums import Color

_TestBoardFromFenCase = tuple[str, Board]


class TestBoardFromFenCases:
    def case_starting_position(self) -> _TestBoardFromFenCase:
        fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        board = Board.new()
        return fen, board

    def case_caro_kann_fantasy(self) -> _TestBoardFromFenCase:
        fen = "rnbqkbnr/pp2pppp/2p5/3p4/3PP3/5P2/PPP3PP/RNBQKBNR b KQkq - 0 3"
        board = Board(
            ply=6,
            halfmove_clock=0,
            to_move=Color.BLACK,
            piece_map={
                Square.A1: Rook(Color.WHITE, Square.A1),
                Square.B1: Knight(Color.WHITE, Square.B1),
                Square.C1: Bishop(Color.WHITE, Square.C1),
                Square.D1: Queen(Color.WHITE, Square.D1),
                Square.E1: King(Color.WHITE, Square.E1),
                Square.F1: Bishop(Color.WHITE, Square.F1),
                Square.G1: Knight(Color.WHITE, Square.G1),
                Square.H1: Rook(Color.WHITE, Square.H1),
                Square.A2: Pawn(Color.WHITE, Square.A2),
                Square.B2: Pawn(Color.WHITE, Square.B2),
                Square.C2: Pawn(Color.WHITE, Square.C2),
                Square.D4: Pawn(Color.WHITE, Square.D4),
                Square.E4: Pawn(Color.WHITE, Square.E4),
                Square.F3: Pawn(Color.WHITE, Square.F3),
                Square.G2: Pawn(Color.WHITE, Square.G2),
                Square.H2: Pawn(Color.WHITE, Square.H2),
                Square.A7: Pawn(Color.BLACK, Square.A7),
                Square.B7: Pawn(Color.BLACK, Square.B7),
                Square.C6: Pawn(Color.BLACK, Square.C6),
                Square.D5: Pawn(Color.BLACK, Square.D5),
                Square.E7: Pawn(Color.BLACK, Square.E7),
                Square.F7: Pawn(Color.BLACK, Square.F7),
                Square.G7: Pawn(Color.BLACK, Square.G7),
                Square.H7: Pawn(Color.BLACK, Square.H7),
                Square.A8: Rook(Color.BLACK, Square.A8),
                Square.B8: Knight(Color.BLACK, Square.B8),
                Square.C8: Bishop(Color.BLACK, Square.C8),
                Square.D8: Queen(Color.BLACK, Square.D8),
                Square.E8: King(Color.BLACK, Square.E8),
                Square.F8: Bishop(Color.BLACK, Square.F8),
                Square.G8: Knight(Color.BLACK, Square.G8),
                Square.H8: Rook(Color.BLACK, Square.H8),
            },
            castle_rights=CastleRights.new(),
            en_passant_target=None,
        )
        return fen, board

    def case_deep_blue_kasparov_1997_game_6(self) -> _TestBoardFromFenCase:
        fen = "r1k4r/p2nb1p1/2b4p/1p1n1p2/2PP4/3Q1NB1/1P3PPP/R5K1 b - - 0 19"
        board = Board(
            ply=38,
            halfmove_clock=0,
            to_move=Color.BLACK,
            piece_map={
                Square.A1: Rook(Color.WHITE, Square.A1),
                Square.G1: King(Color.WHITE, Square.G1),
                Square.B2: Pawn(Color.WHITE, Square.B2),
                Square.F2: Pawn(Color.WHITE, Square.F2),
                Square.G2: Pawn(Color.WHITE, Square.G2),
                Square.H2: Pawn(Color.WHITE, Square.H2),
                Square.D3: Queen(Color.WHITE, Square.D3),
                Square.F3: Knight(Color.WHITE, Square.F3),
                Square.G3: Bishop(Color.WHITE, Square.G3),
                Square.C4: Pawn(Color.WHITE, Square.C4),
                Square.D4: Pawn(Color.WHITE, Square.D4),
                Square.B5: Pawn(Color.BLACK, Square.B5),
                Square.D5: Knight(Color.BLACK, Square.D5),
                Square.F5: Pawn(Color.BLACK, Square.F5),
                Square.C6: Bishop(Color.BLACK, Square.C6),
                Square.H6: Pawn(Color.BLACK, Square.H6),
                Square.A7: Pawn(Color.BLACK, Square.A7),
                Square.D7: Knight(Color.BLACK, Square.D7),
                Square.E7: Bishop(Color.BLACK, Square.E7),
                Square.G7: Pawn(Color.BLACK, Square.G7),
                Square.A8: Rook(Color.BLACK, Square.A8),
                Square.C8: King(Color.BLACK, Square.C8),
                Square.H8: Rook(Color.BLACK, Square.H8),
            },
            castle_rights=CastleRights(
                _rights={
                    Color.WHITE: {CastleSide.SHORT: False, CastleSide.LONG: False},
                    Color.BLACK: {CastleSide.SHORT: False, CastleSide.LONG: False},
                }
            ),
            en_passant_target=None,
        )
        return fen, board

    def case_carlsen_nepo_2021_game_6(self) -> _TestBoardFromFenCase:
        fen = "3k4/5RN1/4P3/5P2/7K/8/8/6q1 b - - 2 136"
        board = Board(
            ply=272,
            halfmove_clock=2,
            to_move=Color.BLACK,
            piece_map={
                Square.G1: Queen(Color.BLACK, Square.G1),
                Square.H4: King(Color.WHITE, Square.H4),
                Square.F5: Pawn(Color.WHITE, Square.F5),
                Square.E6: Pawn(Color.WHITE, Square.E6),
                Square.F7: Rook(Color.WHITE, Square.F7),
                Square.G7: Knight(Color.WHITE, Square.G7),
                Square.D8: King(Color.BLACK, Square.D8),
            },
            castle_rights=CastleRights(
                _rights={
                    Color.WHITE: {CastleSide.SHORT: False, CastleSide.LONG: False},
                    Color.BLACK: {CastleSide.SHORT: False, CastleSide.LONG: False},
                }
            ),
            en_passant_target=None,
        )
        return fen, board
