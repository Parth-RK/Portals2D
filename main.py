import pygame
import sys
from src.core.game_loop import GameLoop
from src.utils.logger import Logger

def main():
    """Main entry point for the 2D Portals Game."""
    # Initialize logger
    logger = Logger()
    logger.info("Starting 2D Portals Game")
    
    # Initialize pygame
    pygame.init()
    
    # Initialize the game loop
    game_loop = GameLoop()
    
    try:
        # Start the game
        game_loop.run()
    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")
    finally:
        # Clean up
        pygame.quit()
        logger.info("Game terminated")
        sys.exit()

if __name__ == "__main__":
    main()
