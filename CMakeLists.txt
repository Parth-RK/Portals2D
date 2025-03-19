cmake_minimum_required(VERSION 3.10)
project(2D_Portals_Game)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find SDL2 and required components
find_package(SDL2 REQUIRED)
include_directories(${SDL2_INCLUDE_DIRS})

# Find SDL2_image
find_package(SDL2_image QUIET)
if(NOT SDL2_image_FOUND)
    # Try pkg-config as fallback
    include(FindPkgConfig)
    pkg_check_modules(SDL2_IMAGE REQUIRED SDL2_image)
    include_directories(${SDL2_IMAGE_INCLUDE_DIRS})
    list(APPEND SDL2_LIBRARIES ${SDL2_IMAGE_LIBRARIES})
endif()

# Find SDL2_ttf
find_package(SDL2_ttf QUIET)
if(NOT SDL2_ttf_FOUND)
    # Try pkg-config as fallback
    include(FindPkgConfig)
    pkg_check_modules(SDL2_TTF REQUIRED SDL2_ttf)
    include_directories(${SDL2_TTF_INCLUDE_DIRS})
    list(APPEND SDL2_LIBRARIES ${SDL2_TTF_LIBRARIES})
endif()

# Include directories
include_directories(${CMAKE_SOURCE_DIR}/include)

# Add Box2D
find_package(Box2D REQUIRED)
include_directories(${BOX2D_INCLUDE_DIRS})

# Source files
file(GLOB_RECURSE SOURCES "src/*.cpp")

# Create executable
add_executable(PortalsGame ${SOURCES})

# Link libraries
target_link_libraries(PortalsGame ${SDL2_LIBRARIES} ${BOX2D_LIBRARIES})

# Copy assets to build directory if the directory exists
if(EXISTS "${CMAKE_SOURCE_DIR}/assets")
    file(COPY assets DESTINATION ${CMAKE_BINARY_DIR})
endif()
