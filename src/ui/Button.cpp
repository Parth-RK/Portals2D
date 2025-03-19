#include "Button.h"
#include "../utils/Logger.h"
#include <SDL2/SDL2_gfxPrimitives.h>

Button::Button(int x, int y, int width, int height, const std::string& text) :
    x(x),
    y(y),
    width(width),
    height(height),
    text(text),
    hovered(false),
    pressed(false) {
    
    // Set default colors
    normalColor = {80, 80, 100, 255};     // Dark blue/gray
    hoveredColor = {100, 100, 140, 255};  // Lighter blue/gray
    pressedColor = {60, 60, 80, 255};     // Darker blue/gray
    textColor = {255, 255, 255, 255};     // White
    
    LOG_DEBUG("Button created: " + text);
}

Button::~Button() {
    LOG_DEBUG("Button destroyed: " + text);
}

void Button::update(float deltaTime) {
    // Any continuous animations or state changes would go here
}

void Button::render(SDL_Renderer* renderer) {
    if (!renderer) return;
    
    // Choose color based on state
    SDL_Color currentColor;
    
    if (pressed) {
        currentColor = pressedColor;
    } else if (hovered) {
        currentColor = hoveredColor;
    } else {
        currentColor = normalColor;
    }
    
    // Draw button background with rounded corners
    roundedBoxRGBA(
        renderer,
        x, y,
        x + width, y + height,
        5,  // Radius of rounded corners
        currentColor.r, currentColor.g, currentColor.b, currentColor.a
    );
    
    // Draw border
    roundedRectangleRGBA(
        renderer,
        x, y,
        x + width, y + height,
        5,  // Radius of rounded corners
        textColor.r, textColor.g, textColor.b, 150  // Semi-transparent
    );
    
    // Draw text centered on button
    stringRGBA(
        renderer,
        x + width / 2 - text.length() * 3, // Approximate centering
        y + height / 2 - 5,  // Approximate centering
        text.c_str(),
        textColor.r, textColor.g, textColor.b, textColor.a
    );
}

bool Button::isPointInside(int px, int py) const {
    return px >= x && px <= x + width && py >= y && py <= y + height;
}

void Button::click() {
    pressed = true;
    
    // Call callback if registered
    if (callback) {
        callback();
    }
    
    // Reset pressed state after a short delay (would be better with a timer)
    pressed = false;
    
    LOG_DEBUG("Button clicked: " + text);
}

void Button::setPosition(int newX, int newY) {
    x = newX;
    y = newY;
}

void Button::setDimensions(int newWidth, int newHeight) {
    width = newWidth;
    height = newHeight;
}

void Button::setText(const std::string& newText) {
    text = newText;
}

void Button::setHovered(bool isHovered) {
    hovered = isHovered;
}

void Button::setPressed(bool isPressed) {
    pressed = isPressed;
}

void Button::setCallback(ButtonCallback cb) {
    callback = cb;
}

void Button::setNormalColor(SDL_Color color) {
    normalColor = color;
}

void Button::setHoveredColor(SDL_Color color) {
    hoveredColor = color;
}

void Button::setPressedColor(SDL_Color color) {
    pressedColor = color;
}

void Button::setTextColor(SDL_Color color) {
    textColor = color;
}
