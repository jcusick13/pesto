from typing import Mapping

from pesto.board.move_gen.attack import square_is_attacked
from pesto.board.move_gen.moves import Move, make_move, unmake_move
from pesto.board.square import Square
from pesto.board.piece import King, Piece

from pesto.core.enums import Color


def legal_move_generator(
    piece_map: Mapping[Square, Piece], to_move: Color
) -> list[Move]:
    """Creates a group of moves that are legal when considering the
    full scope of the board (i.e. do not leave the king in check)

    TODO:
        * castling
        * en passant
        * promotion
    """
    moves: list[Move] = []

    # Find king of color to move
    king: King
    for piece in piece_map.values():
        if isinstance(piece, King) and piece.color == to_move:
            king = piece
            break

    for piece in piece_map.values():
        if piece.color != to_move:
            continue

        piece_is_king: bool = piece == king

        for move in piece.generate_psuedo_legal_moves(piece_map=piece_map):
            # Temporarily make move and see if king is in check
            tmp_piece_map, tmp_move = make_move(piece_map=piece_map, move=move)

            king_square: Square
            if piece_is_king:
                king_square = tmp_move.end.curr
            else:
                king_square = king.curr

            if not square_is_attacked(piece_map=tmp_piece_map, square=king_square):
                moves.append(move)

            _ = unmake_move(piece_map=tmp_piece_map, move=tmp_move)

    return moves
