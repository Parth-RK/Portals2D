#include "Game.h"
#include "GameController.h"
#include "../utils/Logger.h"
#include "../utils/Config.h"
#include <iostream>
#include <stdexcept>

int main(int argc, char* argv[]) {
    try {
        // Initialize logger
        Logger::getInstance()->setLogLevel(LogLevel::DEBUG);
        LOG_INFO("2D Portals Game Starting");
        
        // Load configuration
        Config* config = Config::getInstance();
        config->loadDefaultConfig();
        
        // Try to load from file (not critical if it fails)
        try {
            config->loadFromFile("config.txt");
        }
        catch (const std::exception& e) {
            LOG_WARNING("Failed to load config file: " + std::string(e.what()));
            LOG_INFO("Using default configuration");
        }
        
        // Create and initialize game
        Game game;
        if (!game.initialize()) {
            LOG_ERROR("Game initialization failed");
            return 1;
        }
        
        // Setup initial game state
        GameController* gameController = game.getGameController();
        ObjectManager* objectManager = game.getObjectManager();
        PhysicsEngine* physicsEngine = game.getPhysicsEngine();
        
        if (gameController && objectManager && physicsEngine) {
            // Create boundary walls to contain objects
            LOG_INFO("Creating boundary walls");
            
            // Create floor
            b2Body* floorBody = physicsEngine->createStaticBody(0.0f, 15.0f, 0.0f);
            physicsEngine->createBoxFixture(floorBody, 40.0f, 1.0f);
            
            // Create ceiling
            b2Body* ceilingBody = physicsEngine->createStaticBody(0.0f, -15.0f, 0.0f);
            physicsEngine->createBoxFixture(ceilingBody, 40.0f, 1.0f);
            
            // Create left wall
            b2Body* leftWallBody = physicsEngine->createStaticBody(-20.0f, 0.0f, 0.0f);
            physicsEngine->createBoxFixture(leftWallBody, 1.0f, 30.0f);
            
            // Create right wall
            b2Body* rightWallBody = physicsEngine->createStaticBody(20.0f, 0.0f, 0.0f);
            physicsEngine->createBoxFixture(rightWallBody, 1.0f, 30.0f);
            
            // Create some initial objects
            LOG_INFO("Creating initial objects");
            auto circle = objectManager->createDynamicObject(ObjectShape::CIRCLE, -10.0f, 0.0f);
            if (circle) {
                circle->setRadius(1.0f);
            }
            
            auto box = objectManager->createDynamicObject(ObjectShape::RECTANGLE, 10.0f, 0.0f);
            if (box) {
                box->setSize(2.0f, 2.0f);
            }
        }
        
        // Run the game
        game.run();
        
        // Save config
        try {
            config->saveToFile("config.txt");
        }
        catch (const std::exception& e) {
            LOG_WARNING("Failed to save config file: " + std::string(e.what()));
        }
        
        LOG_INFO("Game shutting down normally");
        return 0;
    }
    catch (const std::exception& e) {
        std::cerr << "Fatal error: " << e.what() << std::endl;
        LOG_ERROR("Fatal error: " + std::string(e.what()));
        return 1;
    }
    catch (...) {
        std::cerr << "Unknown fatal error occurred!" << std::endl;
        LOG_ERROR("Unknown fatal error occurred!");
        return 1;
    }
}
