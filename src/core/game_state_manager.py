from utils.enums import GameState
from utils.loader import AssetLoader
from config.game_configurations import GAME_CONFIG


class GameStateManager:
    def __init__(self):
        self.state = GameState.MENU

    def switch_to_menu(self):
        self.state = GameState.MENU
        AssetLoader.stop_music()
        AssetLoader.play_music(
            volume=GAME_CONFIG['audio']['music']['menu']['volume']
        )

    def switch_to_playing(self):
        self.state = GameState.PLAYING
        AssetLoader.stop_music()
        AssetLoader.load_music(GAME_CONFIG['audio']['music']['game']['path'])
        AssetLoader.play_music(
            volume=GAME_CONFIG['audio']['music']['game']['volume']
        )

    def switch_to_upgrade(self):
        self.state = GameState.UPGRADE

    def switch_to_game_over(self):
        self.state = GameState.GAME_OVER
        AssetLoader.stop_music()