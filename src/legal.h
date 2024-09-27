#ifndef _LEGAL_H_
#define _LEGAL_H_

#include "collections.h"
#include "square.h"
#include "piece.h"
#include "types.h"

bool squareIsAttacked(Pieces *pieces, Square square, Color by);

#endif  // _LEGAL_H_
