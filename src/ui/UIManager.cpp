#include "UIManager.h"
#include "Button.h"
#include "Slider.h"
#include "../core/InputManager.h"
#include "../utils/Logger.h"

UIManager::UIManager(SDL_Renderer* sdlRenderer, InputManager* input) :
    renderer(sdlRenderer),
    inputManager(input),
    uiActive(true),
    uiHovered(false) {
    
    LOG_DEBUG("UI Manager created");
}

UIManager::~UIManager() {
    // Clear UI elements
    buttons.clear();
    sliders.clear();
    
    LOG_DEBUG("UI Manager destroyed");
}

void UIManager::initialize() {
    // Register input callbacks
    registerInputCallbacks();
    
    LOG_INFO("UI Manager initialized");
}

void UIManager::registerInputCallbacks() {
    if (!inputManager) return;
    
    // Register mouse move callback
    inputManager->registerMouseMoveCallback([this](int x, int y) {
        this->handleMouseMove(x, y);
    });
    
    // Register mouse button callbacks
    inputManager->registerMouseButtonPressedCallback(MouseButton::LEFT, [this](int x, int y) {
        this->handleMouseClick(x, y);
    });
}

void UIManager::update(float deltaTime) {
    if (!uiActive) return;
    
    // Update UI elements
    for (auto& button : buttons) {
        if (button) button->update(deltaTime);
    }
    
    for (auto& slider : sliders) {
        if (slider) slider->update(deltaTime);
    }
}

void UIManager::render() {
    if (!uiActive || !renderer) return;
    
    // Render UI background
    SDL_SetRenderDrawColor(renderer, 40, 40, 50, 200);
    SDL_Rect backgroundRect = {0, 500, 800, 100};  // Bottom bar
    SDL_RenderFillRect(renderer, &backgroundRect);
    
    // Render UI elements
    for (auto& button : buttons) {
        if (button) button->render(renderer);
    }
    
    for (auto& slider : sliders) {
        if (slider) slider->render(renderer);
    }
}

std::shared_ptr<Button> UIManager::createButton(int x, int y, int width, int height, 
                                              const std::string& text, ButtonCallback callback) {
    auto button = std::make_shared<Button>(x, y, width, height, text);
    button->setCallback(callback);
    buttons.push_back(button);
    return button;
}

std::shared_ptr<Slider> UIManager::createSlider(int x, int y, int width, int height, 
                                              float minValue, float maxValue, float currentValue, 
                                              SliderCallback callback) {
    auto slider = std::make_shared<Slider>(x, y, width, height, minValue, maxValue, currentValue);
    slider->setCallback(callback);
    sliders.push_back(slider);
    return slider;
}

bool UIManager::handleMouseClick(int x, int y) {
    if (!uiActive) return false;
    
    // Check if any button was clicked
    for (auto& button : buttons) {
        if (button && button->isPointInside(x, y)) {
            button->click();
            return true;
        }
    }
    
    // Check if any slider was clicked
    for (auto& slider : sliders) {
        if (slider && slider->isPointInside(x, y)) {
            slider->setValue(slider->getValueAtPosition(x));
            return true;
        }
    }
    
    return false;
}

bool UIManager::handleMouseMove(int x, int y) {
    if (!uiActive) return false;
    
    uiHovered = false;
    
    // Check if mouse is over any button
    for (auto& button : buttons) {
        if (button) {
            bool hovered = button->isPointInside(x, y);
            button->setHovered(hovered);
            uiHovered |= hovered;
        }
    }
    
    // Check if mouse is over any slider
    for (auto& slider : sliders) {
        if (slider) {
            bool hovered = slider->isPointInside(x, y);
            slider->setHovered(hovered);
            uiHovered |= hovered;
            
            // If slider is being dragged
            if (slider->isDragging()) {
                slider->setValue(slider->getValueAtPosition(x));
            }
        }
    }
    
    return uiHovered;
}
