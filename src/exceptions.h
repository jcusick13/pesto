#ifndef _EXCEPTIONS_H_
#define _EXCEPTIONS_H_

#include <exception>

class EmptyBitboardException : public std::exception{};

class InvalidPieceException : public std::exception{};

class InvalidSquareException : public std::exception{};

#endif  // _EXCEPTIONS_H_

