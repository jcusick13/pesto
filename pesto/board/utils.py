def index_on_board(idx: int) -> bool:
    """Determines if the index of a given square resides
    within the board, based on the 16x8 0x88 board logic"""
    return idx & 0x88 == 0
