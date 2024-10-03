#include "exceptions.h"
#include "legal.h"

#include <iostream>


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


std::vector<Move> generateLegalMoves(Pieces *pieces, Color to_move,
                                     Square en_passant) {

  std::vector<Move> legal_moves;
  std::vector<Move> potential_moves;
  std::vector<Move> potential_king_moves;

  Square king_square = getLeastSigBit(pieces->get(KING)->at(to_move));
  U64 occupied = pieces->occupied();
  U64 same_color = pieces->getColor(to_move);
  Color other_color{to_move ^ BLACK};

  // Collect piece moves with standard behavior (all but pawns and king)
  for (int ptype = KNIGHT; ptype != KING; ++ptype) {
    PieceType piece_type = PieceType(ptype);
    U64 from_bb = pieces->get(piece_type)->at(to_move);
    if (from_bb == 0) { continue; }

    addPieceTypeMoves(piece_type, &potential_moves, from_bb,
                      occupied, same_color);
  }

  // Collect pawn moves
  addPawnMoves(&potential_moves, pieces->get(PAWN)->at(to_move), occupied,
               to_move, same_color, en_passant);

  bool legal;
  for (Move &move : potential_moves) {
    legal = true;
    applyMove(pieces, move, to_move);
    if (squareIsAttacked(pieces, king_square, other_color)) { legal = false; }
    revertMove(pieces, move, to_move);

    if (legal) { legal_moves.push_back(move); }
  }

  // Collect and check king moves
  PieceType king = KING;
  addPieceTypeMoves(king, &potential_king_moves, pieces->get(KING)->at(to_move),
                    occupied, same_color);
  for (Move &move : potential_king_moves) {
    legal = true;
    applyMove(pieces, move, to_move);
    if (squareIsAttacked(pieces, move.to, other_color)) { legal = false; }
    revertMove(pieces, move, to_move);

    if (legal) { legal_moves.push_back(move); }
  }

  return legal_moves;
}