#pragma once

#include <string>
#include <map>

class Config {
private:
    static Config* instance;
    std::map<std::string, std::string> stringConfig;
    std::map<std::string, int> intConfig;
    std::map<std::string, float> floatConfig;
    std::map<std::string, bool> boolConfig;
    
    Config();
    
public:
    static Config* getInstance();
    
    void loadFromFile(const std::string& filename);
    void saveToFile(const std::string& filename);
    
    // Getters
    std::string getString(const std::string& key, const std::string& defaultValue = "");
    int getInt(const std::string& key, int defaultValue = 0);
    float getFloat(const std::string& key, float defaultValue = 0.0f);
    bool getBool(const std::string& key, bool defaultValue = false);
    
    // Setters
    void setString(const std::string& key, const std::string& value);
    void setInt(const std::string& key, int value);
    void setFloat(const std::string& key, float value);
    void setBool(const std::string& key, bool value);
    
    // Default game settings
    void loadDefaultConfig();
};
