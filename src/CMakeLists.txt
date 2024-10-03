add_library(
    board 
    board.cpp
    collections.cpp
    fen.cpp
)
target_include_directories(
    board PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}
)

add_library(
    fen
    fen.cpp
    collections.cpp
)
target_include_directories(
    fen PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}
)

add_library(
    legal
    legal.cpp
    collections.cpp
    move.cpp
    piece.cpp
)
target_include_directories(
    legal PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}
)

add_library(
    move 
    move.cpp
    collections.cpp
    piece.cpp
)
target_include_directories(
    move PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}
)

add_library(
    piece 
    piece.cpp
)
target_include_directories(
    piece PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}
)
