from pesto.board.enums import Square


def test_valid_square_enum():
    """Ensure on-board indicies are correctly mapped"""
    for square in Square:
        assert square.value & 0x88 == 0
