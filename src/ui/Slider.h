#pragma once

#include <SDL2/SDL.h>
#include <string>
#include <functional>

typedef std::function<void(float)> SliderCallback;

class Slider {
private:
    int x, y;
    int width, height;
    float minValue, maxValue;
    float currentValue;
    
    bool hovered;
    bool dragging;
    
    // Label and value display
    std::string label;
    bool showValue;
    
    // Callbacks
    SliderCallback callback;
    
    // Styling
    SDL_Color backgroundColor;
    SDL_Color fillColor;
    SDL_Color handleColor;
    SDL_Color textColor;
    
public:
    Slider(int x, int y, int width, int height, float minValue, float maxValue, float currentValue);
    ~Slider();
    
    void update(float deltaTime);
    void render(SDL_Renderer* renderer);
    
    // Event handling
    bool isPointInside(int px, int py) const;
    float getValueAtPosition(int px) const;
    
    // Getters and setters
    void setPosition(int x, int y);
    void setDimensions(int width, int height);
    void setRange(float min, float max);
    void setValue(float value);
    void setLabel(const std::string& text);
    void setShowValue(bool show);
    void setHovered(bool isHovered);
    void setDragging(bool isDragging);
    void setCallback(SliderCallback cb);
    
    // Style customization
    void setBackgroundColor(SDL_Color color);
    void setFillColor(SDL_Color color);
    void setHandleColor(SDL_Color color);
    void setTextColor(SDL_Color color);
    
    // State access
    bool isHovered() const { return hovered; }
    bool isDragging() const { return dragging; }
    float getValue() const { return currentValue; }
    
    int getX() const { return x; }
    int getY() const { return y; }
    int getWidth() const { return width; }
    int getHeight() const { return height; }
};
