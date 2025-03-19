#include "Game.h"
#include "GameLoop.h"
#include "InputManager.h"
#include "ObjectManager.h"
#include "GameController.h"
#include "../physics/PhysicsEngine.h"
#include "../rendering/Renderer.h"
#include "../ui/UIManager.h"
#include "../utils/Config.h"
#include "../utils/Logger.h"

Game::Game() : 
    running(false),
    title("2D Portals Game"),
    width(800),
    height(600),
    window(nullptr),
    renderer(nullptr) {
    
    // Load settings from config
    Config* config = Config::getInstance();
    title = config->getString("window_title", "2D Portals Game");
    width = config->getInt("window_width", 800);
    height = config->getInt("window_height", 600);
}

Game::~Game() {
    // SDL cleanup
    if (renderer) {
        SDL_DestroyRenderer(renderer);
    }
    
    if (window) {
        SDL_DestroyWindow(window);
    }
    
    // Quit SDL subsystems
    SDL_Quit();
    
    LOG_INFO("Game destroyed");
}

bool Game::initialize() {
    LOG_INFO("Initializing game...");
    
    // Initialize SDL
    if (!initSDL()) {
        LOG_ERROR("Failed to initialize SDL");
        return false;
    }
    
    // Initialize subsystems
    if (!initSubsystems()) {
        LOG_ERROR("Failed to initialize game subsystems");
        return false;
    }
    
    running = true;
    LOG_INFO("Game initialized successfully");
    return true;
}

bool Game::initSDL() {
    // Initialize SDL
    if (SDL_Init(SDL_INIT_VIDEO | SDL_INIT_TIMER) < 0) {
        LOG_ERROR("SDL could not initialize! SDL_Error: " + std::string(SDL_GetError()));
        return false;
    }
    
    // Create window
    window = SDL_CreateWindow(
        title.c_str(),
        SDL_WINDOWPOS_UNDEFINED,
        SDL_WINDOWPOS_UNDEFINED,
        width,
        height,
        SDL_WINDOW_SHOWN
    );
    
    if (window == nullptr) {
        LOG_ERROR("Window could not be created! SDL_Error: " + std::string(SDL_GetError()));
        return false;
    }
    
    // Create renderer
    renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED);
    
    if (renderer == nullptr) {
        LOG_ERROR("Renderer could not be created! SDL_Error: " + std::string(SDL_GetError()));
        return false;
    }
    
    // Set render color
    SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255);
    
    LOG_INFO("SDL initialized successfully");
    return true;
}

bool Game::initSubsystems() {
    try {
        // Create physics engine
        physicsEngine = std::make_unique<PhysicsEngine>();
        physicsEngine->initialize();
        
        // Create renderer system
        renderSystem = std::make_unique<Renderer>(renderer, width, height);
        renderSystem->initialize();
        
        // Create object manager
        objectManager = std::make_unique<ObjectManager>(physicsEngine.get());
        
        // Create input manager
        inputManager = std::make_unique<InputManager>();
        
        // Create UI manager
        uiManager = std::make_unique<UIManager>(renderer, inputManager.get());
        uiManager->initialize();
        
        // Create game controller
        gameController = std::make_unique<GameController>(this);
        gameController->initialize();
        
        // Create game loop
        gameLoop = std::make_unique<GameLoop>(this);
        
        LOG_INFO("All subsystems initialized successfully");
        return true;
    }
    catch (const std::exception& e) {
        LOG_ERROR("Failed to initialize subsystems: " + std::string(e.what()));
        return false;
    }
}

void Game::run() {
    if (!running) {
        LOG_WARNING("Attempted to run game before initialization");
        return;
    }
    
    LOG_INFO("Starting game loop");
    gameLoop->start();
}

void Game::stop() {
    running = false;
    LOG_INFO("Stopping game");
}

// Getters
GameLoop* Game::getGameLoop() const {
    return gameLoop.get();
}

InputManager* Game::getInputManager() const {
    return inputManager.get();
}

ObjectManager* Game::getObjectManager() const {
    return objectManager.get();
}

PhysicsEngine* Game::getPhysicsEngine() const {
    return physicsEngine.get();
}

Renderer* Game::getRenderer() const {
    return renderSystem.get();
}

UIManager* Game::getUIManager() const {
    return uiManager.get();
}

GameController* Game::getGameController() const {
    return gameController.get();
}

SDL_Window* Game::getWindow() const {
    return window;
}

SDL_Renderer* Game::getSDLRenderer() const {
    return renderer;
}

int Game::getWidth() const {
    return width;
}

int Game::getHeight() const {
    return height;
}
