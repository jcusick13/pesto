#include <cstdint>

typedef uint64_t U64;

enum Color: int {
  WHITE, BLACK
};

constexpr U64 FileA = 0x0101010101010101ULL;
constexpr U64 FileB = FileA << 1;
constexpr U64 FileG = FileA << 6;
constexpr U64 FileH = FileA << 7;
