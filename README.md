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

## Usage

Currently on windows only
```
Double click Portals2D.exe
```

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
Create a virtual environment
```bash
python -m venv venv
```
Activate the virtual environment
```bash
# On Windows:
venv\Scripts\activate
```
```bash
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

### 5. Compile the Executable
```bash
pip install nuitka #if not already installed
```
```bash
nuitka --standalone --onefile --windows-console-mode=disable main.py
```

### 6. Sign it personally
```bash
$cert = New-SelfSignedCertificate -Type CodeSigning -Subject "Portals2D" -CertStoreLocation "Cert:\CurrentUser\My" -HashAlgorithm sha256
```
```bash
$pwd = ConvertTo-SecureString -String "Password" -Force -AsPlainText 
```
```bash
Export-PfxCertificate -cert $cert -FilePath Portals2D.pfx -Password $pwd
```
```bash
signtool.exe sign /f Portals2D.pfx /fd SHA256 /p Password Portals2D.exe
```
```bash
signtool timestamp /tr http://timestamp.digicert.com /td SHA256 Portals2D.exe
```
Last step, Install certificate
```
Portals.exe > Properties > Digital Signature > Portals2D Details > View Certificate > Install Certificate > Yes *(to all)
```
## How to Play

### Controls
- **ESC**: Quit game
- **G**: Toggle gravity on/off
- **B**: Create a box at cursor position
- **C**: Create a circle at cursor position
- **D**: Debug Stats
- **Left Click**: Grab and drag objects
- **Release Left Click**: Throw the object
- **Right Click**: click on object/portal to delete it 

### Gameplay
1. Create objects using the B and C keys.
2. Objects will teleport between linked portals, conserving momentum.
3. Drag objects with the left mouse button and throw them by releasing.
4. Right-click on objects to delete them.

## Project Structure
```
Portals2D/
├── docs/               # Documentation
├── game.py             # Main game class orchestrating the game loop
├── input.py            # Handles user input and events
├── objects.py          # Game object definitions
├── physics.py          # Physics engine integration
├── portals.py          # Portal mechanics and teleportation logic
├── renderer.py         # Rendering components
├── settings.py         # Configuration and constants
├── ui.py               # User interface components
├── utils.py            # Utility functions and classes
├── main.py             # Game entry point
├── requirements.txt    # Project dependencies
└── LICENSE             # License file
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

## Documentation for 2D Portals Game

The "docs" folder contains detailed documentation for the 2D Portals Game project. Below is an index of the available documentation files:

- [Gameplay](docs/gameplay.md): Instructions on how to play the game.
- [Technical Details](docs/technical.md): In-depth details about the implementation.
- [Code Structure](docs/core_systems.md): Functionalities and their purpose
