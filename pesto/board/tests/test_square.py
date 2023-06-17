import pytest

from pesto.board.square import Square, str_to_square


@pytest.mark.unit
def test_valid_square_enum():
    """Ensure on-board indicies are correctly mapped"""
    for square in Square:
        assert square.value & 0x88 == 0


@pytest.mark.unit
@pytest.mark.parametrize(
    ("string", "exp"),
    [
        ("c1", Square.C1),
        ("e4", Square.E4),
        ("h7", Square.H7),
    ],
)
def test_str_to_square(string: str, exp: Square):
    assert str_to_square(string) == exp


@pytest.mark.unit
def test_str_to_square_raises():
    with pytest.raises(ValueError):
        _ = str_to_square("e2e4")
