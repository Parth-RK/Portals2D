#include "Slider.h"
#include "../utils/Logger.h"
#include <SDL2/SDL2_gfxPrimitives.h>
#include <sstream>
#include <iomanip>

Slider::Slider(int x, int y, int width, int height, float minValue, float maxValue, float currentValue) :
    x(x),
    y(y),
    width(width),
    height(height),
    minValue(minValue),
    maxValue(maxValue),
    currentValue(currentValue),
    hovered(false),
    dragging(false),
    label(""),
    showValue(true) {
    
    // Set default colors
    backgroundColor = {60, 60, 80, 255};  // Dark blue/gray
    fillColor = {100, 100, 240, 255};     // Bright blue
    handleColor = {200, 200, 200, 255};   // Light gray
    textColor = {255, 255, 255, 255};     // White
    
    // Ensure current value is within range
    if (currentValue < minValue) currentValue = minValue;
    if (currentValue > maxValue) currentValue = maxValue;
    
    LOG_DEBUG("Slider created with range " + std::to_string(minValue) + " to " + std::to_string(maxValue));
}

Slider::~Slider() {
    LOG_DEBUG("Slider destroyed");
}

void Slider::update(float deltaTime) {
    // Any continuous animations or state changes would go here
}

void Slider::render(SDL_Renderer* renderer) {
    if (!renderer) return;
    
    // Draw background track
    boxRGBA(
        renderer,
        x, y + height / 3,
        x + width, y + 2 * height / 3,
        backgroundColor.r, backgroundColor.g, backgroundColor.b, backgroundColor.a
    );
    
    // Calculate fill width based on current value
    float fillRatio = (currentValue - minValue) / (maxValue - minValue);
    int fillWidth = static_cast<int>(width * fillRatio);
    
    // Draw filled portion
    boxRGBA(
        renderer,
        x, y + height / 3,
        x + fillWidth, y + 2 * height / 3,
        fillColor.r, fillColor.g, fillColor.b, fillColor.a
    );
    
    // Draw handle
    int handleRadius = height / 2;
    int handleX = x + fillWidth;
    int handleY = y + height / 2;
    
    filledCircleRGBA(
        renderer,
        handleX, handleY,
        handleRadius,
        handleColor.r, handleColor.g, handleColor.b, handleColor.a
    );
    
    // Draw handle border
    circleRGBA(
        renderer,
        handleX, handleY,
        handleRadius,
        textColor.r, textColor.g, textColor.b, 180
    );
    
    // Draw label and/or value if enabled
    std::string displayText = label;
    
    if (showValue) {
        std::ostringstream valueStream;
        valueStream << std::fixed << std::setprecision(1) << currentValue;
        
        if (!displayText.empty()) {
            displayText += ": ";
        }
        
        displayText += valueStream.str();
    }
    
    if (!displayText.empty()) {
        stringRGBA(
            renderer,
            x, y - 10,
            displayText.c_str(),
            textColor.r, textColor.g, textColor.b, textColor.a
        );
    }
}

bool Slider::isPointInside(int px, int py) const {
    // Check if point is within the slider area (including the handle)
    return px >= x && px <= x + width && py >= y && py <= y + height;
}

float Slider::getValueAtPosition(int px) const {
    // Calculate value based on position
    float position = static_cast<float>(px - x) / width;
    if (position < 0.0f) position = 0.0f;
    if (position > 1.0f) position = 1.0f;
    
    return minValue + position * (maxValue - minValue);
}

void Slider::setPosition(int newX, int newY) {
    x = newX;
    y = newY;
}

void Slider::setDimensions(int newWidth, int newHeight) {
    width = newWidth;
    height = newHeight;
}

void Slider::setRange(float min, float max) {
    minValue = min;
    maxValue = max;
    
    // Ensure current value is still within range
    if (currentValue < minValue) currentValue = minValue;
    if (currentValue > maxValue) currentValue = maxValue;
}

void Slider::setValue(float value) {
    // Clamp value to the valid range
    if (value < minValue) value = minValue;
    if (value > maxValue) value = maxValue;
    
    float oldValue = currentValue;
    currentValue = value;
    
    // Call callback if value changed and callback is set
    if (oldValue != currentValue && callback) {
        callback(currentValue);
    }
}

void Slider::setLabel(const std::string& text) {
    label = text;
}

void Slider::setShowValue(bool show) {
    showValue = show;
}

void Slider::setHovered(bool isHovered) {
    hovered = isHovered;
}

void Slider::setDragging(bool isDragging) {
    dragging = isDragging;
}

void Slider::setCallback(SliderCallback cb) {
    callback = cb;
}

void Slider::setBackgroundColor(SDL_Color color) {
    backgroundColor = color;
}

void Slider::setFillColor(SDL_Color color) {
    fillColor = color;
}

void Slider::setHandleColor(SDL_Color color) {
    handleColor = color;
}

void Slider::setTextColor(SDL_Color color) {
    textColor = color;
}
