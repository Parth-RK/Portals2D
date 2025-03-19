#pragma once

#include <SDL2/SDL.h>
#include <memory>
#include <string>

class GameLoop;
class InputManager;
class ObjectManager;
class PhysicsEngine;
class Renderer;
class UIManager;
class GameController;

class Game {
private:
    bool running;
    std::string title;
    int width;
    int height;
    
    // SDL components
    SDL_Window* window;
    SDL_Renderer* renderer;
    
    // Game subsystems
    std::unique_ptr<GameLoop> gameLoop;
    std::unique_ptr<InputManager> inputManager;
    std::unique_ptr<ObjectManager> objectManager;
    std::unique_ptr<PhysicsEngine> physicsEngine;
    std::unique_ptr<Renderer> renderSystem;
    std::unique_ptr<UIManager> uiManager;
    std::unique_ptr<GameController> gameController;
    
    // Initialization helpers
    bool initSDL();
    bool initSubsystems();
    
public:
    Game();
    ~Game();
    
    bool initialize();
    void run();
    void stop();
    
    // Getters for subsystems (used by other components)
    GameLoop* getGameLoop() const;
    InputManager* getInputManager() const;
    ObjectManager* getObjectManager() const;
    PhysicsEngine* getPhysicsEngine() const;
    Renderer* getRenderer() const;
    UIManager* getUIManager() const;
    GameController* getGameController() const;
    
    // Window getters
    SDL_Window* getWindow() const;
    SDL_Renderer* getSDLRenderer() const;
    int getWidth() const;
    int getHeight() const;
};
