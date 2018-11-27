"""Simple and fast functions to process visual data from the game"""
import cv2
import numpy as np


def DenoiseDigit(digit):
    """Remove the non-white pixels of a digit capture"""
    return cv2.inRange(digit, (130, 130, 130, 0), (255, 255, 255, 255))

def LoadFilters():
    """Load static digit filters from disk"""
    filters = []
    for i in range(0, 10):
        filters.append(cv2.cvtColor(cv2.imread("filters/filter" + str(i) + ".jpg"), cv2.COLOR_BGR2GRAY))
    return filters

def ClassifyDigit(digit, filters=LoadFilters()):
    """Compare the intersection of the digit and each of the static filters."""
    digit = DenoiseDigit(digit)
    scores = []
    for filt in filters:
        intersection = np.count_nonzero(np.bitwise_and(digit, filt))
        scores.append(intersection)
    print(scores)
    return scores.index(max(scores))

def ReadScore(digits):
    """Classify a list of digits and return a total score"""
    score = ""
    for digit in digits:
        score += str(ClassifyDigit(digit))
    return int(score)

def DenoiseLives(lives_box):
    """Remove non-red pixels of a lives region capture"""
    return cv2.inRange(lives_box, (0, 0, 130, 0), (255, 255, 255, 255))

def DenoiseBombs(bombs_box):
    """Remove non-red pixels of a bombs region capture"""
    return cv2.inRange(bombs_box, (130, 0, 0, 0), (255, 255, 255, 255))

def CountStars(region):
    """Count star shapes in a region"""
    area = np.count_nonzero(region)
    return int(area/46)
