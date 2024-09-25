#include <gtest/gtest.h>
#include "board.h"

TEST(BoardFromFen, DeepBlueKasparov1997Game6) {
  std::string fen = "r1k4r/p2nb1p1/2b4p/1p1n1p2/2PP4/3Q1NB1/1P3PPP/R5K1 b - - 0 19";
  Board board;
  board.fromFen(fen);

  EXPECT_EQ(board.to_move, BLACK);
  EXPECT_EQ(board.ply, 38);
  EXPECT_EQ(board.halfmove_clock, 0);
  EXPECT_EQ(board.en_passant_target, nullsq);
  EXPECT_EQ(board.castle_white, CastleRights(false, false));
  EXPECT_EQ(board.castle_black, CastleRights(false, false));

  EXPECT_EQ(board.pieces.get(ROOK)->at(WHITE), 1ULL);
  EXPECT_EQ(board.pieces.get(QUEEN)->at(WHITE), 1ULL << d3);
  EXPECT_EQ(board.pieces.get(KING)->at(BLACK), 1ULL << c8);
  EXPECT_EQ(board.pieces.get(BISHOP)->at(BLACK), (1ULL << c6 | 1ULL << e7));
}

TEST(BoardToFen, StartingPosition) {
  Board board;
  std::string obs_fen = board.toFen();
  std::string exp_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1";
  EXPECT_EQ(obs_fen, exp_fen);
}

TEST(BoardFromAndToFen, StartingPosition) {
  Board board;
  std::string start_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1";
  board.fromFen(start_fen);
  std::string end_fen = board.toFen();
  EXPECT_EQ(start_fen, end_fen);
}

