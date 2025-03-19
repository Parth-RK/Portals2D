#include "Renderer.h"
#include "TextureManager.h"
#include "PortalRenderer.h"
#include "../core/Game.h"
#include "../core/ObjectManager.h"
#include "../entities/DynamicObject.h"
#include "../entities/Portal.h"
#include "../physics/PhysicsEngine.h"
#include "../utils/Logger.h"
#include <SDL2/SDL2_gfxPrimitives.h>
#include <string>
#include <sstream>

Renderer::Renderer(SDL_Renderer* renderer, int width, int height) :
    sdlRenderer(renderer),
    screenWidth(width),
    screenHeight(height),
    cameraX(0.0f),
    cameraY(0.0f),
    cameraZoom(20.0f),  // Pixels per unit (higher = more zoomed in)
    game(nullptr),
    debugDrawEnabled(true) {
    
    LOG_DEBUG("Renderer created with dimensions " + 
              std::to_string(width) + "x" + std::to_string(height));
}

Renderer::~Renderer() {
    LOG_DEBUG("Renderer destroyed");
}

void Renderer::initialize() {
    // Initialize texture manager
    textureManager = std::make_unique<TextureManager>(sdlRenderer);
    
    // Initialize portal renderer
    portalRenderer = std::make_unique<PortalRenderer>(this);
    
    // Load default textures
    loadTexture("blue_portal", "assets/textures/blue_portal.png");
    loadTexture("orange_portal", "assets/textures/orange_portal.png");
    loadTexture("box", "assets/textures/box.png");
    loadTexture("circle", "assets/textures/circle.png");
    loadTexture("background", "assets/textures/background.png");
    
    LOG_INFO("Renderer initialized");
}

void Renderer::setGame(Game* gameInstance) {
    game = gameInstance;
}

void Renderer::clear() {
    SDL_SetRenderDrawColor(sdlRenderer, 0, 0, 0, 255);
    SDL_RenderClear(sdlRenderer);
}

void Renderer::present() {
    SDL_RenderPresent(sdlRenderer);
}

void Renderer::render() {
    if (!game) {
        LOG_WARNING("Cannot render, game reference not set");
        return;
    }
    
    // Render background first
    renderBackground();
    
    // Render portals
    ObjectManager* objectManager = game->getObjectManager();
    if (objectManager) {
        // Render portals first (they should appear behind objects)
        for (const auto& portal : objectManager->getPortals()) {
            if (portal && portal->getIsActive()) {
                renderPortal(portal.get());
            }
        }
        
        // Then render dynamic objects
        for (const auto& obj : objectManager->getDynamicObjects()) {
            if (obj && obj->getIsActive()) {
                renderDynamicObject(obj.get());
            }
        }
    }
    
    // Render debug info if enabled
    if (isDebugDrawEnabled()) {
        renderDebugInfo();
    }
}

SDL_Rect Renderer::worldToScreen(float x, float y, float width, float height) {
    SDL_Rect rect;
    
    // Convert world coordinates to screen coordinates
    // Origin is center of the screen
    float screenX = (x - cameraX) * cameraZoom + screenWidth / 2.0f;
    float screenY = (y - cameraY) * cameraZoom + screenHeight / 2.0f;
    
    // Convert dimensions
    float screenWidth = width * cameraZoom;
    float screenHeight = height * cameraZoom;
    
    // Set rectangle
    rect.x = static_cast<int>(screenX - screenWidth / 2.0f);
    rect.y = static_cast<int>(screenY - screenHeight / 2.0f);
    rect.w = static_cast<int>(screenWidth);
    rect.h = static_cast<int>(screenHeight);
    
    return rect;
}

SDL_Point Renderer::worldToScreen(float x, float y) {
    SDL_Point point;
    
    // Convert world coordinates to screen coordinates
    point.x = static_cast<int>((x - cameraX) * cameraZoom + screenWidth / 2.0f);
    point.y = static_cast<int>((y - cameraY) * cameraZoom + screenHeight / 2.0f);
    
    return point;
}

