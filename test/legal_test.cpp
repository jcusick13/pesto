#include <gmock/gmock.h>
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


TEST(GenerateLegalMovesTest, NoLegalMoves)
{
  // King is trapped in the corner
  Pieces pieces;
  pieces.get(KING)->at(WHITE) = 1ULL << a1;
  pieces.get(ROOK)->at(BLACK) = 1ULL << h2 | 1ULL << b8;

  std::vector<Move> moves = generateLegalMoves(&pieces, WHITE);
  EXPECT_TRUE(moves.size() == 0);
}


TEST(GenerateLegalMovesTest, NoLegalMovesPieceIsPinned)
{
  // King is stalemated and lone piece in front of it
  // is pinned
  Pieces pieces;
  pieces.get(KING)->at(BLACK) = 1ULL << h8;
  pieces.get(KNIGHT)->at(BLACK) = 1ULL << h7;
  pieces.get(ROOK)->at(WHITE) = 1ULL << h1 | 1ULL << g1;

  std::vector<Move> moves = generateLegalMoves(&pieces, BLACK);
  EXPECT_TRUE(moves.size() == 0);
}

TEST(GenerateLegalMovesTest, SingleLegalNonKingMove)
{
  // King is trapped in the corner, though
  // one pawn is free to move
  Pieces pieces;
  pieces.get(KING)->at(WHITE) = 1ULL << a1;
  pieces.get(PAWN)->at(WHITE) = 1ULL << e4;
  pieces.get(ROOK)->at(BLACK) = 1ULL << h2 | 1ULL << b8;

  std::vector<Move> moves = generateLegalMoves(&pieces, WHITE);
  EXPECT_THAT(moves, ::testing::ElementsAre(Move{e4, e5}));
}

TEST(GenerateLegalMovesTest, SingleLegalEnPassantMove)
{
  // King is trapped in the corner and can only
  // escape with an en passant capture
  Pieces pieces;
  pieces.get(KING)->at(WHITE) = 1ULL << b4;
  pieces.get(PAWN)->at(WHITE) = 1ULL << b5;
  pieces.get(ROOK)->at(BLACK) = 1ULL << a1 | 1ULL << c1;
  pieces.get(PAWN)->at(BLACK) = 1ULL << c5;
  pieces.get(QUEEN)->at(BLACK) = 1ULL << h3;

  std::vector<Move> moves = generateLegalMoves(&pieces, WHITE, c6);
  EXPECT_THAT(moves, ::testing::ElementsAre(Move(b5, c6, NULL_PIECE, PAWN, c5)));
}

TEST(GenerateLegalMovesTest, MultipleLegalMoves)
{
  Pieces pieces;
  pieces.get(KING)->at(WHITE) = 1ULL << a8;
  pieces.get(PAWN)->at(WHITE) = 1ULL << b6;
  pieces.get(BISHOP)->at(BLACK) = 1ULL << d6;

  std::vector<Move> moves = generateLegalMoves(&pieces, WHITE);
  EXPECT_THAT(moves,
              ::testing::ElementsAre(Move{b6, b7},
                                     Move{a8, a7},
                                     Move{a8, b7}));
}

// TEST(GenerateLegalMovesTest, MultipleLegalMovesIncludesCastling)
// {
//   EXPECT_EQ(0, 1);
// }