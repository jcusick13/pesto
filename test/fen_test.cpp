#include <string>

#include <gtest/gtest.h>

#include "fen.h"

TEST(DumpCastlingRightsToFenTest, AllRightsAvailable) {
  CastleRights white;
  CastleRights black;

  std::string exp_fen = "KQkq";
  std::string obs_fen = dumpCastlingRightsToFen(white, black);
  EXPECT_EQ(obs_fen, exp_fen);
}

TEST(DumpCastlingRightsToFenTest, PartialRightsAvailable) {
  CastleRights white(false, true);
  CastleRights black(true, false);

  std::string exp_fen = "Qk";
  std::string obs_fen = dumpCastlingRightsToFen(white, black);
  EXPECT_EQ(obs_fen, exp_fen);
}

TEST(DumpCastlingRightsToFenTest, NoRightsAvailable) {
  CastleRights white(false, false);
  CastleRights black(false, false);

  std::string exp_fen = "-";
  std::string obs_fen = dumpCastlingRightsToFen(white, black);
  EXPECT_EQ(obs_fen, exp_fen);
}

TEST(DumpEnPassantTargetToFenTest, EnPassantSquarePresent) {
  Square ep_square = c3;
  std::string exp_fen = "c3";
  std::string obs_fen = dumpEnPassantTargetToFen(ep_square);
  EXPECT_EQ(obs_fen, exp_fen);
}

TEST(DumpEnPassantTargetToFenTest, NoEnPassantSquarePresent) {
  Square ep_square = nullsq;
  std::string exp_fen = "-";
  std::string obs_fen = dumpEnPassantTargetToFen(ep_square);
  EXPECT_EQ(obs_fen, exp_fen);
}

TEST(DumpPiecesToFenTest, StartingGamePosition) {
  Pieces pieces;
  pieces.initStartingPosition();

  std::string obs_fen = dumpPiecesToFen(pieces);
  std::string exp_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR";
  EXPECT_EQ(obs_fen, exp_fen);
}

TEST(ParseFenCastlingRightsTest, AllRightsAvailable) {
  std::string fen = "KQkq";
  CastleRights exp_white(true, true);
  CastleRights exp_black(true, true);
  
  auto [obs_white, obs_black] = parseFenCastlingRights(fen);
  EXPECT_EQ(obs_white, exp_white);
  EXPECT_EQ(obs_black, exp_black);
}

TEST(ParseFenCastlingRightsTest, PartialRightsAvailable) {
  std::string fen = "Qq";
  CastleRights exp_white(false, true);
  CastleRights exp_black(false, true);

  auto [obs_white, obs_black] = parseFenCastlingRights(fen);
  EXPECT_EQ(obs_white, exp_white);
  EXPECT_EQ(obs_black, exp_black);
}

TEST(ParseFenCastlingRightsTest, NoRightsAvailable) {
  std::string fen = "-";
  CastleRights exp_white(false, false);
  CastleRights exp_black(false, false);

  auto [obs_white, obs_black] = parseFenCastlingRights(fen);
  EXPECT_EQ(obs_white, exp_white);
  EXPECT_EQ(obs_black, exp_black);
}

TEST(ParseFenEnPassantTargetTest, NoTargetSquare) {
  std::string fen = "-";
  Square exp_sq = nullsq;
  Square obs_sq = parseFenEnPassantTarget(fen);
  EXPECT_EQ(obs_sq, exp_sq);
}

TEST(ParseFenEnPassantTargetTest, TargetSquareAvailableWhite) {
  std::string fen = "c3";
  Square exp_sq = c3;
  Square obs_sq = parseFenEnPassantTarget(fen);
  EXPECT_EQ(obs_sq, exp_sq);
}

TEST(ParseFenEnPassantTargetTest, TargetSquareAvailableBlack) {
  std::string fen = "h6";
  Square exp_sq = h6;
  Square obs_sq = parseFenEnPassantTarget(fen);
  EXPECT_EQ(obs_sq, exp_sq);
}

