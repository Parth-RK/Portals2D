#!/bin/bash

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to install a package if not already installed
install_package() {
    if ! dpkg -s "$1" >/dev/null 2>&1; then
        echo "Installing $1..."
        sudo apt install -y "$1"
    else
        echo "$1 is already installed."
    fi
}

echo "Starting setup for Portals2D project..."

# Update the system
echo "Updating system..."
sudo apt update && sudo apt upgrade -y

# Install required packages
echo "Installing required packages..."
install_package git
install_package build-essential
if ! command_exists cmake; then
    echo "Installing CMake..."
    sudo apt install -y cmake
fi

# Install SDL2 and related libraries
echo "Installing SDL2 and related libraries..."
install_package libsdl2-dev
install_package libsdl2-image-dev
install_package libsdl2-ttf-dev
install_package libbox2d-dev

# Configure and build the project
echo "Configuring and building the project..."
mkdir -p build
cd build || exit
cmake ..
make -j$(nproc)

echo "Build complete!"
echo "To run the game, use: cd build && ./PortalsGame"