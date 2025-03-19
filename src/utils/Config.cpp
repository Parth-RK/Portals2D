#include "Config.h"
#include "Logger.h"
#include <fstream>
#include <sstream>

Config* Config::instance = nullptr;

Config::Config() {
    loadDefaultConfig();
}

Config* Config::getInstance() {
    if (instance == nullptr) {
        instance = new Config();
    }
    return instance;
}

void Config::loadDefaultConfig() {
    // Window settings
    setInt("window_width", 800);
    setInt("window_height", 600);
    setString("window_title", "2D Portals Game");
    setBool("fullscreen", false);
    
    // Physics settings
    setFloat("physics_gravity_x", 0.0f);
    setFloat("physics_gravity_y", 9.8f);
    setFloat("physics_time_step", 1.0f / 60.0f);
    setInt("physics_velocity_iterations", 8);
    setInt("physics_position_iterations", 3);
    
    // Portal settings
    setFloat("portal_width", 1.0f);
    setFloat("portal_height", 2.0f);
    setInt("max_portals", 2);
    
    // Game objects
    setInt("max_dynamic_objects", 100);
    
    LOG_INFO("Default configuration loaded");
}

void Config::loadFromFile(const std::string& filename) {
    std::ifstream file(filename);
    if (!file.is_open()) {
        LOG_WARNING("Could not open config file: " + filename);
        return;
    }
    
    std::string line;
    while (std::getline(file, line)) {
        std::istringstream is_line(line);
        std::string key;
        
        if (std::getline(is_line, key, '=')) {
            std::string value;
            if (std::getline(is_line, value)) {
                // Determine type and store
                if (key.substr(0, 3) == "int") {
                    setInt(key.substr(4), std::stoi(value));
                } 
                else if (key.substr(0, 5) == "float") {
                    setFloat(key.substr(6), std::stof(value));
                }
                else if (key.substr(0, 4) == "bool") {
                    setBool(key.substr(5), (value == "true" || value == "1"));
                }
                else {
                    setString(key, value);
                }
            }
        }
    }
    
    LOG_INFO("Configuration loaded from " + filename);
}

void Config::saveToFile(const std::string& filename) {
    std::ofstream file(filename);
    if (!file.is_open()) {
        LOG_ERROR("Could not write to config file: " + filename);
        return;
    }
    
    // Write string configs
    for (const auto& pair : stringConfig) {
        file << "str_" << pair.first << "=" << pair.second << std::endl;
    }
    
    // Write int configs
    for (const auto& pair : intConfig) {
        file << "int_" << pair.first << "=" << pair.second << std::endl;
    }
    
    // Write float configs
    for (const auto& pair : floatConfig) {
        file << "float_" << pair.first << "=" << pair.second << std::endl;
    }
    
    // Write bool configs
    for (const auto& pair : boolConfig) {
        file << "bool_" << pair.first << "=" << (pair.second ? "true" : "false") << std::endl;
    }
    
    LOG_INFO("Configuration saved to " + filename);
}

std::string Config::getString(const std::string& key, const std::string& defaultValue) {
    if (stringConfig.find(key) != stringConfig.end()) {
        return stringConfig[key];
    }
    return defaultValue;
}

int Config::getInt(const std::string& key, int defaultValue) {
    if (intConfig.find(key) != intConfig.end()) {
        return intConfig[key];
    }
    return defaultValue;
}

float Config::getFloat(const std::string& key, float defaultValue) {
    if (floatConfig.find(key) != floatConfig.end()) {
        return floatConfig[key];
    }
    return defaultValue;
}

bool Config::getBool(const std::string& key, bool defaultValue) {
    if (boolConfig.find(key) != boolConfig.end()) {
        return boolConfig[key];
    }
    return defaultValue;
}

void Config::setString(const std::string& key, const std::string& value) {
    stringConfig[key] = value;
}

void Config::setInt(const std::string& key, int value) {
    intConfig[key] = value;
}

void Config::setFloat(const std::string& key, float value) {
    floatConfig[key] = value;
}

void Config::setBool(const std::string& key, bool value) {
    boolConfig[key] = value;
}
