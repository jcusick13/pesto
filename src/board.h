#include <cstdint>
#include <vector>

#include "square.h"
#include "types.h"

using namespace std;

class Board {
  public:
    Board();

    vector<U64> pawns   = vector<U64>(2);
    vector<U64> knights = vector<U64>(2);
    vector<U64> bishops = vector<U64>(2);
    vector<U64> rooks   = vector<U64>(2);
    vector<U64> queens  = vector<U64>(2);
    vector<U64> kings   = vector<U64>(2);

};

Square popLeastSigBit(U64 &piece_bb);
