#pragma once

#include <SDL2/SDL.h>
#include <memory>
#include <vector>
#include <unordered_map>

class Game;
class PhysicsEngine;
class ObjectManager;
class TextureManager;
class PortalRenderer;

// Forward declarations of entity classes
class DynamicObject;
class Portal;

class Renderer {
private:
    SDL_Renderer* sdlRenderer;
    int screenWidth;
    int screenHeight;
    
    // Camera properties
    float cameraX;
    float cameraY;
    float cameraZoom;
    
    // Game references
    Game* game;
    
    // Managers
    std::unique_ptr<TextureManager> textureManager;
    std::unique_ptr<PortalRenderer> portalRenderer;
    
    // Helpers
    SDL_Rect worldToScreen(float x, float y, float width, float height);
    SDL_Point worldToScreen(float x, float y);
    
    // Debug drawing
    bool debugDrawEnabled;
    
public:
    Renderer(SDL_Renderer* renderer, int width, int height);
    ~Renderer();
    
    void initialize();
    void setGame(Game* gameInstance);
    
    // Basic rendering
    void clear();
    void present();
    void render();
    
    // Specialized rendering
    void renderDynamicObject(DynamicObject* object);
    void renderPortal(Portal* portal);
    void renderBackground();
    void renderDebugInfo();
    
    // Camera controls
    void setCameraPosition(float x, float y);
    float getCameraX() const { return cameraX; }
    float getCameraY() const { return cameraY; }
    void setCameraZoom(float zoom);
    float getCameraZoom() const { return cameraZoom; }
    void moveCamera(float dx, float dy);
    void zoomCamera(float factor);
    
    // Texture management
    bool loadTexture(const std::string& name, const std::string& filepath);
    void unloadTexture(const std::string& name);
    
    // Debug rendering
    void toggleDebugDraw();
    bool isDebugDrawEnabled() const { return debugDrawEnabled; }
    
    // Getters
    TextureManager* getTextureManager() const;
    PortalRenderer* getPortalRenderer() const;
    SDL_Renderer* getSDLRenderer() const;
};
