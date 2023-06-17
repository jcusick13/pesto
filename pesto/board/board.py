from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from pesto.board.board_state import (
    find_en_passant_target,
    update_castle_rights,
    update_halfmove_clock,
)
from pesto.board.fen import (
    dump_castling_rights_to_fen,
    dump_en_passant_target_to_fen,
    dump_piece_map_to_fen,
    parse_fen_castling_rights,
    parse_fen_en_passant_target,
    parse_fen_piece_map,
)
from pesto.board.move.apply import make_move
from pesto.board.move.castle import CastleRights
from pesto.board.piece import Bishop, King, Knight, Move, Pawn, Piece, Queen, Rook
from pesto.board.square import Square
from pesto.core.enums import Color


@dataclass
class Board:
    ply: int
    halfmove_clock: int
    to_move: Color
    piece_map: dict[Square, Piece]
    castle_rights: CastleRights
    en_passant_target: Optional[Square]

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Board):
            return NotImplemented
        return self.to_fen() == other.to_fen()

    def __hash__(self) -> int:
        return hash(self.to_fen())

    @classmethod
    def new(cls) -> Board:
        """Create a new board at the starting game position"""
        return Board(
            ply=1,
            halfmove_clock=0,
            to_move=Color.WHITE,
            piece_map=starting_piece_map(),
            castle_rights=CastleRights.new(),
            en_passant_target=None,
        )

    @classmethod
    def from_fen(cls, fen: str) -> Board:
        """Construct a new `Board` from a FEN string"""
        (
            pieces,
            color,
            castling,
            en_passant,
            halfmove_clock,
            fullmove_count,
        ) = fen.split()

        to_move = Color.WHITE if color == "w" else Color.BLACK
        ply = (int(fullmove_count) * 2) - 1
        if to_move == Color.BLACK:
            ply += 1

        return Board(
            ply=ply,
            halfmove_clock=int(halfmove_clock),
            to_move=to_move,
            piece_map=parse_fen_piece_map(pieces),
            castle_rights=parse_fen_castling_rights(castling),
            en_passant_target=parse_fen_en_passant_target(en_passant),
        )

    def to_fen(self) -> str:
        """Dumps the current board state to a FEN string"""
        pieces = dump_piece_map_to_fen(self.piece_map)
        color = "w" if self.to_move == Color.WHITE else "b"
        castling = dump_castling_rights_to_fen(self.castle_rights)
        en_passant = dump_en_passant_target_to_fen(self.en_passant_target)
        halfmove = str(self.halfmove_clock)
        _fullmove_extra = 1 if self.to_move == Color.WHITE else 0
        fullmove = str((self.ply // 2) + _fullmove_extra)

        fen_components = [pieces, color, castling, en_passant, halfmove, fullmove]
        return " ".join(fen_components)

    def apply_move(self, move: Move) -> Board:
        """Create new board state from the received move"""
        new_piece_map, played_move = make_move(piece_map=self.piece_map, move=move)

        return Board(
            ply=self.ply + 1,
            halfmove_clock=update_halfmove_clock(clock=self.halfmove_clock, move=move),
            to_move=(Color.WHITE if self.to_move == Color.BLACK else Color.BLACK),
            piece_map=new_piece_map,
            castle_rights=update_castle_rights(self.castle_rights, move=played_move),
            en_passant_target=find_en_passant_target(move=played_move),
        )


def starting_piece_map() -> dict[Square, Piece]:
    return {
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
        Square.D2: Pawn(Color.WHITE, Square.D2),
        Square.E2: Pawn(Color.WHITE, Square.E2),
        Square.F2: Pawn(Color.WHITE, Square.F2),
        Square.G2: Pawn(Color.WHITE, Square.G2),
        Square.H2: Pawn(Color.WHITE, Square.H2),
        Square.A8: Rook(Color.BLACK, Square.A8),
        Square.B8: Knight(Color.BLACK, Square.B8),
        Square.C8: Bishop(Color.BLACK, Square.C8),
        Square.D8: Queen(Color.BLACK, Square.D8),
        Square.E8: King(Color.BLACK, Square.E8),
        Square.F8: Bishop(Color.BLACK, Square.F8),
        Square.G8: Knight(Color.BLACK, Square.G8),
        Square.H8: Rook(Color.BLACK, Square.H8),
        Square.A7: Pawn(Color.BLACK, Square.A7),
        Square.B7: Pawn(Color.BLACK, Square.B7),
        Square.C7: Pawn(Color.BLACK, Square.C7),
        Square.D7: Pawn(Color.BLACK, Square.D7),
        Square.E7: Pawn(Color.BLACK, Square.E7),
        Square.F7: Pawn(Color.BLACK, Square.F7),
        Square.G7: Pawn(Color.BLACK, Square.G7),
        Square.H7: Pawn(Color.BLACK, Square.H7),
    }
