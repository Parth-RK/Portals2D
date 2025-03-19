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
install_package pkg-config
if ! command_exists cmake; then
    echo "Installing CMake..."
    sudo apt install -y cmake
fi

# Install SDL2 and related libraries
echo "Installing SDL2 and related libraries..."
install_package libsdl2-dev
install_package libsdl2-image-dev
install_package libsdl2-ttf-dev

# Install Box2D - try both common package names
echo "Installing Box2D..."
if ! apt-cache search libbox2d-dev | grep -q libbox2d-dev; then
    if apt-cache search box2d | grep -q libbox2d; then
        install_package libbox2d
    else
        echo "Box2D package not found in repositories."
        echo "Attempting to build Box2D from source..."
        
        # Create a temporary directory for Box2D build
        mkdir -p /tmp/box2d_build
        cd /tmp/box2d_build
        
        # Clone Box2D repository
        git clone https://github.com/erincatto/box2d.git
        cd box2d
        
        # Build and install Box2D
        mkdir -p build
        cd build
        cmake -DBOX2D_BUILD_SHARED=ON -DBOX2D_BUILD_STATIC=ON ..
        make -j$(nproc)
        sudo make install
        
        # Return to the project directory
        cd "$OLDPWD"
    fi
else
    install_package libbox2d-dev
fi

# Configure and build the project
echo "Configuring and building the project..."
mkdir -p build
cd build || exit
cmake ..
make -j$(nproc)

echo "Build complete!"
echo "To run the game, use: cd build && ./PortalsGame"