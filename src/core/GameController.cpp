#include "GameController.h"
#include "Game.h"
#include "InputManager.h"
#include "ObjectManager.h"
#include "../physics/PhysicsEngine.h"
#include "../physics/PortalPhysics.h"
#include "../rendering/Renderer.h"
#include "../ui/UIManager.h"
#include "../ui/Button.h"
#include "../ui/Slider.h"
#include "../utils/Logger.h"

GameController::GameController(Game* game) : 
    game(game),
    objectSize(1.0f),
    portalSize(2.0f),
    currentObjectShape(ObjectShape::CIRCLE),
    currentPortalColor(PortalColor::BLUE),
    inputManager(nullptr),
    objectManager(nullptr),
    physicsEngine(nullptr),
    renderer(nullptr),
    uiManager(nullptr),
    placingBluePortal(false),
    placingOrangePortal(false),
    draggingCamera(false),
    dragStartX(0),
    dragStartY(0),
    dragCameraStartX(0.0f),
    dragCameraStartY(0.0f) {
    
    LOG_INFO("GameController created");
}

GameController::~GameController() {
    LOG_INFO("GameController destroyed");
}

void GameController::initialize() {
    if (!game) {
        LOG_ERROR("Cannot initialize GameController: game is null");
        return;
    }
    
    // Get game components
    inputManager = game->getInputManager();
    objectManager = game->getObjectManager();
    physicsEngine = game->getPhysicsEngine();
    renderer = game->getRenderer();
    uiManager = game->getUIManager();
    
    // Create portal physics helper
    if (physicsEngine) {
        portalPhysics = std::make_unique<PortalPhysics>(physicsEngine);
    }
    
    // Setup input handlers
    setupInputHandlers();
    
    // Setup UI
    setupUI();
    
    LOG_INFO("GameController initialized");
}

void GameController::update(float deltaTime) {
    // This method could be used for continuous game logic updates
    // Currently empty as most functionality is event-driven
}

void GameController::setupInputHandlers() {
    if (!inputManager) return;
    
    // Mouse click handlers
    inputManager->registerMouseButtonPressedCallback(MouseButton::LEFT, [this](int x, int y) {
        handleMouseClick(x, y, MouseButton::LEFT);
    });
    
    inputManager->registerMouseButtonPressedCallback(MouseButton::RIGHT, [this](int x, int y) {
        handleMouseClick(x, y, MouseButton::RIGHT);
    });
    
    inputManager->registerMouseButtonPressedCallback(MouseButton::MIDDLE, [this](int x, int y) {
        handleMouseClick(x, y, MouseButton::MIDDLE);
    });
    
    // Mouse move handler
    inputManager->registerMouseMoveCallback([this](int x, int y) {
        handleMouseMove(x, y);
    });
    
    // Key press handlers
    inputManager->registerKeyPressedCallback(SDLK_g, [this]() {
        toggleGravity();
    });
    
    inputManager->registerKeyPressedCallback(SDLK_1, [this]() {
        changeObjectShape(ObjectShape::CIRCLE);
    });
    
    inputManager->registerKeyPressedCallback(SDLK_2, [this]() {
        changeObjectShape(ObjectShape::RECTANGLE);
    });
    
    inputManager->registerKeyPressedCallback(SDLK_3, [this]() {
        changeObjectShape(ObjectShape::POLYGON);
    });
    
    inputManager->registerKeyPressedCallback(SDLK_c, [this]() {
        clearAllObjects();
    });
    
    inputManager->registerKeyPressedCallback(SDLK_DELETE, [this]() {
        clearAllObjects();
    });
    
    inputManager->registerKeyPressedCallback(SDLK_q, [this]() {
        currentPortalColor = PortalColor::BLUE;
    });
    
    inputManager->registerKeyPressedCallback(SDLK_e, [this]() {
        currentPortalColor = PortalColor::ORANGE;
    });
    
    LOG_DEBUG("Input handlers set up");
}

void GameController::setupUI() {
    if (!uiManager) return;
    
    // Create gravity toggle button
    auto toggleGravityBtn = uiManager->createButton(10, 550, 120, 40, "Toggle Gravity", [this]() {
        toggleGravity();
    });
    
    // Create spawn object button
    auto spawnObjectBtn = uiManager->createButton(140, 550, 120, 40, "Spawn Object", [this]() {
        int centerX = game->getWidth() / 2;
        int centerY = game->getHeight() / 2;
        spawnObject(centerX, centerY);
    });
    
    // Create clear objects button
    auto clearObjectsBtn = uiManager->createButton(270, 550, 120, 40, "Clear Objects", [this]() {
        clearAllObjects();
    });
    
    // Create object shape button
    auto shapeBtn = uiManager->createButton(400, 550, 120, 40, "Change Shape", [this]() {
        // Cycle through object shapes
        int shapeValue = static_cast<int>(currentObjectShape);
        shapeValue = (shapeValue + 1) % 3;
        changeObjectShape(static_cast<ObjectShape>(shapeValue));
    });
    
    // Create object size slider
    auto objectSizeSlider = uiManager->createSlider(530, 550, 150, 30, 0.5f, 5.0f, objectSize, [this](float value) {
        changeObjectSize(value);
    });
    objectSizeSlider->setLabel("Object Size");
    
    // Create portal size slider
    auto portalSizeSlider = uiManager->createSlider(530, 510, 150, 30, 1.0f, 3.0f, portalSize, [this](float value) {
        changePortalSize(value);
    });
    portalSizeSlider->setLabel("Portal Size");
    
    // Create portal color button
    auto portalColorBtn = uiManager->createButton(400, 510, 120, 40, "Portal Color", [this]() {
        // Toggle portal color
        currentPortalColor = (currentPortalColor == PortalColor::BLUE) ? 
                              PortalColor::ORANGE : PortalColor::BLUE;
    });
    
    LOG_DEBUG("UI elements set up");
}

