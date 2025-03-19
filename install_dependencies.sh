#!/bin/bash

echo "Installing dependencies for 2D Portals Game..."

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check and install build essentials
if ! command_exists g++; then
    echo "Installing build essentials..."
    if command_exists apt-get; then
        sudo apt-get update
        sudo apt-get install -y build-essential
    elif command_exists pacman; then
        sudo pacman -S --noconfirm base-devel
    elif command_exists dnf; then
        sudo dnf groupinstall -y "Development Tools"
    fi
fi

# Install CMake if not present
if ! command_exists cmake; then
    echo "Installing CMake..."
    if command_exists apt-get; then
        sudo apt-get install -y cmake
    elif command_exists pacman; then
        sudo pacman -S --noconfirm cmake
    elif command_exists dnf; then
        sudo dnf install -y cmake
    fi
fi

# Install SDL2 development libraries
echo "Installing SDL2 development libraries..."
if command_exists apt-get; then
    sudo apt-get install -y libsdl2-dev libsdl2-image-dev libsdl2-ttf-dev
elif command_exists pacman; then
    sudo pacman -S --noconfirm sdl2 sdl2_image sdl2_ttf
elif command_exists dnf; then
    sudo dnf install -y SDL2-devel SDL2_image-devel SDL2_ttf-devel
fi

# Install Box2D
echo "Installing Box2D..."
if command_exists apt-get; then
    sudo apt-get install -y libbox2d-dev
elif command_exists pacman; then
    sudo pacman -S --noconfirm box2d
elif command_exists dnf; then
    sudo dnf install -y box2d-devel
else
    # Manual installation of Box2D if package manager installation fails
    echo "Installing Box2D from source..."
    git clone https://github.com/erincatto/box2d.git
    cd box2d
    mkdir build
    cd build
    cmake ..
    make -j4
    sudo make install
    cd ../..
    rm -rf box2d
fi

# Handle Box2D configuration issues
handle_box2d_config() {
    echo "Ensuring Box2D is properly configured..."
    
    # Check if Box2D config files exist in standard locations
    if [ ! -f "/usr/local/lib/cmake/box2d/box2dConfig.cmake" ] && 
       [ ! -f "/usr/lib/cmake/Box2D/Box2DConfig.cmake" ]; then
        echo "Box2D configuration files not found in standard locations."
        echo "Attempting to resolve Box2D configuration issues..."
        
        # Manual installation of Box2D with proper configuration
        echo "Installing Box2D from source with proper configuration..."
        git clone https://github.com/erincatto/box2d.git
        cd box2d
        mkdir -p build
        cd build
        cmake -DBOX2D_BUILD_TESTBED=OFF -DBOX2D_BUILD_UNIT_TESTS=OFF ..
        make -j4
        sudo make install
        cd ../..
        rm -rf box2d
        
        # Create a symlink if needed for backward compatibility
        if [ ! -d "/usr/local/lib/cmake/Box2D" ] && [ -d "/usr/local/lib/cmake/box2d" ]; then
            sudo mkdir -p /usr/local/lib/cmake/Box2D
            sudo ln -sf /usr/local/lib/cmake/box2d/box2dConfig.cmake /usr/local/lib/cmake/Box2D/Box2DConfig.cmake
        fi
    else
        echo "Box2D configuration files found."
    fi
    
    # Update the linker cache to ensure libraries are found
    sudo ldconfig
    
    # Create custom FindBox2D.cmake as a fallback solution
    create_find_box2d_cmake
}

# Function to create a custom FindBox2D.cmake file
create_find_box2d_cmake() {
    echo "Creating custom FindBox2D.cmake file as a fallback solution..."
    
    # Create cmake/modules directory if it doesn't exist
    mkdir -p cmake/modules
    
    # Create FindBox2D.cmake file
    cat > cmake/modules/FindBox2D.cmake << 'EOL'
# FindBox2D.cmake
# Custom module to find Box2D library
# This file helps CMake find Box2D even when standard configuration files are missing

# Variables that will be defined:
# BOX2D_FOUND        - System has Box2D
# BOX2D_INCLUDE_DIRS - Box2D include directories
# BOX2D_LIBRARIES    - Box2D libraries

# Look for Box2D headers in standard locations
find_path(BOX2D_INCLUDE_DIR 
    NAMES box2d/box2d.h box2d.h
    PATHS
        /usr/include
        /usr/local/include
        /opt/local/include
)

# Look for Box2D library
find_library(BOX2D_LIBRARY
    NAMES box2d Box2D
    PATHS
        /usr/lib
        /usr/local/lib
        /opt/local/lib
)

# Set BOX2D_FOUND if both include dir and library are found
include(FindPackageHandleStandardArgs)
find_package_handle_standard_args(Box2D DEFAULT_MSG BOX2D_LIBRARY BOX2D_INCLUDE_DIR)

# Set the output variables
if(BOX2D_FOUND)
    set(BOX2D_LIBRARIES ${BOX2D_LIBRARY})
    set(BOX2D_INCLUDE_DIRS ${BOX2D_INCLUDE_DIR})
    message(STATUS "Found Box2D: ${BOX2D_LIBRARIES}")
else()
    set(BOX2D_LIBRARIES "")
    set(BOX2D_INCLUDE_DIRS "")
endif()

# Hide these variables in GUI
mark_as_advanced(BOX2D_INCLUDE_DIR BOX2D_LIBRARY)
EOL

    echo "Custom FindBox2D.cmake created in cmake/modules directory"
    echo "Add the following to your CMakeLists.txt file before find_package(Box2D):"
    echo "set(CMAKE_MODULE_PATH \${CMAKE_MODULE_PATH} \${CMAKE_CURRENT_SOURCE_DIR}/cmake/modules)"
}

# Run the Box2D configuration handler
handle_box2d_config

# Optional: Install Dear ImGui (commented out by default)
# echo "Installing Dear ImGui..."
# git clone https://github.com/ocornut/imgui.git
# cp -r imgui/backends/* include/
# cp imgui/*.h include/
# cp imgui/*.cpp src/
# rm -rf imgui

# Create build directory and run CMake
echo "Setting up build environment..."
mkdir -p build
cd build
# Try with explicit Box2D path and module path if standard methods fail
cmake -DCMAKE_PREFIX_PATH="/usr/local/lib/cmake/box2d;/usr/local/lib/cmake/Box2D" -DCMAKE_MODULE_PATH="../cmake/modules" ..

echo "Dependencies installation complete!"
echo "You can now build the project using: cd build && make"
echo ""
echo "If you still encounter Box2D not found errors, try the following:"
echo "1. Delete the CMakeCache.txt file: rm build/CMakeCache.txt"
echo "2. Make sure you have the custom FindBox2D.cmake in cmake/modules directory"
echo "3. Re-run CMake with explicit paths:"
echo "   cmake -DCMAKE_PREFIX_PATH=/usr/local/lib/cmake/box2d -DCMAKE_MODULE_PATH=../cmake/modules .."
echo "4. Check if you need to add this line to your CMakeLists.txt:"
echo "   set(CMAKE_MODULE_PATH \${CMAKE_MODULE_PATH} \${CMAKE_CURRENT_SOURCE_DIR}/cmake/modules)"