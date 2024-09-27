include(FetchContent)
FetchContent_Declare(
  googletest
  URL https://github.com/google/googletest/archive/03597a01ee50ed33e9dfd640b249b4be3799d395.zip
)
FetchContent_MakeAvailable(googletest)

enable_testing()

add_executable(
  board_test
  board_test.cpp
)
target_link_libraries(
  board_test
  board
  GTest::gtest_main
)

add_executable(
  fen_test
  fen_test.cpp
)
target_link_libraries(
  fen_test
  fen 
  GTest::gtest_main
)

add_executable(
  legal_test
  legal_test.cpp
)
target_link_libraries(
  legal_test
  legal
  GTest::gtest_main
)

add_executable(
  move_test
  move_test.cpp
)
target_link_libraries(
  move_test
  move
  GTest::gtest_main
  GTest::gmock_main
)

add_executable(
  piece_test
  piece_test.cpp
)
target_link_libraries(
  piece_test
  piece 
  GTest::gtest_main
)

include(GoogleTest)
gtest_discover_tests(board_test)
gtest_discover_tests(fen_test)
gtest_discover_tests(legal_test)
gtest_discover_tests(move_test)
gtest_discover_tests(piece_test)
