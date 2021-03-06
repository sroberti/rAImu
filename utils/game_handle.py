from mss.linux import MSS as mss
from mss import tools
from pynput import keyboard as kb
import subprocess
import numpy as np
import image_proc



class GameHandle:
    """Provide access to the game's screen"""
    def __init__(self):
        """Set regions for important screen data"""
        self.keyboard = kb.Controller()

        win = self.GetGameWindow()

        self.screen = mss(":0")
        #self.monitor = {'top': 0, 'left': 0, 'width': 1920, 'height': 1080}
        self.game_area = {'top': win['top'] + 35, 'left': win['left'] + 35, 'width': 380, 'height': 450}
        self.score_area = {'top': win['top'] + 86, 'left': win['left'] + 500, 'width': 14, 'height': 15}
        self.lives_area = {'top': win['top'] + 121, 'left': win['left'] + 500, 'width': 150, 'height': 10}
        self.bombs_area = {'top': win['top'] + 137, 'left': win['left'] + 500, 'width': 150, 'height': 10}

        self.keystate = {'Z': 0, 'X': 0, kb.Key.shift_l: 0, kb.Key.left: 0, kb.Key.right: 0, kb.Key.up: 0,kb.Key.down: 0,}

    def GetGameWindow(self):
        """Get the coordinates for the game window."""
        pipe = subprocess.Popen('xwininfo -root -tree | grep Perfect', shell=True, stdout=subprocess.PIPE)
        with line in pipe.stdout:
            winInfo = line.split()
            corner = winInfo[-1]
            corner = corner.split('+')
            win['top'] = corner[1]
            win['left'] = corner[0]
        return win

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
        return digits

    def GetLives(self):
        """Get the number of player lives"""
        lives = self.CaptureScreen(self.lives_area)
        lives = image_proc.DenoiseLives(lives)
        lives = image_proc.CountStars(lives)
        return lives

    def GetBombs(self):
        """Get the number of player bombs"""
        bombs = self.CaptureScreen(self.bombs_area)
        bombs = image_proc.DenoiseBombs(bombs)
        bombs = image_proc.CountStars(bombs)
        return bombs

    def GetScore(self):
        """Get the player's score"""
        score = self.CaptureScore()
        score = image_proc.ReadScore(score)
        return score

    def GetState(self):
        """Capture the game's state for the current frame"""
        state = {
            'lives': self.GetLives(),
            'bombs': self.GetBombs(),
            'score': self.GetScore(),
            'game': self.CaptureScreen(self.game_area)
            }
        return state

    def UpdateKeyState(self, keystate):
        """Press or release buttons as needed"""
        for k, v in keystate:
            if v != self.keystate[k]:
                if v == 1:
                    self.keyboard.press(k)
                elif v == 0:
                    self.keyboard.release(k)
                self.keystate[k] = v





