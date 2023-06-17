from collections import Counter

from pesto.board.board import Board
from pesto.board.move.legal import legal_move_generator


def perft(board: Board, depth: int) -> Counter[int]:
    """Counts distinct moves (nodes) at each level
    down the tree starting from the passed `board`,
    going `depth` levels.

    Returns a counter shaped like `{depth: node_count}`
    """
    return get_node_count(
        start_board=board, curr_depth=0, max_depth=depth, visited=set()
    )


def get_node_count(
    start_board: Board, curr_depth: int, max_depth: int, visited: set[Board]
) -> Counter[int]:
    """Depth first traversal of positions that occur"""
    node_count = Counter({curr_depth + 1: 0})

    if curr_depth >= max_depth:
        return node_count

    if start_board not in visited:
        visited.add(start_board)

        for move in legal_move_generator(
            piece_map=start_board.piece_map,
            to_move=start_board.to_move,
            castle_rights=start_board.castle_rights,
            en_passant_sq=start_board.en_passant_target,
        ):
            child_board = start_board.apply_move(move)
            if child_board not in visited:
                one_deeper = curr_depth + 1
                node_count += get_node_count(
                    start_board=child_board,
                    curr_depth=one_deeper,
                    max_depth=max_depth,
                    visited=visited,
                )
                node_count[curr_depth + 1] += 1

    return node_count
