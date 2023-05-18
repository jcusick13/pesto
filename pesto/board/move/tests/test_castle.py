from pytest_cases import parametrize_with_cases

from pesto.board.move.castle import CastleRights, generate_castling_moves
from pesto.board.move.tests.test_castle_cases import TestGenerateCastlingMovesCases
from pesto.board.square import Square
from pesto.board.piece import CastlingMove, Piece
from pesto.core.enums import Color


@parametrize_with_cases(
    ("piece_map", "castle_rights", "to_move", "exp_moves"),
    TestGenerateCastlingMovesCases,
)
def test_generate_castling_moves(
    piece_map: dict[Square, Piece],
    castle_rights: CastleRights,
    to_move: Color,
    exp_moves: set[CastlingMove],
):
    obs_moves = generate_castling_moves(
        piece_map=piece_map, castle_rights=castle_rights, to_move=to_move
    )
    assert sorted(obs_moves) == sorted(exp_moves)
