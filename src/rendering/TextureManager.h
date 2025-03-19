#pragma once

#include <SDL2/SDL.h>
#include <string>
#include <unordered_map>

class TextureManager {
private:
    SDL_Renderer* renderer;
    std::unordered_map<std::string, SDL_Texture*> textures;

public:
    TextureManager(SDL_Renderer* renderer);
    ~TextureManager();
    
    bool loadTexture(const std::string& name, const std::string& filepath);
    void unloadTexture(const std::string& name);
    void unloadAllTextures();
    
    SDL_Texture* getTexture(const std::string& name) const;
    bool hasTexture(const std::string& name) const;
    
    // Utility functions
    SDL_Surface* loadSurface(const std::string& filepath);
    SDL_Texture* createTextureFromSurface(SDL_Surface* surface);
};