void Renderer::renderDynamicObject(DynamicObject* object) {
    if (!object) return;
    
    // Get object properties
    b2Vec2 position = object->getPosition();
    float angle = object->getAngle();
    ObjectShape shape = object->getShape();
    std::string textureName = object->getTextureName();
    
    // If no texture specified, use default based on shape
    if (textureName.empty()) {
        switch (shape) {
            case ObjectShape::CIRCLE:
                textureName = "circle";
                break;
            case ObjectShape::RECTANGLE:
            case ObjectShape::POLYGON:
                textureName = "box";
                break;
        }
    }
    
    // Get dimensions based on shape
    float width, height;
    
    switch (shape) {
        case ObjectShape::CIRCLE:
            width = height = object->getRadius() * 2.0f;
            break;
        case ObjectShape::RECTANGLE:
        case ObjectShape::POLYGON:
            width = object->getWidth();
            height = object->getHeight();
            break;
    }
    
    // Convert to screen space
    SDL_Rect destRect = worldToScreen(position.x, position.y, width, height);
    
    // Render the object
    if (textureManager->hasTexture(textureName)) {
        // Use the texture
        SDL_Texture* texture = textureManager->getTexture(textureName);
        
        // Convert angle from radians to degrees
        double angleDegrees = angle * 180.0 / M_PI;
        
        SDL_RenderCopyEx(sdlRenderer, texture, nullptr, &destRect, angleDegrees, nullptr, SDL_FLIP_NONE);
    } else {
        // Fallback: render a colored rectangle or circle
        switch (shape) {
            case ObjectShape::CIRCLE:
                filledCircleRGBA(
                    sdlRenderer,
                    destRect.x + destRect.w / 2,
                    destRect.y + destRect.h / 2,
                    destRect.w / 2,
                    255, 100, 100, 255
                );
                break;
                
            case ObjectShape::RECTANGLE:
                // Draw a rectangle
                SDL_SetRenderDrawColor(sdlRenderer, 100, 100, 255, 255);
                SDL_RenderFillRect(sdlRenderer, &destRect);
                break;
                
            case ObjectShape::POLYGON:
                // Draw a triangle for polygon
                filledTrigonRGBA(
                    sdlRenderer,
                    destRect.x, destRect.y + destRect.h,
                    destRect.x + destRect.w, destRect.y + destRect.h,
                    destRect.x + destRect.w / 2, destRect.y,
                    100, 255, 100, 255
                );
                break;
        }
    }
    
    // Debug rendering
    if (isDebugDrawEnabled()) {
        // Draw bounding box
        rectangleRGBA(
            sdlRenderer,
            destRect.x, destRect.y,
            destRect.x + destRect.w, destRect.y + destRect.h,
            255, 255, 0, 255
        );
        
        // Draw center point
        SDL_Point center = worldToScreen(position.x, position.y);
        filledCircleRGBA(
            sdlRenderer,
            center.x, center.y,
            3,  // Small radius
            255, 0, 0, 255
        );
    }
}

void Renderer::renderPortal(Portal* portal) {
    if (!portal) return;
    
    // Use portal renderer for advanced portal effects
    if (portalRenderer) {
        portalRenderer->renderPortal(portal);
        return;
    }
    
    // Fallback simple portal rendering
    b2Vec2 position = portal->getPosition();
    float angle = portal->getAngle();
    float width = portal->getWidth();
    float height = portal->getHeight();
    
    // Determine color based on portal type
    Uint8 r = 0, g = 0, b = 0;
    if (portal->getColor() == PortalColor::BLUE) {
        r = 0;
        g = 100;
        b = 255;
    } else {
        r = 255;
        g = 100;
        b = 0;
    }
    
    // Convert to screen space
    SDL_Rect destRect = worldToScreen(position.x, position.y, width, height);
    
    // Draw portal
    SDL_SetRenderDrawColor(sdlRenderer, r, g, b, 200);
    SDL_RenderFillRect(sdlRenderer, &destRect);
    
    // Debug drawing
    if (isDebugDrawEnabled()) {
        // Draw border
        rectangleRGBA(
            sdlRenderer,
            destRect.x, destRect.y,
            destRect.x + destRect.w, destRect.y + destRect.h,
            255, 255, 255, 255
        );
        
        // Draw direction indicator
        SDL_Point center = worldToScreen(position.x, position.y);
        SDL_Point normal = {
            static_cast<int>(center.x + 20.0f * sin(angle)),
            static_cast<int>(center.y - 20.0f * cos(angle))
        };
        
        lineRGBA(
            sdlRenderer,
            center.x, center.y,
            normal.x, normal.y,
            255, 255, 0, 255
        );
    }
}

