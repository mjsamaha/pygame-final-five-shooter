# load images, audio...
import os
import pygame


class AssetLoader:
    @staticmethod
    def get_asset_path(filename, subfolder=None):
        # Get the path to the assets directory (one level up from src)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        assets_path = os.path.join(project_root, 'assets')

        if subfolder:
            assets_path = os.path.join(assets_path, subfolder)

        return os.path.join(assets_path, filename)

    @staticmethod
    def load_image(filename, size=None):
        """Load an image and optionally resize it"""
        try:
            image = pygame.image.load(AssetLoader.get_asset_path(filename, 'images')).convert_alpha()
            if size:
                return pygame.transform.scale(image, (size, size))
            return image
        except (pygame.error, FileNotFoundError) as e:
            print(f"Error loading image {filename}: {e}")
            # Create a default surface with magenta color to make missing textures obvious
            surface = pygame.Surface((size or 32, size or 32))
            surface.fill((255, 0, 255))  # Magenta color
            return surface