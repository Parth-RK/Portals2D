#!/bin/bash

echo "Uninstalling dependencies for 2D Portals Game..."

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Remove SDL2 development libraries
echo "Removing SDL2 development libraries..."
if command_exists apt-get; then
    sudo apt-get remove -y libsdl2-dev libsdl2-image-dev libsdl2-ttf-dev
elif command_exists pacman; then
    sudo pacman -R --noconfirm sdl2 sdl2_image sdl2_ttf
elif command_exists dnf; then
    sudo dnf remove -y SDL2-devel SDL2_image-devel SDL2_ttf-devel
fi

# Remove Box2D
echo "Removing Box2D..."
if command_exists apt-get; then
    sudo apt-get remove -y libbox2d-dev
elif command_exists pacman; then
    sudo pacman -R --noconfirm box2d
elif command_exists dnf; then
    sudo dnf remove -y box2d-devel
fi

# Remove manually installed Box2D
echo "Removing manually installed Box2D..."
sudo rm -f /usr/local/lib/libbox2d.a
sudo rm -f /usr/local/lib/libBox2D.a
sudo rm -rf /usr/local/include/box2d
sudo rm -rf /usr/local/lib/cmake/box2d
sudo rm -rf /usr/local/lib/cmake/Box2D

# Remove symlinks created during installation
echo "Removing symlinks..."
sudo rm -rf /usr/local/lib/cmake/Box2D

# Remove custom CMake modules
echo "Removing custom CMake modules..."
rm -rf cmake/modules

# Remove build directory
echo "Removing build directory..."
rm -rf build

# Remove any leftover Box2D source code
rm -rf box2d

# Remove Dear ImGui if it was installed
if [ -d "imgui" ]; then
    echo "Removing Dear ImGui..."
    rm -rf imgui
fi

# Update the shared library cache
echo "Updating shared library cache..."
sudo ldconfig

echo "Uninstallation complete!"
echo "Note: This script does not remove CMake or build essentials as they may be used by other projects."
echo "If you wish to remove them, please do so manually using your package manager."
echo "For example: sudo apt-get remove cmake build-essential (for Debian/Ubuntu)"
