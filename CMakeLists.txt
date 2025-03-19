cmake_minimum_required(VERSION 3.10)
project(2D_Portals_Game)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find SDL2
find_package(SDL2 REQUIRED)
include_directories(${SDL2_INCLUDE_DIRS})

# Include directories
include_directories(${CMAKE_SOURCE_DIR}/include)

# Add Box2D
# Note: You may need to adjust this based on how Box2D is installed on your system
find_package(Box2D REQUIRED)
include_directories(${BOX2D_INCLUDE_DIRS})

# Source files
file(GLOB_RECURSE SOURCES "src/*.cpp")

# Create executable
add_executable(PortalsGame ${SOURCES})

# Link libraries
target_link_libraries(PortalsGame ${SDL2_LIBRARIES} ${BOX2D_LIBRARIES})

# Copy assets to build directory
file(COPY assets DESTINATION ${CMAKE_BINARY_DIR})
