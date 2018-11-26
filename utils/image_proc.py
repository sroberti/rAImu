"""Simple and fast functions to process visual data from the game"""
import cv2
import numpy as np


def DenoiseDigit(digit):
    """Remove the non-white pixels of a digit capture"""
    return cv2.inRange(digit, (230, 230, 230, 0), (255, 255, 255, 255))
