#include "TextureManager.h"
#include "../utils/Logger.h"
#include <SDL2/SDL_image.h>

TextureManager::TextureManager(SDL_Renderer* renderer) : renderer(renderer) {
    // Initialize SDL_image
    int imgFlags = IMG_INIT_PNG | IMG_INIT_JPG;
    if (!(IMG_Init(imgFlags) & imgFlags)) {
        LOG_ERROR("SDL_image could not initialize! SDL_image Error: " + std::string(IMG_GetError()));
    } else {
        LOG_INFO("TextureManager initialized with SDL_image");
    }
}

TextureManager::~TextureManager() {
    unloadAllTextures();
    IMG_Quit();
    LOG_INFO("TextureManager destroyed");
}

bool TextureManager::loadTexture(const std::string& name, const std::string& filepath) {
    // Check if texture already exists
    if (hasTexture(name)) {
        LOG_WARNING("Texture with name '" + name + "' already exists, replacing");
        unloadTexture(name);
    }
    
    // Load the image
    SDL_Surface* surface = loadSurface(filepath);
    if (!surface) {
        LOG_ERROR("Failed to load image: " + filepath);
        return false;
    }
    
    // Create texture
    SDL_Texture* texture = createTextureFromSurface(surface);
    
    // Free the surface
    SDL_FreeSurface(surface);
    
    if (!texture) {
        LOG_ERROR("Failed to create texture from " + filepath);
        return false;
    }
    
    // Store the texture
    textures[name] = texture;
    LOG_DEBUG("Loaded texture '" + name + "' from " + filepath);
    return true;
}

void TextureManager::unloadTexture(const std::string& name) {
    auto it = textures.find(name);
    if (it != textures.end()) {
        SDL_DestroyTexture(it->second);
        textures.erase(it);
        LOG_DEBUG("Unloaded texture '" + name + "'");
    }
}

void TextureManager::unloadAllTextures() {
    for (auto& pair : textures) {
        SDL_DestroyTexture(pair.second);
    }
    textures.clear();
    LOG_DEBUG("All textures unloaded");
}

SDL_Texture* TextureManager::getTexture(const std::string& name) const {
    auto it = textures.find(name);
    if (it != textures.end()) {
        return it->second;
    }
    LOG_WARNING("Texture '" + name + "' not found");
    return nullptr;
}

bool TextureManager::hasTexture(const std::string& name) const {
    return textures.find(name) != textures.end();
}

SDL_Surface* TextureManager::loadSurface(const std::string& filepath) {
    // Load image using SDL_image
    SDL_Surface* surface = IMG_Load(filepath.c_str());
    
    if (!surface) {
        LOG_ERROR("Unable to load image " + filepath + "! SDL_image Error: " + IMG_GetError());
        return nullptr;
    }
    
    return surface;
}

SDL_Texture* TextureManager::createTextureFromSurface(SDL_Surface* surface) {
    if (!surface) {
        LOG_ERROR("Cannot create texture from null surface");
        return nullptr;
    }
    
    SDL_Texture* texture = SDL_CreateTextureFromSurface(renderer, surface);
    if (!texture) {
        LOG_ERROR("Unable to create texture! SDL Error: " + std::string(SDL_GetError()));
    }
    
    return texture;
}
