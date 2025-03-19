#pragma once

#include <SDL2/SDL.h>
#include <memory>

class Game;

class GameLoop {
private:
    Game* game;
    bool running;
    
    // Timing variables
    Uint32 lastFrameTime;
    float deltaTime;
    float timeAccumulator;
    float fixedTimeStep;
    
    // Performance monitoring
    int frameCount;
    float frameCountTimer;
    int fps;
    
    void calculateDeltaTime();
    void processInput();
    void update();
    void render();
    void limitFPS(int targetFPS = 60);
    
public:
    GameLoop(Game* gameInstance);
    ~GameLoop();
    
    void start();
    void stop();
    
    float getDeltaTime() const;
    int getFPS() const;
};
