from mss.linux import MSS as mss
from mss import tools
from pynput import keyboard as KeyboardController
import numpy as np


class GameHandle:
    """Provide access to the game's screen"""
    def __init__(self):
        """Set regions for important screen data"""
        self.keyboard = KeyboardController.Controller()

        self.screen = mss(":0")
        self.monitor = {'top': 0, 'left': 0, 'width': 1920, 'height': 1080}
        self.game_area = {'top': 35, 'left': 35, 'width': 380, 'height': 450}
        self.score_area = {'top': 86, 'left': 500, 'width': 14, 'height': 15}
        #TODO Add individual boxes instances for score, bombs, lives, game area 

    def CaptureScreen(self, area):
        """Capture one of the preset areas of the screen."""
        screenshot = self.screen.grab(area)
        img = np.array(screenshot, dtype=np.uint8)
        return img

    def CaptureScore(self):
        """Capture every digit from the score area individually."""
        digits = [] #Unprocessed images of each digit, starting from the left.
        digit_area = dict(self.score_area)
        for i in range(9):
            digits.append(self.CaptureScreen(digit_area))
            digit_area['left'] += 14
            print(digit_area['left'])
        return digits
