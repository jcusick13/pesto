from typing import Mapping, Optional

from pesto.board.enums import Square
from pesto.board.piece import Piece
from pesto.core.enums import Color


def square_is_attacked(
    square: Square,
    piece_map: Mapping[Square, Piece],
    by: Optional[Color] = None,
) -> bool:
    """Determines if `square` is attacked by any pieces on
    the board.

    square: Location to check if under attack
    piece_map: Locations of all pieces on the board
    by: When `Color` is provided, check only if that `Color`
        attacks `square`
    """
    for _, piece in piece_map.items():
        if by is not None and piece.color != by:
            continue

        attacked_squares = piece.generate_psuedo_legal_moves(piece_set=piece_map.keys())
        if square in attacked_squares:
            return True

    return False
