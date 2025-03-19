# 2D Portals Game

## Overview
A 2D physics-based game inspired by the portal mechanics from Valve's Portal games. This implementation uses Python with Pygame for rendering and PyBox2D for physics simulation, enabling realistic portal teleportation with momentum conservation.

## Features
- Realistic 2D physics simulation
- Portal creation and teleportation
- Momentum conservation through portals
- Dynamic object creation
- Toggleable gravity
- Object manipulation (dragging, throwing, resizing)

## Requirements
- Python 3.8+
- Dependencies listed in requirements.txt

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/Parth-RK/Portals2D.git
cd Portals2D
```

### 2. Set Up a Virtual Environment (recommended)
```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Game
```bash
python main.py
```

## How to Play

### Controls
- **ESC**: Quit game
- **G**: Toggle gravity on/off
- **B**: Create a box at cursor position
- **C**: Create a circle at cursor position
- **P**: Create portals (press twice to create a pair)
- **Left Click**: Grab and drag objects
- **Release Left Click**: Throw the object
- **Right Click**: Open object properties menu (resize, rotate)

### Gameplay
1. Create objects using the B and C keys.
2. Place portals on surfaces using the P key (press twice for a pair).
3. Objects will teleport between linked portals, conserving momentum.
4. Drag objects with the left mouse button and throw them by releasing.
5. Right-click on objects to resize or rotate them.

## Project Structure
```
Portals2D/
├── docs/               # Documentation
├── logs/               # Game logs (created during runtime)
├── src/                # Source code
│   ├── core/           # Core game components
│   ├── game_objects/   # Game object definitions
│   ├── physics/        # Physics engine integration
│   ├── rendering/      # Rendering components
│   ├── ui/             # User interface components
│   └── utils/          # Utility functions and classes
├── main.py             # Game entry point
└── requirements.txt    # Project dependencies
```

## Implementation Details

### Portal Mechanics
The game implements true portal mechanics where:
- Objects maintain momentum when passing through portals.
- The exit velocity is calculated based on the orientation of both portals.
- Objects can partially enter portals, appearing gradually on the other side.

### Physics
- Built on PyBox2D for accurate physics simulation.
- Uses collision detection for portal interactions.
- Implements gravity and other physical forces.

### Rendering
- Uses Pygame for efficient 2D rendering.
- Object rotation and portal effects are handled through surface transformations.

## Development
This project is structured with modularity in mind, making it easy to extend with new features:
- Add new object types in the `game_objects` module.
- Extend physics functionality in the `physics` module.
- Add visual effects in the `rendering` module.

## License
[Specify your license here]
