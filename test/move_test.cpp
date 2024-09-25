#include <vector>

#include <gmock/gmock.h>
#include <gtest/gtest.h>

#include "exceptions.h"
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


TEST(ApplyMoveTest, UnobstructedMove)
{
  Pieces pieces;
  pieces.initStartingPosition();
  Move move{d2, d4};

  applyMove(&pieces, move, WHITE);
  EXPECT_EQ(pieces.get(PAWN)->at(WHITE) & 1ULL << d2, 0ULL);
  EXPECT_EQ(pieces.get(PAWN)->at(WHITE) & 1ULL << d4, 1ULL << d4);
}

TEST(ApplyMoveTest, CapturingMove)
{
  Pieces pieces;
  pieces.get(PAWN)->at(WHITE) = (1ULL << d5);
  pieces.get(KNIGHT)->at(BLACK) = (1ULL << c6);
  Move move{d5, c6};

  applyMove(&pieces, move, WHITE);
  EXPECT_EQ(pieces.get(PAWN)->at(WHITE), 1ULL << c6);
  EXPECT_EQ(pieces.get(KNIGHT)->at(BLACK), 0ULL);
  EXPECT_EQ(move.captured, KNIGHT);
}

TEST(ApplyMoveTest, PromotionMove)
{
  Pieces pieces;
  pieces.get(PAWN)->at(BLACK) = (1ULL << b2);
  Move move{b2, b1, QUEEN};

  applyMove(&pieces, move, BLACK);
  EXPECT_EQ(pieces.get(PAWN)->at(BLACK), 0ULL);
  EXPECT_EQ(pieces.get(QUEEN)->at(BLACK), 1ULL << b1);
}

TEST(ApplyMoveTest, NonPawnMove)
{
  Pieces pieces;
  pieces.get(KING)->at(WHITE) = 1ULL << c6;
  Move move{c6, b6};

  applyMove(&pieces, move, WHITE);
  EXPECT_EQ(pieces.get(KING)->at(WHITE), 1ULL << b6);
}

TEST(ApplyMoveTest, NoPieceExistsToMove)
{
  Pieces pieces;
  Move move{d2, d4};
  EXPECT_THROW(applyMove(&pieces, move, WHITE), InvalidPieceException);
}


TEST(RevertMoveTest, UnobstructedMove)
{
  Pieces pieces;
  pieces.get(BISHOP)->at(BLACK) = 1ULL << f6;
  Move move{a1, f6};

  revertMove(&pieces, move, BLACK);
  EXPECT_EQ(pieces.get(BISHOP)->at(BLACK), 1ULL << a1);
}

TEST(RevertMoveTest, CapturingMove)
{
  Pieces pieces;
  pieces.get(ROOK)->at(WHITE) = 1ULL << b6;
  Move move(b1, b6, NULL_PIECE, QUEEN);

  revertMove(&pieces, move, WHITE);
  EXPECT_EQ(pieces.get(ROOK)->at(WHITE), 1ULL << b1);
  EXPECT_EQ(pieces.get(QUEEN)->at(BLACK), 1ULL << b6);
}

TEST(RevertMoveTest, PromotionMove)
{
  Pieces pieces;
  pieces.get(KNIGHT)->at(BLACK) = 1ULL << e1;
  Move move{e2, e1, KNIGHT};

  revertMove(&pieces, move, BLACK);
  EXPECT_EQ(pieces.get(KNIGHT)->at(BLACK), 0ULL);
  EXPECT_EQ(pieces.get(PAWN)->at(BLACK), 1ULL << e2);
}

TEST(RevertMoveTest, NoPieceExistsToMove)
{
  Pieces pieces;
  Move move{d2, d4};
  EXPECT_THROW(revertMove(&pieces, move, WHITE), InvalidPieceException);
}
