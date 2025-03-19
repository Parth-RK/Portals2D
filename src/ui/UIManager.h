#pragma once

#include <SDL2/SDL.h>
#include <vector>
#include <memory>
#include <functional>
#include <string>

class Button;
class Slider;
class InputManager;

// Function typedefs
typedef std::function<void()> ButtonCallback;
typedef std::function<void(float)> SliderCallback;

class UIManager {
private:
    SDL_Renderer* renderer;
    InputManager* inputManager;
    
    // UI Elements
    std::vector<std::shared_ptr<Button>> buttons;
    std::vector<std::shared_ptr<Slider>> sliders;
    
    // UI State
    bool uiActive;
    bool uiHovered;
    
    // Helper methods
    void registerInputCallbacks();
    
public:
    UIManager(SDL_Renderer* sdlRenderer, InputManager* input);
    ~UIManager();
    
    void initialize();
    void update(float deltaTime);
    void render();
    
    // UI Element creation
    std::shared_ptr<Button> createButton(int x, int y, int width, int height, 
                                       const std::string& text, ButtonCallback callback);
    std::shared_ptr<Slider> createSlider(int x, int y, int width, int height, 
                                       float minValue, float maxValue, float currentValue, 
                                       SliderCallback callback);
    
    // UI State management
    void setUIActive(bool active) { uiActive = active; }
    bool isUIActive() const { return uiActive; }
    bool isUIHovered() const { return uiHovered; }
    
    // Input handling
    bool handleMouseClick(int x, int y);
    bool handleMouseMove(int x, int y);
};
