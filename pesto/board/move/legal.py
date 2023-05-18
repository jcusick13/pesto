from typing import Optional

from pesto.board.move.attack import square_is_attacked
from pesto.board.move.castle import CastleRights, generate_castling_moves
from pesto.board.move.apply import make_move, unmake_move
from pesto.board.square import Square
from pesto.board.piece import King, Move, Piece, SinglePieceMove

from pesto.core.enums import Color


def legal_move_generator(
    piece_map: dict[Square, Piece],
    to_move: Color,
    castle_rights: CastleRights,
    en_passant_sq: Optional[Square],
) -> set[Move]:
    """Creates a group of moves that are legal when considering the
    full scope of the board (i.e. do not leave the king in check)
    """

    # Find king of color to move
    king: King
    for piece in piece_map.values():
        if isinstance(piece, King) and piece.color == to_move:
            king = piece
            break

    single_piece_moves: set[SinglePieceMove] = set()
    for piece in piece_map.values():
        if piece.color != to_move:
            continue

        piece_is_king: bool = piece == king

        for move in piece.generate_psuedo_legal_moves(
            piece_map=piece_map, **{"en_passant_sq": en_passant_sq}
        ):
            # Temporarily make move and see if king is in check
            tmp_piece_map, tmp_move = make_move(piece_map=piece_map, move=move)

            king_square: Square
            if piece_is_king:
                king_square = tmp_move.end.curr
            else:
                king_square = king.curr

            if not square_is_attacked(piece_map=tmp_piece_map, square=king_square):
                single_piece_moves.add(move)

            _ = unmake_move(piece_map=tmp_piece_map, move=tmp_move)

    castling_moves = generate_castling_moves(
        piece_map=piece_map, castle_rights=castle_rights, to_move=to_move
    )

    return single_piece_moves | castling_moves
