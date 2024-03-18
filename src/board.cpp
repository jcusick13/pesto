#include "board.h"
#include "fen.h"
#include "square.h"

/*
  Initialize board to the start of a new game
*/
Board::Board()
{
  pieces.initStartingPosition();
  to_move = WHITE;
  ply = 1;
  halfmove_clock = 0;
  en_passant_target = nullsq;
};

void Board::fromFen(std::string fen) {
  std::vector<std::string> fen_sections = splitString(fen, " ");

  pieces = parseFenPieces(fen_sections[0]);
  to_move = (fen_sections[1] == "w") ? WHITE : BLACK;
  auto [white, black] = parseFenCastlingRights(fen_sections[2]);
  castle_white = white;
  castle_black = black;
  en_passant_target = parseFenEnPassantTarget(fen_sections[3]);
  halfmove_clock = std::stoi(fen_sections[4]);
  ply = ((std::stoi(fen_sections[5]) * 2) - 1);
  if (to_move == BLACK) { ply++; }
}

std::string Board::toFen() {
  std::string piece_str = dumpPiecesToFen(pieces);
  std::string color = (to_move == WHITE) ? "w" : "b";

  std::string castling = dumpCastlingRightsToFen(castle_white, castle_black);
  std::string en_passant = dumpEnPassantTargetToFen(en_passant_target);

  std::string halfmove = std::to_string(halfmove_clock);
  int fullmove_extra = (to_move == WHITE) ? 1 : 0;
  std::string fullmove = std::to_string((ply / 2) + fullmove_extra);

  return (
    piece_str + " " + color + " " + castling + " " + 
    en_passant + " " + halfmove + " " + fullmove
  );
}

