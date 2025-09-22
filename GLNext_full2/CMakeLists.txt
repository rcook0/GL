cmake_minimum_required(VERSION 3.15)
project(GLNext LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

option(BUILD_TESTS "Build unit tests" ON)

find_package(Vulkan REQUIRED)
find_package(glfw3 REQUIRED)

add_subdirectory(src)
if(BUILD_TESTS)
  enable_testing()
  add_subdirectory(tests)
endif()