void Renderer::renderBackground() {
    // Simple background: just fill with a dark color
    SDL_SetRenderDrawColor(sdlRenderer, 20, 20, 40, 255);
    SDL_RenderClear(sdlRenderer);
    
    // Grid lines for visual reference
    SDL_SetRenderDrawColor(sdlRenderer, 50, 50, 70, 255);
    
    // Draw vertical grid lines
    for (int x = -100; x <= 100; x += 5) {
        SDL_Point start = worldToScreen(x, -100);
        SDL_Point end = worldToScreen(x, 100);
        SDL_RenderDrawLine(sdlRenderer, start.x, start.y, end.x, end.y);
    }
    
    // Draw horizontal grid lines
    for (int y = -100; y <= 100; y += 5) {
        SDL_Point start = worldToScreen(-100, y);
        SDL_Point end = worldToScreen(100, y);
        SDL_RenderDrawLine(sdlRenderer, start.x, start.y, end.x, end.y);
    }
    
    // Draw coordinate axes
    SDL_SetRenderDrawColor(sdlRenderer, 100, 100, 200, 255);
    
    // X-axis
    SDL_Point xStart = worldToScreen(-100, 0);
    SDL_Point xEnd = worldToScreen(100, 0);
    SDL_RenderDrawLine(sdlRenderer, xStart.x, xStart.y, xEnd.x, xEnd.y);
    
    // Y-axis
    SDL_Point yStart = worldToScreen(0, -100);
    SDL_Point yEnd = worldToScreen(0, 100);
    SDL_RenderDrawLine(sdlRenderer, yStart.x, yStart.y, yEnd.x, yEnd.y);
}

void Renderer::renderDebugInfo() {
    // Draw camera info
    std::stringstream ss;
    ss << "Camera: (" << cameraX << ", " << cameraY << ") Zoom: " << cameraZoom;
    
    // Use SDL2_gfx to render text
    stringRGBA(
        sdlRenderer,
        10, 10, // Position
        ss.str().c_str(),
        255, 255, 255, 255
    );
    
    // Draw object counts if we have the object manager
    if (game && game->getObjectManager()) {
        ObjectManager* objectManager = game->getObjectManager();
        
        ss.str("");
        ss << "Objects: " << objectManager->getDynamicObjects().size()
           << " Portals: " << objectManager->getPortals().size();
        
        stringRGBA(
            sdlRenderer,
            10, 30, // Position
            ss.str().c_str(),
            255, 255, 255, 255
        );
    }
    
    // Draw physics debug info if we have the physics engine
    if (game && game->getPhysicsEngine()) {
        PhysicsEngine* physicsEngine = game->getPhysicsEngine();
        
        ss.str("");
        ss << "Gravity: " << (physicsEngine->isGravityEnabled() ? "ON" : "OFF");
        
        stringRGBA(
            sdlRenderer,
            10, 50, // Position
            ss.str().c_str(),
            255, 255, 255, 255
        );
    }
}

void Renderer::setCameraPosition(float x, float y) {
    cameraX = x;
    cameraY = y;
}

void Renderer::setCameraZoom(float zoom) {
    if (zoom > 0.1f) {  // Prevent zoom from getting too small
        cameraZoom = zoom;
    }
}

void Renderer::moveCamera(float dx, float dy) {
    cameraX += dx;
    cameraY += dy;
}

void Renderer::zoomCamera(float factor) {
    setCameraZoom(cameraZoom * factor);
}

bool Renderer::loadTexture(const std::string& name, const std::string& filepath) {
    if (!textureManager) {
        LOG_ERROR("Cannot load texture, texture manager not initialized");
        return false;
    }
    
    return textureManager->loadTexture(name, filepath);
}

void Renderer::unloadTexture(const std::string& name) {
    if (textureManager) {
        textureManager->unloadTexture(name);
    }
}

void Renderer::toggleDebugDraw() {
    debugDrawEnabled = !debugDrawEnabled;
    LOG_DEBUG("Debug drawing " + std::string(debugDrawEnabled ? "enabled" : "disabled"));
}

bool Renderer::isDebugDrawEnabled() const {
    // Always enabled for now
    return true;
}

TextureManager* Renderer::getTextureManager() const {
    return textureManager.get();
}

PortalRenderer* Renderer::getPortalRenderer() const {
    return portalRenderer.get();
}

SDL_Renderer* Renderer::getSDLRenderer() const {
    return sdlRenderer;
}
