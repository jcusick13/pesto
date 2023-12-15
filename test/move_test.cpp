#include <vector>

#include <gmock/gmock.h>
#include <gtest/gtest.h>

#include "move.h"


TEST(AddPawnMovesTest, SinglePawnWithoutPromotion)
{
  std::vector<Move> obs_moves;
  U64 pawns = 1ULL << b2;
  U64 occupied = 1ULL << b2;
  Color color = WHITE;
  U64 same_color = 1ULL << b2;
  Square ep = nullsq;

  addPawnMoves(&obs_moves, pawns, occupied, color, same_color, ep);
  ASSERT_THAT(obs_moves, ::testing::ElementsAre(Move{b2, b3}, Move{b2, b4}));
}

TEST(AddPawnMovesTest, TwoPawnsWithoutPromotion)
{
  std::vector<Move> obs_moves;
  U64 pawns = 1ULL << b2 | 1ULL << c5;
  U64 occupied = 1ULL << b2 | 1ULL << c5;
  Color color = WHITE;
  U64 same_color = 1ULL << b2 | 1ULL << c5;
  Square ep = nullsq;

  addPawnMoves(&obs_moves, pawns, occupied, color, same_color, ep);
  ASSERT_THAT(
    obs_moves,
    ::testing::ElementsAre(Move{b2, b3}, Move{b2, b4}, Move{c5, c6})
  );
}

TEST(AddPawnMovesTest, SinglePawnPromotes)
{
  std::vector<Move> obs_moves;
  U64 pawns = 1ULL << d7;
  U64 occupied = 1ULL << d7;
  Color color = WHITE;
  U64 same_color = 1ULL << d7;
  Square ep = nullsq;

  addPawnMoves(&obs_moves, pawns, occupied, color, same_color, ep);
  ASSERT_THAT(
    obs_moves,
    ::testing::ElementsAre(
      Move{d7, d8, KNIGHT}, Move{d7, d8, BISHOP}, Move{d7, d8, ROOK},
      Move{d7, d8, QUEEN}
    )
  );
}


TEST(AddPieceTypeMovesTest, SingleBishop)
{
  std::vector<Move> obs_moves;
  PieceType piece_type = BISHOP;
  U64 bishops = 1ULL << b2;
  U64 occupied = 0x50200ULL;
  U64 same_color = 0x40200ULL;

  addPieceTypeMoves(piece_type, &obs_moves, bishops, occupied, same_color);
  ASSERT_THAT(
    obs_moves, 
    ::testing::ElementsAre(Move{b2, a1}, Move{b2, c1}, Move{b2, a3})
  );
}

TEST(AddPieceTypeMovesTest, TwoRooksTrappedBySameColor)
{
  std::vector<Move> obs_moves;
  PieceType piece_type = ROOK;
  U64 rooks = 0x3ULL;
  U64 occupied = 0x707ULL;
  U64 same_color = 0x707ULL;
  
  addPieceTypeMoves(piece_type, &obs_moves, rooks, occupied, same_color);
  EXPECT_TRUE(obs_moves.empty());
}

TEST(AddPieceTypeMovesTest, SingleRookInCorner)
{
  std::vector<Move> obs_moves;
  PieceType piece_type = ROOK;
  U64 rooks = 1ULL << h1;
  U64 occupied = 0x80a0ULL;
  U64 same_color = 1ULL << h1;

  addPieceTypeMoves(piece_type, &obs_moves, rooks, occupied, same_color);
  ASSERT_THAT(
    obs_moves, 
    ::testing::ElementsAre(Move{h1, f1}, Move{h1, g1}, Move{h1, h2})
  );
}
