import pytest

from pesto.board.fen import dump_castling_rights_to_fen
from pesto.board.move.castle import CastleRights, CastleSide
from pesto.core.enums import Color


@pytest.mark.parametrize(
    ("castle_rights", "fen"),
    [
        (CastleRights.new(), "KQkq"),
        (
            CastleRights(
                {
                    Color.WHITE: {CastleSide.SHORT: False, CastleSide.LONG: True},
                    Color.BLACK: {CastleSide.SHORT: True, CastleSide.LONG: True},
                }
            ),
            "Qkq",
        ),
        (
            CastleRights(
                {
                    Color.WHITE: {CastleSide.SHORT: True, CastleSide.LONG: False},
                    Color.BLACK: {CastleSide.SHORT: True, CastleSide.LONG: True},
                }
            ),
            "Kkq",
        ),
        (
            CastleRights(
                {
                    Color.WHITE: {CastleSide.SHORT: False, CastleSide.LONG: False},
                    Color.BLACK: {CastleSide.SHORT: True, CastleSide.LONG: True},
                }
            ),
            "kq",
        ),
        (
            CastleRights(
                {
                    Color.WHITE: {CastleSide.SHORT: False, CastleSide.LONG: False},
                    Color.BLACK: {CastleSide.SHORT: False, CastleSide.LONG: False},
                }
            ),
            "-",
        ),
    ],
)
def test_dump_castling_rights_to_fen(castle_rights: CastleRights, fen: str):
    assert dump_castling_rights_to_fen(castle_rights) == fen
