#pragma once

#include <SDL2/SDL.h>
#include <memory>
#include <vector>

class Renderer;
class Portal;
class GameEntity;

// Class for handling the special rendering of portals
class PortalRenderer {
private:
    Renderer* mainRenderer;
    bool useStencilBuffer;
    
    // Stencil buffer for portal rendering
    SDL_Texture* portalTexture;
    
    // Helper methods
    void renderPortalView(Portal* portal, std::shared_ptr<Portal> linkedPortal);
    void renderPortalFrame(Portal* portal);
    void renderPortalDebug(Portal* portal);
    
public:
    PortalRenderer(Renderer* renderer);
    ~PortalRenderer();
    
    void initialize();
    
    // Main rendering method
    void renderPortal(Portal* portal);
    
    // Partial object rendering
    void renderEntityInPortal(GameEntity* entity, Portal* entryPortal, Portal* exitPortal);
    
    // Stencil buffer toggle
    void enableStencilBuffer(bool enable);
    bool isStencilBufferEnabled() const;
};
