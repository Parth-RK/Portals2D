#include "PortalRenderer.h"
#include "Renderer.h"
#include "../entities/Portal.h"
#include "../entities/GameEntity.h"
#include "../utils/Logger.h"
#include <SDL2/SDL2_gfxPrimitives.h>

PortalRenderer::PortalRenderer(Renderer* renderer) : 
    mainRenderer(renderer),
    useStencilBuffer(false),
    portalTexture(nullptr) {
    
    initialize();
    LOG_DEBUG("PortalRenderer created");
}

PortalRenderer::~PortalRenderer() {
    if (portalTexture) {
        SDL_DestroyTexture(portalTexture);
    }
    
    LOG_DEBUG("PortalRenderer destroyed");
}

void PortalRenderer::initialize() {
    // Check if we have access to the renderer
    if (!mainRenderer) {
        LOG_ERROR("Cannot initialize portal renderer, main renderer is null");
        return;
    }
    
    // Try to create a texture for portal rendering
    SDL_Renderer* sdlRenderer = mainRenderer->getSDLRenderer();
    if (sdlRenderer) {
        // Create a texture that we can use for rendering portals
        portalTexture = SDL_CreateTexture(
            sdlRenderer,
            SDL_PIXELFORMAT_RGBA8888,
            SDL_TEXTUREACCESS_TARGET,
            1024,  // Reasonable size for the portal view
            1024
        );
        
        if (!portalTexture) {
            LOG_ERROR("Failed to create portal texture: " + std::string(SDL_GetError()));
        } else {
            useStencilBuffer = true;
            LOG_INFO("Portal renderer initialized with render-to-texture support");
        }
    }
}

void PortalRenderer::renderPortal(Portal* portal) {
    if (!portal || !mainRenderer) {
        return;
    }
    
    // Get the linked portal
    std::shared_ptr<Portal> linkedPortal = portal->getLinkedPortal();
    
    // If portal is linked and both portals are active, render the view through the portal
    if (linkedPortal && portal->canTeleport()) {
        renderPortalView(portal, linkedPortal);
    }
    
    // Always render the portal frame
    renderPortalFrame(portal);
    
    // Debug rendering
    if (mainRenderer->isDebugDrawEnabled()) {
        renderPortalDebug(portal);
    }
}

void PortalRenderer::renderPortalView(Portal* portal, std::shared_ptr<Portal> linkedPortal) {
    // For now, this is a simplified version without actual recursive portal views
    // A true portal rendering system would need stencil buffers and render-to-texture features
    
    // In this simplified version, we'll just render a color gradient to simulate the portal effect
    SDL_Renderer* sdlRenderer = mainRenderer->getSDLRenderer();
    
    // Get portal properties
    b2Vec2 position = portal->getPosition();
    float width = portal->getWidth();
    float height = portal->getHeight();
    PortalColor color = portal->getColor();
    
    // Create a rect for the portal
    SDL_Rect portalRect = mainRenderer->worldToScreen(
        position.x, position.y, width, height
    );
    
    // Fill with a gradient based on the portal color
    if (color == PortalColor::BLUE) {
        // Blue portal gradient
        boxRGBA(
            sdlRenderer,
            portalRect.x, portalRect.y,
            portalRect.x + portalRect.w, portalRect.y + portalRect.h,
            0, 80, 200, 200  // Semi-transparent blue
        );
    } else {
        // Orange portal gradient
        boxRGBA(
            sdlRenderer,
            portalRect.x, portalRect.y,
            portalRect.x + portalRect.w, portalRect.y + portalRect.h,
            200, 80, 0, 200  // Semi-transparent orange
        );
    }
}

void PortalRenderer::renderPortalFrame(Portal* portal) {
    SDL_Renderer* sdlRenderer = mainRenderer->getSDLRenderer();
    
    // Get portal properties
    b2Vec2 position = portal->getPosition();
    float angle = portal->getAngle();
    float width = portal->getWidth();
    float height = portal->getHeight();
    PortalColor color = portal->getColor();
    
    // Get portal rect
    SDL_Rect portalRect = mainRenderer->worldToScreen(
        position.x, position.y, width, height
    );
    
    // Determine color
    Uint8 r = 0, g = 0, b = 0, a = 255;
    if (color == PortalColor::BLUE) {
        r = 0;
        g = 150;
        b = 255;
    } else {
        r = 255;
        g = 150;
        b = 0;
    }
    
    // Draw a frame around the portal
    int thickness = 3;
    rectangleRGBA(
        sdlRenderer,
        portalRect.x, portalRect.y,
        portalRect.x + portalRect.w, portalRect.y + portalRect.h,
        r, g, b, a
    );
    
    // Draw inner glow
    for (int i = 1; i < thickness; i++) {
        rectangleRGBA(
            sdlRenderer,
            portalRect.x + i, portalRect.y + i,
            portalRect.x + portalRect.w - i, portalRect.y + portalRect.h - i,
            r, g, b, a - i * 40
        );
    }
}

void PortalRenderer::renderPortalDebug(Portal* portal) {
    SDL_Renderer* sdlRenderer = mainRenderer->getSDLRenderer();
    
    // Get portal properties
    b2Vec2 position = portal->getPosition();
    float angle = portal->getAngle();
    
    // Draw portal ID and link status
    std::string portalInfo = "Portal ID: " + std::to_string(portal->getId());
    if (portal->hasLinkedPortal()) {
        portalInfo += " linked to " + std::to_string(portal->getLinkedPortal()->getId());
    } else {
        portalInfo += " (unlinked)";
    }
    
    // Convert position to screen coordinates
    SDL_Point screenPos = mainRenderer->worldToScreen(position.x, position.y);
    
    // Draw text above the portal
    stringRGBA(
        sdlRenderer,
        screenPos.x - 50, screenPos.y - 30,
        portalInfo.c_str(),
        255, 255, 255, 255
    );
    
    // Draw direction indicator for the portal
    lineRGBA(
        sdlRenderer,
        screenPos.x, screenPos.y,
        screenPos.x + 30 * cos(angle), screenPos.y + 30 * sin(angle),
        255, 255, 0, 255
    );
}

void PortalRenderer::renderEntityInPortal(GameEntity* entity, Portal* entryPortal, Portal* exitPortal) {
    // This is a complex feature that would require render-to-texture and stencil buffer support
    // For simplicity, we'll just log that this would need additional implementation
    LOG_DEBUG("renderEntityInPortal called but not fully implemented");
}

void PortalRenderer::enableStencilBuffer(bool enable) {
    useStencilBuffer = enable && portalTexture != nullptr;
}

bool PortalRenderer::isStencilBufferEnabled() const {
    return useStencilBuffer;
}
