from typing import Optional

from pesto.board.move.castle import CastleRights, CastleSide
from pesto.board.piece import CastlingMove, King, Move, Pawn, Rook, SinglePieceMove
from pesto.board.square import Square
from pesto.core.enums import Color


def find_en_passant_target(move: Move) -> Optional[Square]:
    """Returns a square eligible to be attacked via
    en passant after the passed move has been played
    """
    if not isinstance(move.start, Pawn):
        return None

    move_dist: int = abs(move.start.curr.value - move.end.curr.value)
    if move_dist != 32:
        return None

    # Pawn moved two squares
    direction: int = 1 if move.start.color == Color.WHITE else -1
    ep_square_idx: int = move.end.curr.value - 16 * direction
    return Square(ep_square_idx)


def update_castle_rights(castle_rights: CastleRights, move: Move) -> CastleRights:
    """Returns an updated CastlingRights object based upon
    the provided move
    """
    if isinstance(move, SinglePieceMove) and not isinstance(move.start, (Rook, King)):
        return castle_rights

    if isinstance(move, SinglePieceMove) and isinstance(move.start, King):
        castle_rights.set_false(color=move.start.color, castle_side=CastleSide.SHORT)
        castle_rights.set_false(color=move.start.color, castle_side=CastleSide.LONG)
        return castle_rights

    side: CastleSide
    if isinstance(move, SinglePieceMove) and isinstance(move.start, Rook):
        if move.start.curr not in {
            Square.A1,
            Square.A8,
            Square.H1,
            Square.H8,
        }:
            return castle_rights

        if move.start.curr in {Square.A1, Square.A8}:
            side = CastleSide.LONG
        else:
            side = CastleSide.SHORT

        castle_rights.set_false(color=move.start.color, castle_side=side)
        return castle_rights

    if isinstance(move, CastlingMove):
        if move.start.curr in {Square.A1, Square.A8}:
            side = CastleSide.LONG
        else:
            side = CastleSide.SHORT

        castling_color = move.start.color
        if not castle_rights(castling_color)[side]:
            raise ValueError(f"{castling_color} has no rights to castle {side.value}")

        castle_rights(castling_color)[CastleSide.SHORT] = False
        castle_rights(castling_color)[CastleSide.LONG] = False
        return castle_rights

    return castle_rights


def update_halfmove_clock(clock: int, move: Move) -> int:
    """Determines the new value of the halfmove clock
    based on the provided move
    """
    if isinstance(move, CastlingMove):
        return clock + 1

    if isinstance(move.start, Pawn) or move.captures is not None:
        return 0

    return clock + 1
