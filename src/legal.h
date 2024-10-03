#ifndef _LEGAL_H_
#define _LEGAL_H_

#include <vector>

#include "collections.h"
#include "move.h"
#include "square.h"
#include "piece.h"
#include "types.h"

bool squareIsAttacked(Pieces *pieces, Square square, Color by);

std::vector<Move> generateLegalMoves(Pieces *pieces, Color to_move,
                                     Square en_passant = nullsq);

#endif  // _LEGAL_H_
