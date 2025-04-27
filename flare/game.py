import pygame,flare.scene

class AssetLoader:
    def __init__(self):
        self.AssetsToLoad = []

class Game:
    def __init__(self):
        self.manager = flare.scene.SceneManager()
        self.assets = {}
        self.assetsToLoad = AssetLoader()