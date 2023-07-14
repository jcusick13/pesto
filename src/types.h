#include <cstdint>

typedef uint64_t U64;

enum Color: int {
  WHITE, BLACK
};

constexpr U64 FileA = 0x0101010101010101ULL;
constexpr U64 FileH = FileA << 7;

constexpr U64 Rank1 = 0b11111111;
constexpr U64 Rank8 = Rank1 << (8 * 7);
