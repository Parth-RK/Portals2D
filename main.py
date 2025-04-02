import sys
import os
import traceback # Import traceback for detailed error reporting

# --- Path Setup ---
# Ensures the 'portals2d' package directory and its parent are in the Python path
# This helps when running the script directly or as a module.
try:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    package_dir = script_dir # Assuming main.py is inside portals2d
    parent_dir = os.path.abspath(os.path.join(package_dir, '..'))

    # Add parent directory for potential imports like 'import portals2d'
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)
    # Add package directory itself for relative imports if needed (less common for main)
    # if package_dir not in sys.path:
    #    sys.path.insert(0, package_dir)

except Exception as e:
    print(f"Warning: Error during path setup - {e}")
    # Continue anyway, hoping Python finds the modules

# --- Import Game Class ---
try:
    # Attempt to import using package structure (preferred)
    from game import Game
except ImportError:
    # Fallback if running script directly inside portals2d dir without package install
    try:
        from game import Game
    except ImportError as e:
        print("FATAL ERROR: Could not import the Game class.")
        print("Ensure 'game.py' exists and the script is run correctly.")
        print(f"Python Path: {sys.path}")
        print(f"Import Error: {e}")
        sys.exit(1)
except Exception as e:
    print(f"FATAL ERROR: An unexpected error occurred importing Game class: {e}")
    traceback.print_exc()
    sys.exit(1)


# --- Main Execution Guard ---
if __name__ == '__main__':
    print("-" * 30)
    print(" Starting Portals2D ")
    print("-" * 30)

    # --- Basic Dependency Check ---
    dependencies_ok = True
    try:
        import pygame
        print(f"Pygame version: {pygame.ver}")
    except ImportError:
        print("ERROR: Pygame not found. Please install it (e.g., 'pip install pygame')")
        dependencies_ok = False

    try:
        # Just check if Box2D can be imported
        import Box2D
        # Box2D doesn't have a standard easy way to get version string here
        print("Box2D imported successfully.")
    except ImportError:
        print("ERROR: Box2D-py not found. Please install it (e.g., 'pip install Box2D-py')")
        dependencies_ok = False

    if not dependencies_ok:
        print("Please install missing dependencies and try again.")
        sys.exit(1)

    # --- Run the Game ---
    main_game = None # Initialize to None
    try:
        # Instantiate the main game class
        main_game = Game()
        # Run the game loop (blocking call until game exits)
        main_game.run()

    except Exception as e:
        # Catch any unexpected errors during game initialization or runtime
        print("\n" + "="*50)
        print(" FATAL RUNTIME ERROR ")
        print("="*50)
        print(f"An unexpected error occurred: {e}")
        print("-" * 50)
        # Print the full traceback for debugging
        traceback.print_exc()
        print("="*50)
        # Attempt graceful cleanup if game object exists
        if main_game and hasattr(main_game, 'cleanup'):
             print("Attempting cleanup despite error...")
             try:
                  main_game.cleanup()
             except Exception as cleanup_e:
                  print(f"Error during cleanup after runtime error: {cleanup_e}")
        else:
             # Force quit Pygame if cleanup wasn't possible
             pygame.quit()
        sys.exit(1) # Exit with error status

    # --- Normal Exit ---
    # If main_game.run() completes without error, cleanup is called inside it.
    print("Application finished normally.")
    sys.exit(0) # Exit with success status