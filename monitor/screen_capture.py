import pyautogui
import cv2
import numpy as np

def capture_screen():
    img = pyautogui.screenshot()
    return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

def blur_regions(img, regions):
    result = img.copy()
    for (x, y, w, h) in regions:
        result[y:y+h, x:x+w] = cv2.GaussianBlur(result[y:y+h, x:x+w], (99, 99), 0)
    return result

def save_blurred_screen(img, regions):
    blurred = blur_regions(img, regions)
    cv2.imwrite("blurred_sensitive_data.png", blurred)
