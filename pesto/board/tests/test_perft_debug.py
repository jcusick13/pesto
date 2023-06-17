# pylint: disable=redefined-outer-name
"""
    Debugging tools for diagnosing incorrect Perft test counts

    Set the fixtures `fen` and `max_depth` in order to call and
    debug with pytest. Pass the resulting FEN board from that test
    to `print_moves_from_single_ply` in order to manually inspect
    the differences from a single position between Pesto and Stockfish.
"""
import re
from subprocess import PIPE, Popen

import pytest

from pesto.board.board import Board
from pesto.board.move.legal import legal_move_generator
from pesto.board.perft import perft

STOCKFISH = "stockfish/stockfish_15.1_linux_x64_avx2/src/stockfish"


def stockfish_node_count(fen: str) -> int:
    """Return the nodes searched from Stockfish at depth 1
    from the given starting FEN position
    """
    with Popen(
        [f"./{STOCKFISH}"], stdin=PIPE, stdout=PIPE, stderr=PIPE, encoding="ascii"
    ) as proc:
        proc_output, _ = proc.communicate(f"position fen {fen}\n go perft 1", timeout=5)

    if (regex_search := re.search("Nodes searched: ([0-9]+)", proc_output)) is not None:
        node_count = int(regex_search.group(1))
        return node_count

    return -1


def board_state_generator(board: Board, depth: int, max_depth: int):
    """Yields individual Board objects using a depth first
    traversal of legal moves
    """
    if depth >= max_depth:
        return

    for move in legal_move_generator(
        piece_map=board.piece_map,
        to_move=board.to_move,
        castle_rights=board.castle_rights,
        en_passant_sq=board.en_passant_target,
    ):
        child_board = board.apply_move(move)
        yield child_board

        one_deeper = depth + 1
        yield from board_state_generator(
            board=child_board, depth=one_deeper, max_depth=max_depth
        )


@pytest.fixture
def fen():
    return "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"


@pytest.fixture
def max_depth():
    return 2


@pytest.mark.perft
def test_debug_perft_position(fen: str, max_depth: int):
    board = Board.from_fen(fen)

    for board_state in board_state_generator(board=board, depth=0, max_depth=max_depth):
        pesto_nodes = perft(board=board_state, depth=1)[1]
        stockfish_nodes = stockfish_node_count(board_state.to_fen())

        if pesto_nodes != stockfish_nodes:
            raise ValueError(
                f"{pesto_nodes=}, {stockfish_nodes=}, FEN={board_state.to_fen()}"
            )


def print_moves_from_single_ply(fen: str):
    """Print out the list of moves for a single ply of both
    Stockfish and Pesto, given a starting position
    """
    with Popen(
        [f"./{STOCKFISH}"], stdin=PIPE, stdout=PIPE, stderr=PIPE, encoding="ascii"
    ) as proc:
        proc_output, _ = proc.communicate(f"position fen {fen}\n go perft 1", timeout=5)
    print(proc_output)

    board = Board.from_fen(fen)
    for move in legal_move_generator(
        piece_map=board.piece_map,
        to_move=board.to_move,
        castle_rights=board.castle_rights,
        en_passant_sq=board.en_passant_target,
    ):
        print(move)


if __name__ == "__main__":
    print_moves_from_single_ply(
        "r3k3/p1pNqpb1/bn2pnpr/3P4/1p2P3/5Q1p/PPPBBPPP/RN2K2R b KQq - 3 2"
    )
