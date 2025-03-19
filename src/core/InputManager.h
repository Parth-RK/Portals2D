#pragma once

#include <SDL2/SDL.h>
#include <vector>
#include <unordered_map>
#include <functional>

enum class MouseButton {
    LEFT,
    MIDDLE,
    RIGHT
};

struct MouseState {
    int x;
    int y;
    bool buttons[3];  // LEFT, MIDDLE, RIGHT
    int wheel;
};

typedef std::function<void()> KeyCallback;
typedef std::function<void(int x, int y)> MouseMoveCallback;
typedef std::function<void(int x, int y)> MouseButtonCallback;

class InputManager {
private:
    bool quitRequested;
    
    // Keyboard state
    const Uint8* keyboardState;
    std::unordered_map<SDL_Keycode, bool> keyStates;
    std::unordered_map<SDL_Keycode, KeyCallback> keyPressedCallbacks;
    std::unordered_map<SDL_Keycode, KeyCallback> keyReleasedCallbacks;
    
    // Mouse state
    MouseState mouseState;
    MouseState previousMouseState;
    MouseMoveCallback mouseMoveCallback;
    std::unordered_map<MouseButton, MouseButtonCallback> mouseButtonPressedCallbacks;
    std::unordered_map<MouseButton, MouseButtonCallback> mouseButtonReleasedCallbacks;
    
    // Helper methods
    void updateMouseState(const SDL_Event& event);
    void handleKeyboardEvent(const SDL_Event& event);
    void handleMouseButtonEvent(const SDL_Event& event);
    
public:
    InputManager();
    ~InputManager();
    
    void processEvents();
    
    // Keyboard input
    bool isKeyDown(SDL_Keycode key) const;
    bool isKeyPressed(SDL_Keycode key) const;  // Pressed this frame
    bool isKeyReleased(SDL_Keycode key) const; // Released this frame
    
    // Mouse input
    bool isMouseButtonDown(MouseButton button) const;
    bool isMouseButtonPressed(MouseButton button) const;  // Pressed this frame
    bool isMouseButtonReleased(MouseButton button) const; // Released this frame
    int getMouseX() const;
    int getMouseY() const;
    int getMouseWheel() const;
    
    // Event callbacks
    void registerKeyPressedCallback(SDL_Keycode key, KeyCallback callback);
    void registerKeyReleasedCallback(SDL_Keycode key, KeyCallback callback);
    void registerMouseMoveCallback(MouseMoveCallback callback);
    void registerMouseButtonPressedCallback(MouseButton button, MouseButtonCallback callback);
    void registerMouseButtonReleasedCallback(MouseButton button, MouseButtonCallback callback);
    
    // Window events
    bool isQuitRequested() const;
};
