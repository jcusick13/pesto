import pytest

from pesto.board.board import Board
from pesto.board.perft import perft


@pytest.mark.perft
def test_perft_starting_position():
    fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    node_count = perft(board=Board.from_fen(fen), depth=4)
    expected = {1: 20, 2: 400, 3: 8_902, 4: 197_281}
    assert node_count == expected


@pytest.mark.perft
def test_perft_position_3():
    fen = "8/2p5/3p4/KP5r/1R3p1k/8/4P1P1/8 w - - 0 1"
    node_count = perft(board=Board.from_fen(fen), depth=4)
    expected = {1: 14, 2: 191, 3: 2_812, 4: 43_238}
    assert node_count == expected


@pytest.mark.perft
def test_perft_position_4():
    fen = "r3k2r/Pppp1ppp/1b3nbN/nP6/BBP1P3/q4N2/Pp1P2PP/R2Q1RK1 w kq - 0 1"
    node_count = perft(board=Board.from_fen(fen), depth=3)
    expected = {1: 6, 2: 264, 3: 9_467}
    assert node_count == expected


@pytest.mark.perft
def test_perft_position_5():
    fen = "rnbq1k1r/pp1Pbppp/2p5/8/2B5/8/PPP1NnPP/RNBQK2R w KQ - 1 8"
    node_count = perft(board=Board.from_fen(fen), depth=3)
    expected = {1: 44, 2: 1_486, 3: 62_379}
    assert node_count == expected
