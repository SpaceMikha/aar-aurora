cmake_minimum_required(VERSION 3.16)
project(AARCoordinator)

set(CMAKE_CXX_STANDARD 17)

add_executable(aar-coordinator
    src/main.cpp
)

if(WIN32)
    target_link_libraries(aar-coordinator ws2_32)
endif()
