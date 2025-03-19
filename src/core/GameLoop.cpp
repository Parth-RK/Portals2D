#include "GameLoop.h"
#include "Game.h"
#include "InputManager.h"
#include "ObjectManager.h"
#include "../physics/PhysicsEngine.h"
#include "../rendering/Renderer.h"
#include "../ui/UIManager.h"
#include "../utils/Logger.h"

GameLoop::GameLoop(Game* gameInstance) :
    game(gameInstance),
    running(false),
    lastFrameTime(0),
    deltaTime(0.0f),
    timeAccumulator(0.0f),
    fixedTimeStep(1.0f / 60.0f),
    frameCount(0),
    frameCountTimer(0.0f),
    fps(0) {
    
    LOG_DEBUG("Game loop created");
}

GameLoop::~GameLoop() {
    LOG_DEBUG("Game loop destroyed");
}

void GameLoop::start() {
    if (!game) {
        LOG_ERROR("Cannot start game loop: no game instance");
        return;
    }
    
    running = true;
    lastFrameTime = SDL_GetTicks();
    
    // Main loop
    while (running) {
        calculateDeltaTime();
        processInput();
        update();
        render();
        limitFPS();
    }
}

void GameLoop::stop() {
    running = false;
    LOG_INFO("Game loop stopped");
}

void GameLoop::calculateDeltaTime() {
    // Calculate time elapsed since last frame
    Uint32 currentTime = SDL_GetTicks();
    deltaTime = (currentTime - lastFrameTime) / 1000.0f; // Convert to seconds
    lastFrameTime = currentTime;
    
    // Limit delta time to avoid "spiral of death" when lagging
    if (deltaTime > 0.25f) {
        deltaTime = 0.25f;
    }
    
    // Update accumulator for fixed time step updates
    timeAccumulator += deltaTime;
    
    // Update FPS counter
    frameCount++;
    frameCountTimer += deltaTime;
    
    if (frameCountTimer >= 1.0f) {
        fps = frameCount;
        frameCount = 0;
        frameCountTimer = 0;
        
        LOG_DEBUG("FPS: " + std::to_string(fps));
    }
}

void GameLoop::processInput() {
    if (!game) return;
    
    // Get input manager
    InputManager* input = game->getInputManager();
    if (!input) return;
    
    // Process input events
    input->processEvents();
    
    // Check for quit
    if (input->isQuitRequested()) {
        stop();
        game->stop();
    }
}

void GameLoop::update() {
    if (!game) return;
    
    // Get necessary subsystems
    PhysicsEngine* physics = game->getPhysicsEngine();
    ObjectManager* objects = game->getObjectManager();
    UIManager* ui = game->getUIManager();
    
    // Fixed time step for physics
    while (timeAccumulator >= fixedTimeStep) {
        // Update physics
        if (physics) {
            physics->update(fixedTimeStep);
        }
        
        // Update game objects
        if (objects) {
            objects->update(fixedTimeStep);
        }
        
        // Subtract fixed time step from accumulator
        timeAccumulator -= fixedTimeStep;
    }
    
    // Update UI (variable time step is fine for UI)
    if (ui) {
        ui->update(deltaTime);
    }
}

void GameLoop::render() {
    if (!game) return;
    
    // Get renderer
    Renderer* renderer = game->getRenderer();
    UIManager* ui = game->getUIManager();
    
    if (!renderer) return;
    
    // Clear screen
    renderer->clear();
    
    // Render game objects
    renderer->render();
    
    // Render UI on top
    if (ui) {
        ui->render();
    }
    
    // Present rendered frame
    renderer->present();
}

void GameLoop::limitFPS(int targetFPS) {
    // Calculate frame delay to maintain target FPS
    const int frameDelay = 1000 / targetFPS;
    Uint32 frameTime = SDL_GetTicks() - lastFrameTime;
    
    // If we're rendering too fast, delay
    if (frameDelay > frameTime) {
        SDL_Delay(frameDelay - frameTime);
    }
}

float GameLoop::getDeltaTime() const {
    return deltaTime;
}

int GameLoop::getFPS() const {
    return fps;
}
