#ifndef _MOVE_H_
#define _MOVE_H_

#include <vector>

#include "square.h"
#include "types.h"


struct Move{
  Square from;
  Square to;
  PieceType promotion;

  Move(Square from, Square to) : from(from), to(to) { promotion = NULL_PIECE; };
  Move(Square from, Square to, PieceType promotion) : from(from), to(to),
    promotion(promotion) {};

  bool operator==(const Move &other) const {
      return from == other.from && to == other.to;
  }
};


void addPawnMoves(std::vector<Move> *moves, U64 pawns, U64 &occupied,
                  Color color, U64 &same_color, Square en_passant);
void addPieceTypeMoves(PieceType &piece_type, std::vector<Move> *moves, 
                       U64 pieces, U64 &occupied, U64 &same_color);

#endif  // _MOVE_H_

