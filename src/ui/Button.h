#pragma once

#include <SDL2/SDL.h>
#include <string>
#include <functional>

typedef std::function<void()> ButtonCallback;

class Button {
private:
    int x, y;
    int width, height;
    std::string text;
    bool hovered;
    bool pressed;
    
    // Callbacks
    ButtonCallback callback;
    
    // Styling
    SDL_Color normalColor;
    SDL_Color hoveredColor;
    SDL_Color pressedColor;
    SDL_Color textColor;
    
public:
    Button(int x, int y, int width, int height, const std::string& text);
    ~Button();
    
    void update(float deltaTime);
    void render(SDL_Renderer* renderer);
    
    // Event handling
    bool isPointInside(int px, int py) const;
    void click();
    
    // Getters and setters
    void setPosition(int x, int y);
    void setDimensions(int width, int height);
    void setText(const std::string& text);
    void setHovered(bool isHovered);
    void setPressed(bool isPressed);
    void setCallback(ButtonCallback cb);
    
    // Style customization
    void setNormalColor(SDL_Color color);
    void setHoveredColor(SDL_Color color);
    void setPressedColor(SDL_Color color);
    void setTextColor(SDL_Color color);
    
    // State access
    bool isHovered() const { return hovered; }
    bool isPressed() const { return pressed; }
    
    int getX() const { return x; }
    int getY() const { return y; }
    int getWidth() const { return width; }
    int getHeight() const { return height; }
    const std::string& getText() const { return text; }
};
