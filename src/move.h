#ifndef _MOVE_H_
#define _MOVE_H_

#include <vector>

#include "square.h"
#include "types.h"


struct Move{
  Square from;
  Square to;

  Move(Square from, Square to) : from(from), to(to) {};

  bool operator==(const Move &other) const {
      return from == other.from && to == other.to;
  }
};


void addPieceTypeMoves(PieceType &piece_type, std::vector<Move> *moves, 
                       U64 pieces, U64 &occupied, U64 &same_color);

#endif  // _MOVE_H_