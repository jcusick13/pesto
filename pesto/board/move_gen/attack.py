from typing import Mapping, Optional

from pesto.board.square import Square
from pesto.board.piece import Piece
from pesto.core.enums import Color


def square_is_attacked(
    piece_map: Mapping[Square, Piece],
    square: Square,
    by: Optional[Color] = None,
) -> bool:
    """Determines if `square` is attacked by any pieces on
    the board.

    piece_map: Locations of all pieces on the board
    en_passant_square: Target square that can be moved to via en passant
    square: Location to check if under attack
    by: When `Color` is provided, check only if that `Color`
        attacks `square`
    """
    for _, piece in piece_map.items():
        if by is not None and piece.color != by:
            continue

        moves = piece.generate_psuedo_legal_moves(
            # We can ignore en passant captures in this context, as
            # we're only concerned with which squares are under attack,
            # not if an additional pawn can be captured
            piece_map=piece_map,
            **{"en_passant_sq": None}
        )
        attacked_squares: set[Square] = {move.end.curr for move in moves}
        if square in attacked_squares:
            return True

    return False
