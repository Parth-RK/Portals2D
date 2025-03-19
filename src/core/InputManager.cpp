#include "InputManager.h"
#include "../utils/Logger.h"

InputManager::InputManager() :
    quitRequested(false),
    keyboardState(nullptr) {
    
    // Initialize keyboard state
    keyboardState = SDL_GetKeyboardState(nullptr);
    
    // Initialize mouse state
    mouseState = {0, 0, {false, false, false}, 0};
    previousMouseState = mouseState;
    
    LOG_DEBUG("Input manager initialized");
}

InputManager::~InputManager() {
    LOG_DEBUG("Input manager destroyed");
}

void InputManager::processEvents() {
    // Save previous mouse state
    previousMouseState = mouseState;
    
    // Reset wheel state (wheel events are only valid for one frame)
    mouseState.wheel = 0;
    
    // Process SDL events
    SDL_Event event;
    while (SDL_PollEvent(&event)) {
        switch (event.type) {
            case SDL_QUIT:
                quitRequested = true;
                break;
                
            case SDL_KEYDOWN:
            case SDL_KEYUP:
                handleKeyboardEvent(event);
                break;
                
            case SDL_MOUSEMOTION:
                updateMouseState(event);
                if (mouseMoveCallback) {
                    mouseMoveCallback(mouseState.x, mouseState.y);
                }
                break;
                
            case SDL_MOUSEBUTTONDOWN:
            case SDL_MOUSEBUTTONUP:
                handleMouseButtonEvent(event);
                break;
                
            case SDL_MOUSEWHEEL:
                mouseState.wheel = event.wheel.y;
                break;
        }
    }
}

void InputManager::updateMouseState(const SDL_Event& event) {
    if (event.type == SDL_MOUSEMOTION) {
        mouseState.x = event.motion.x;
        mouseState.y = event.motion.y;
    }
}

void InputManager::handleKeyboardEvent(const SDL_Event& event) {
    SDL_Keycode key = event.key.keysym.sym;
    
    if (event.type == SDL_KEYDOWN) {
        keyStates[key] = true;
        
        // Call key pressed callback if registered
        auto it = keyPressedCallbacks.find(key);
        if (it != keyPressedCallbacks.end() && it->second) {
            it->second();
        }
    }
    else if (event.type == SDL_KEYUP) {
        keyStates[key] = false;
        
        // Call key released callback if registered
        auto it = keyReleasedCallbacks.find(key);
        if (it != keyReleasedCallbacks.end() && it->second) {
            it->second();
        }
    }
}

void InputManager::handleMouseButtonEvent(const SDL_Event& event) {
    int button = -1;
    
    switch (event.button.button) {
        case SDL_BUTTON_LEFT:   button = 0; break;
        case SDL_BUTTON_MIDDLE: button = 1; break;
        case SDL_BUTTON_RIGHT:  button = 2; break;
        default: return;  // Unsupported button
    }
    
    if (event.type == SDL_MOUSEBUTTONDOWN) {
        mouseState.buttons[button] = true;
        
        // Call button pressed callback if registered
        auto buttonEnum = static_cast<MouseButton>(button);
        auto it = mouseButtonPressedCallbacks.find(buttonEnum);
        if (it != mouseButtonPressedCallbacks.end() && it->second) {
            it->second(mouseState.x, mouseState.y);
        }
    }
    else if (event.type == SDL_MOUSEBUTTONUP) {
        mouseState.buttons[button] = false;
        
        // Call button released callback if registered
        auto buttonEnum = static_cast<MouseButton>(button);
        auto it = mouseButtonReleasedCallbacks.find(buttonEnum);
        if (it != mouseButtonReleasedCallbacks.end() && it->second) {
            it->second(mouseState.x, mouseState.y);
        }
    }
}

bool InputManager::isKeyDown(SDL_Keycode key) const {
    auto it = keyStates.find(key);
    return (it != keyStates.end()) ? it->second : false;
}

bool InputManager::isKeyPressed(SDL_Keycode key) const {
    // Not implemented yet - would need to track key states from previous frame
    return false;
}

bool InputManager::isKeyReleased(SDL_Keycode key) const {
    // Not implemented yet - would need to track key states from previous frame
    return false;
}

bool InputManager::isMouseButtonDown(MouseButton button) const {
    int index = static_cast<int>(button);
    return mouseState.buttons[index];
}

bool InputManager::isMouseButtonPressed(MouseButton button) const {
    int index = static_cast<int>(button);
    return mouseState.buttons[index] && !previousMouseState.buttons[index];
}

bool InputManager::isMouseButtonReleased(MouseButton button) const {
    int index = static_cast<int>(button);
    return !mouseState.buttons[index] && previousMouseState.buttons[index];
}

int InputManager::getMouseX() const {
    return mouseState.x;
}

int InputManager::getMouseY() const {
    return mouseState.y;
}

int InputManager::getMouseWheel() const {
    return mouseState.wheel;
}

void InputManager::registerKeyPressedCallback(SDL_Keycode key, KeyCallback callback) {
    keyPressedCallbacks[key] = callback;
}

void InputManager::registerKeyReleasedCallback(SDL_Keycode key, KeyCallback callback) {
    keyReleasedCallbacks[key] = callback;
}

void InputManager::registerMouseMoveCallback(MouseMoveCallback callback) {
    mouseMoveCallback = callback;
}

void InputManager::registerMouseButtonPressedCallback(MouseButton button, MouseButtonCallback callback) {
    mouseButtonPressedCallbacks[button] = callback;
}

void InputManager::registerMouseButtonReleasedCallback(MouseButton button, MouseButtonCallback callback) {
    mouseButtonReleasedCallbacks[button] = callback;
}

bool InputManager::isQuitRequested() const {
    return quitRequested;
}
