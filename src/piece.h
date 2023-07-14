#include "square.h"
#include "types.h"

Square popLeastSigBit(U64 &piece_bb);

U64 northOne    (U64 &piece_bb);
U64 southOne    (U64 &piece_bb);
U64 eastOne     (U64 &piece_bb);
U64 westOne     (U64 &piece_bb);
U64 northEastOne(U64 &piece_bb);
U64 southEastOne(U64 &piece_bb);
U64 southWestOne(U64 &piece_bb);
U64 northWestOne(U64 &piece_bb);

U64 getKingAttacks(U64 &king_bb);
