#include <gtest/gtest.h>

#include "legal.h"


TEST(SquareIsAttackedTest, NoPiecesOnBoard)
{
  Pieces pieces;
  bool attacked = squareIsAttacked(&pieces, d4, WHITE);
  EXPECT_FALSE(attacked);
}

TEST(SquareIsAttackedTest, AttackedOnce)
{
  Pieces pieces;
  pieces.get(ROOK)->at(BLACK) = 1ULL << h5;

  bool attacked = squareIsAttacked(&pieces, a5, BLACK);
  EXPECT_TRUE(attacked);
}

TEST(SquareIsAttackedTest, AttackedOncePawn)
{
  Pieces pieces;
  pieces.get(PAWN)->at(WHITE) = 1ULL << g6;

  bool attacked = squareIsAttacked(&pieces, h7, WHITE);
  EXPECT_TRUE(attacked);
}

TEST(SquareIsAttackedTest, AttackedOnceByWrongColor)
{
  Pieces pieces;
  pieces.get(ROOK)->at(WHITE) = 1ULL << c1;

  bool attacked = squareIsAttacked(&pieces, c6, BLACK);
  EXPECT_FALSE(attacked);
}

TEST(SquareIsAttackedTest, AttackedMultipleTimes)
{
  Pieces pieces;
  pieces.get(BISHOP)->at(WHITE) = 1ULL << h4;
  pieces.get(ROOK)->at(WHITE) = 1ULL << f6;

  bool attacked = squareIsAttacked(&pieces, f2, WHITE);
  EXPECT_TRUE(attacked);
}

TEST(SquareIsAttackedTest, AttackerIsBlockedByPiece)
{
  Pieces pieces;
  pieces.get(PAWN)->at(BLACK) = 1ULL << d7;
  pieces.get(ROOK)->at(WHITE) = 1ULL << d3;

  bool attacked = squareIsAttacked(&pieces, d8, WHITE);
  EXPECT_FALSE(attacked);
}
