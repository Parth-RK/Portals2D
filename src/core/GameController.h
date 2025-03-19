#pragma once

#include <memory>
#include <functional>
#include "../entities/DynamicObject.h"
#include "../entities/Portal.h"

class Game;
class InputManager;
class ObjectManager;
class PhysicsEngine;
class Renderer;
class UIManager;
class PortalPhysics;

// This class connects user input and UI with game functionality
class GameController {
private:
    Game* game;
    
    // Game configuration
    float objectSize;
    float portalSize;
    ObjectShape currentObjectShape;
    PortalColor currentPortalColor;
    
    // Stored references to game components
    InputManager* inputManager;
    ObjectManager* objectManager;
    PhysicsEngine* physicsEngine;
    Renderer* renderer;
    UIManager* uiManager;
    
    // Portal physics helper
    std::unique_ptr<PortalPhysics> portalPhysics;
    
    // State variables
    bool placingBluePortal;
    bool placingOrangePortal;
    bool draggingCamera;
    int dragStartX, dragStartY;
    float dragCameraStartX, dragCameraStartY;
    
    // Input handling methods
    void setupInputHandlers();
    void handleMouseClick(int x, int y, MouseButton button);
    void handleMouseMove(int x, int y);
    void handleKeyPress(SDL_Keycode key);
    
    // Game actions
    void spawnObject(int x, int y);
    void placePortal(int x, int y, PortalColor color);
    void toggleGravity();
    void clearAllObjects();
    void changeObjectSize(float size);
    void changePortalSize(float size);
    void changeObjectShape(ObjectShape shape);
    
    // UI setup
    void setupUI();

public:
    GameController(Game* game);
    ~GameController();
    
    void initialize();
    void update(float deltaTime);
    
    // World to screen conversions
    b2Vec2 screenToWorld(int x, int y);
};