void GameController::handleMouseClick(int x, int y, MouseButton button) {
    // First check if the UI was clicked
    if (uiManager && uiManager->handleMouseClick(x, y)) {
        return;  // UI handled the click, don't process game actions
    }
    
    switch (button) {
        case MouseButton::LEFT:
            spawnObject(x, y);
            break;
            
        case MouseButton::RIGHT:
            placePortal(x, y, currentPortalColor);
            break;
            
        case MouseButton::MIDDLE:
            // Start camera dragging
            draggingCamera = true;
            dragStartX = x;
            dragStartY = y;
            
            if (renderer) {
                // Store camera position at start of drag
                // Note: These getter methods would need to be added to Renderer
                dragCameraStartX = renderer->getCameraX();
                dragCameraStartY = renderer->getCameraY();
            }
            break;
    }
}

void GameController::handleMouseMove(int x, int y) {
    // Handle camera dragging
    if (draggingCamera && renderer) {
        float dx = (dragStartX - x) / renderer->getCameraZoom();
        float dy = (dragStartY - y) / renderer->getCameraZoom();
        
        renderer->setCameraPosition(
            dragCameraStartX + dx,
            dragCameraStartY + dy
        );
    }
    
    // Handle UI hover
    if (uiManager) {
        uiManager->handleMouseMove(x, y);
    }
}

b2Vec2 GameController::screenToWorld(int x, int y) {
    if (!renderer) {
        return b2Vec2(0.0f, 0.0f);
    }
    
    // Convert screen coordinates to world coordinates
    float worldX = (x - game->getWidth() / 2.0f) / renderer->getCameraZoom() + renderer->getCameraX();
    float worldY = (y - game->getHeight() / 2.0f) / renderer->getCameraZoom() + renderer->getCameraY();
    
    return b2Vec2(worldX, worldY);
}

void GameController::spawnObject(int x, int y) {
    if (!objectManager) return;
    
    // Convert screen position to world position
    b2Vec2 worldPos = screenToWorld(x, y);
    
    // Create the object
    auto object = objectManager->createDynamicObject(currentObjectShape, worldPos.x, worldPos.y);
    
    if (object) {
        // Set object size
        switch (currentObjectShape) {
            case ObjectShape::CIRCLE:
                object->setRadius(objectSize / 2.0f);
                break;
            default:
                object->setSize(objectSize, objectSize);
                break;
        }
        
        LOG_INFO("Spawned " + std::to_string(static_cast<int>(currentObjectShape)) + 
                 " object at (" + std::to_string(worldPos.x) + ", " + 
                 std::to_string(worldPos.y) + ") with size " + std::to_string(objectSize));
    }
}

void GameController::placePortal(int x, int y, PortalColor color) {
    if (!objectManager || !portalPhysics) return;
    
    // Convert screen position to world position
    b2Vec2 worldPos = screenToWorld(x, y);
    
    // Find portal of the same color to replace or create new
    std::shared_ptr<Portal> portal = nullptr;
    for (const auto& p : objectManager->getPortals()) {
        if (p->getColor() == color) {
            portal = p;
            break;
        }
    }
    
    if (!portal) {
        portal = objectManager->createPortal(color, 0, 0, 0);
    }
    
    if (portal) {
        // Set size before placing
        portal->setSize(portalSize, portalSize * 2);
        
        // Place portal at position with appropriate angle
        // For simplicity, we'll use a fixed angle, but ideally this would be calculated
        // based on detected surfaces using ray casting
        float angle = 0.0f;
        
        if (portalPhysics->placePortal(portal, worldPos.x, worldPos.y, angle)) {
            // If we just created both portals, link them
            if (objectManager->getPortals().size() == 2) {
                auto portals = objectManager->getPortals();
                if (portals[0]->getColor() != portals[1]->getColor()) {
                    objectManager->linkPortals(portals[0], portals[1]);
                }
            }
            
            LOG_INFO("Placed " + std::string(color == PortalColor::BLUE ? "blue" : "orange") + 
                     " portal at (" + std::to_string(worldPos.x) + ", " + 
                     std::to_string(worldPos.y) + ")");
        }
    }
}

void GameController::toggleGravity() {
    if (physicsEngine) {
        physicsEngine->toggleGravity();
        LOG_INFO("Gravity toggled: " + std::string(physicsEngine->isGravityEnabled() ? "ON" : "OFF"));
    }
}

void GameController::clearAllObjects() {
    if (!objectManager) return;
    
    // Get copy of objects to destroy
    auto dynamicObjects = objectManager->getDynamicObjects();
    
    // Destroy all dynamic objects
    for (const auto& obj : dynamicObjects) {
        objectManager->destroyEntity(obj->getId());
    }
    
    LOG_INFO("All dynamic objects cleared");
}

void GameController::changeObjectSize(float size) {
    objectSize = size;
    LOG_DEBUG("Object size set to " + std::to_string(size));
}

void GameController::changePortalSize(float size) {
    portalSize = size;
    LOG_DEBUG("Portal size set to " + std::to_string(size));
}

void GameController::changeObjectShape(ObjectShape shape) {
    currentObjectShape = shape;
    
    std::string shapeName;
    switch (shape) {
        case ObjectShape::CIRCLE: shapeName = "Circle"; break;
        case ObjectShape::RECTANGLE: shapeName = "Rectangle"; break;
        case ObjectShape::POLYGON: shapeName = "Polygon"; break;
    }
    
    LOG_DEBUG("Object shape set to " + shapeName);
}
