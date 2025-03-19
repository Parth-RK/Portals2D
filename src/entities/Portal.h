#pragma once

#include "GameEntity.h"
#include <memory>

enum class PortalColor {
    BLUE,
    ORANGE
};

class Portal : public GameEntity {
private:
    PortalColor color;
    float width;
    float height;
    std::weak_ptr<Portal> linkedPortal;
    bool isPlaced;
    
public:
    Portal(int id, PortalColor color);
    ~Portal();
    
    // Initialize with physics body as a sensor
    void initialize(b2World* world, float x, float y, float angle);
    
    // Portal properties
    PortalColor getColor() const { return color; }
    float getWidth() const { return width; }
    float getHeight() const { return height; }
    bool getIsPlaced() const { return isPlaced; }
    void setIsPlaced(bool placed) { isPlaced = placed; }
    void setSize(float width, float height);
    
    // Portal linking
    void linkTo(std::shared_ptr<Portal> otherPortal);
    std::shared_ptr<Portal> getLinkedPortal() const;
    bool hasLinkedPortal() const;
    
    // Teleportation
    bool canTeleport() const;
    void teleportEntity(GameEntity* entity);
    
    // GameEntity methods
    void update(float deltaTime) override;
    void render() override;
};
