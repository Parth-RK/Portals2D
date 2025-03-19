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
cmake ..

echo "Dependencies installation complete!"
echo "You can now build the project using: cd build && make"