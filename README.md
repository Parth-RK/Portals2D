# 2D Portals Game

A lightweight 2D physics-based game with portals, optimized for low-spec hardware.

## Features

- Dynamic object creation and deletion
- Adjustable object and portal sizes
- Realistic physics with Box2D
- Portal teleportation with momentum conservation
- Gravity toggle
- Simple UI for game controls

## Requirements

- C++ compiler with C++11 support
- SDL2
- Box2D
- Dear ImGui (optional)

## Building the Project

```bash
mkdir build
cd build
cmake ..
make
```

## Directory Structure

- `src/`: Source code
  - `core/`: Core game systems
  - `entities/`: Game object definitions
  - `physics/`: Physics implementation
  - `rendering/`: Rendering code
  - `ui/`: User interface code
  - `utils/`: Utility functions and classes
- `include/`: External headers
- `lib/`: External libraries
- `assets/`: Game assets
- `tests/`: Test code
- `docs/`: Documentation
- `tools/`: Helper scripts and tools

## License

[Your license information here]
