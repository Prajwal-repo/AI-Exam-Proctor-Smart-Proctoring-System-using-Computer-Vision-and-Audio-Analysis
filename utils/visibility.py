import cv2

def is_dark(frame, threshold=40):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return gray.mean() < threshold
