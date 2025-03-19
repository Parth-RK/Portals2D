#!/bin/bash

# filepath: c:\Users\JOHN\Desktop\PRK\Portals2D\setup.sh

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

echo "Starting setup for Portals2D project..."

# Update the system
echo "Updating system..."
sudo apt update && sudo apt upgrade -y

# Install Git
if command_exists git; then
    echo "Git is already installed."
else
    echo "Installing Git..."
    sudo apt install -y git
fi

# Install build-essential
if dpkg -s build-essential >/dev/null 2>&1; then
    echo "Build-essential is already installed."
else
    echo "Installing build-essential..."
    sudo apt install -y build-essential
fi

# Install CMake
if command_exists cmake; then
    echo "CMake is already installed."
else
    echo "Installing CMake..."
    sudo apt install -y cmake
fi

# Install SDL2 and related libraries
if dpkg -s libsdl2-dev >/dev/null 2>&1 && dpkg -s libsdl2-image-dev >/dev/null 2>&1 && dpkg -s libsdl2-ttf-dev >/dev/null 2>&1; then
    echo "SDL2 and related libraries are already installed."
else
    echo "Installing SDL2 and related libraries..."
    sudo apt install -y libsdl2-dev libsdl2-image-dev libsdl2-ttf-dev
fi

# Install Box2D
if dpkg -s libbox2d-dev >/dev/null 2>&1; then
    echo "Box2D is already installed."
else
    echo "Installing Box2D..."
    sudo apt install -y libbox2d-dev
fi

# Clone the project repository
if [ -d "Portals2D" ]; then
    echo "Portals2D repository already exists."
else
    echo "Cloning Portals2D repository..."
    git clone https://github.com/Parth-RK/Portals2D.git
    cd Portals2D || exit
fi

# Run dependency installation script if it exists
if [ -f "install_dependencies.sh" ]; then
    echo "Running dependency installation script..."
    chmod +x install_dependencies.sh
    ./install_dependencies.sh
else
    echo "No dependency installation script found. Skipping..."
fi

# Configure the project with CMake
if [ ! -d "build" ]; then
    echo "Creating build directory and configuring the project..."
    mkdir build
    cd build || exit
    cmake ..
else
    echo "Build directory already exists. Skipping configuration..."
    cd build || exit
fi

# Build the project
echo "Building the project..."
make -j$(nproc)

# Run the game
if [ -f "./PortalsGame" ]; then
    echo "Running the game..."
    ./PortalsGame
else
    echo "Game executable not found. Build might have failed."
fi

echo "Setup complete!"