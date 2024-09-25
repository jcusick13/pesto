#include <map>
#include <string>
#include <tuple>
#include <vector>

#include "collections.h"
#include "exceptions.h"
#include "fen.h"
#include "square.h"
#include "types.h"

std::vector<std::string> square_list = {
  "a1", "b1", "c1", "d1", "e1", "f1", "g1", "h1",
  "a2", "b2", "c2", "d2", "e2", "f2", "g2", "h2",
  "a3", "b3", "c3", "d3", "e3", "f3", "g3", "h3",
  "a4", "b4", "c4", "d4", "e4", "f4", "g4", "h4",
  "a5", "b5", "c5", "d5", "e5", "f5", "g5", "h5",
  "a6", "b6", "c6", "d6", "e6", "f6", "g6", "h6",
  "a7", "b7", "c7", "d7", "e7", "f7", "g7", "h7",
  "a8", "b8", "c8", "d8", "e8", "f8", "g8", "h8"
};


std::vector<std::string> splitString(std::string s, std::string delimiter) {
  std::vector<std::string> words;
  size_t idx = 0;
  std::string token;

  while ((idx = s.find(delimiter)) != std::string::npos) {
      token = s.substr(0, idx);

      words.push_back(token);
      s.erase(0, idx + delimiter.length());
  }
  words.push_back(s);
  return words;
}

bool isDigit(const std::string s) {
  return s.find_first_not_of("0123456789") == std::string::npos;
}


std::string dumpCastlingRightsToFen(CastleRights white, CastleRights black) {
  std::string fen = "";
  bool white_has_rights = false;
  bool black_has_rights = false;

  if (white.kingside) { fen = fen + "K"; white_has_rights = true; }
  if (white.queenside) { fen = fen + "Q"; white_has_rights = true; }

  if (black.kingside) { fen = fen + "k"; black_has_rights = true; }
  if (black.queenside) { fen = fen + "q"; black_has_rights = true; }

  if (!white_has_rights & !black_has_rights) { return "-";}
  return fen;
}


std::string dumpEnPassantTargetToFen(Square square){
  if (square == nullsq) { return "-"; }
  return square_list[square];
}


std::string dumpPiecesToFen(Pieces& pieces){
  std::string board_str;

  for (int rank_idx = 7; rank_idx >= 0; rank_idx--) {
    std::string rank_str = ""; 
    int empty_squares = 0;

    for (int file_idx = 0; file_idx < 8; file_idx++) {
      int square_idx = (rank_idx * 8) + file_idx;
      std::string symbol = "";

      while (true) {
        U64 square_bb = 1ULL << square_idx;
        if (pieces.get(PAWN)->at(WHITE) & square_bb) { symbol = "P"; break; }
        if (pieces.get(PAWN)->at(BLACK) & square_bb) { symbol = "p"; break; }

        if (pieces.get(KNIGHT)->at(WHITE) & square_bb) { symbol = "N"; break; }
        if (pieces.get(KNIGHT)->at(BLACK) & square_bb) { symbol = "n"; break; }

        if (pieces.get(BISHOP)->at(WHITE) & square_bb) { symbol = "B"; break; }
        if (pieces.get(BISHOP)->at(BLACK) & square_bb) { symbol = "b"; break; }

        if (pieces.get(ROOK)->at(WHITE) & square_bb) { symbol = "R"; break; }
        if (pieces.get(ROOK)->at(BLACK) & square_bb) { symbol = "r"; break; }

        if (pieces.get(QUEEN)->at(WHITE) & square_bb) { symbol = "Q"; break; }
        if (pieces.get(QUEEN)->at(BLACK) & square_bb) { symbol = "q"; break; }

        if (pieces.get(KING)->at(WHITE) & square_bb) { symbol = "K"; break; }
        if (pieces.get(KING)->at(BLACK) & square_bb) { symbol = "k"; break; }

        break;
      }

      if (symbol == "") {
        empty_squares ++;
        continue;
      }

      if (empty_squares > 0) {
        // Add the count of previous empty squares now
        // that we've found a non-empty square
        symbol = std::to_string(empty_squares) + symbol;
        empty_squares = 0;
      }

      rank_str = rank_str + symbol;
    }
    
    // Ensure ranks ending in empty squares (or entirely
    // empty ranks) have their empty square count added
    if (empty_squares > 0) {
      rank_str = rank_str + std::to_string(empty_squares);
    }

    if (rank_idx != 0) {
      rank_str = rank_str + "/";
    }

    board_str = board_str + rank_str;
  }

  return board_str;
}


std::tuple<CastleRights, CastleRights> parseFenCastlingRights(std::string fen) {
  CastleRights white(false, false);
  CastleRights black(false, false);

  for(char &c : fen) {
    if (c == 'K') { white.kingside = true; }
    else if (c == 'Q') { white.queenside = true; }
    else if (c == 'k') { black.kingside = true; }
    else if (c == 'q') { black.queenside = true; }
  }

  return {white, black};
}

Square parseFenEnPassantTarget(std::string fen) {
  if (fen == "-") { return nullsq; }

  // Only need to check squares in 3rd/6th rank
  for (int i = 16; i < 24; i++) {
    if (fen == square_list[i]) { return Square(i); }
  }
  for (int i = 40; i < 48; i++) {
    if (fen == square_list[i]) { return Square(i); }
  }

  throw InvalidSquareException();
}

Pieces parseFenPieces(std::string fen) {
  std::vector<std::string> rank_strs = splitString(fen, "/");
  std::reverse(rank_strs.begin(), rank_strs.end());
  Pieces pieces;

  std::map<char, U64*> piece_map = {
    {'P', &pieces.get(PAWN)->at(WHITE)},
    {'N', &pieces.get(KNIGHT)->at(WHITE)},
    {'B', &pieces.get(BISHOP)->at(WHITE)},
    {'R', &pieces.get(ROOK)->at(WHITE)},
    {'Q', &pieces.get(QUEEN)->at(WHITE)},
    {'K', &pieces.get(KING)->at(WHITE)},
    {'p', &pieces.get(PAWN)->at(BLACK)},
    {'n', &pieces.get(KNIGHT)->at(BLACK)},
    {'b', &pieces.get(BISHOP)->at(BLACK)},
    {'r', &pieces.get(ROOK)->at(BLACK)},
    {'q', &pieces.get(QUEEN)->at(BLACK)},
    {'k', &pieces.get(KING)->at(BLACK)}
  };

  int rank_idx = 0;
  for (auto rank_str : rank_strs) {
    int file_idx = 0;
    for (char c : rank_str) {
      if (isDigit(std::string(1, c))) { 
        int empty_squares = std::stoi(std::string(1, c));
        file_idx += empty_squares;
        continue;
      }
      U64 *bb = piece_map[c];
      *bb |= 1ULL << ((8 * rank_idx) + file_idx);
      file_idx++;
    }
    rank_idx++;
  }

  return pieces;
}

