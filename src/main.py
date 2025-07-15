# entry point
from core.game import Game
import traceback
import sys
import time

def main():
    try:
        game = Game()
        game.run()
    except Exception as e:
        print("\nAn error occurred:")
        print(traceback.format_exc())
        print("\nPress Enter to exit...")
        input()  # Wait for user input before closing
        sys.exit(1)

if __name__ == "__main__":
    main()