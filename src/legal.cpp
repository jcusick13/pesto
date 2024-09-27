#include "legal.h"


bool squareIsAttacked(Pieces *pieces, Square square, Color by) {
  U64 occupied = pieces->occupied();
  U64 same_color = pieces->getColor(by);

  bool promotion = false;
  U64 pawn = getPawnAttacks(pieces->get(PAWN)->at(by), occupied, same_color, by,
                            promotion, true);
  U64 knight = getPieceAttacks(KNIGHT, pieces->get(KNIGHT)->at(by),
                               occupied, same_color);
  U64 bishop = getPieceAttacks(BISHOP, pieces->get(BISHOP)->at(by),
                               occupied, same_color);
  U64 rook = getPieceAttacks(ROOK, pieces->get(ROOK)->at(by),
                               occupied, same_color);
  U64 queen = getPieceAttacks(QUEEN, pieces->get(QUEEN)->at(by),
                               occupied, same_color);
  U64 king = getPieceAttacks(KING, pieces->get(KING)->at(by),
                               occupied, same_color);

  U64 attacked = pawn | knight | bishop | rook | queen | king;
  return ((1ULL << square) & attacked) != 0ULL;
}