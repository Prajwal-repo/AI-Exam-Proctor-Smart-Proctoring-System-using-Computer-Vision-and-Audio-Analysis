from ultralytics import YOLO
from PIL import Image
import cv2

model = YOLO("yolov8n.pt")

def detect_objects(frame):
    # Convert OpenCV BGR frame to RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # Convert NumPy array to PIL Image
    image = Image.fromarray(frame_rgb)
    
    # Perform detection
    results = model(image, verbose=False)[0]

    detected_labels = []
    for box in results.boxes:
        cls_id = int(box.cls[0])
        label = model.names[cls_id]
        if label in ['cell phone', 'book', 'laptop']:
            detected_labels.append(label)

    return detected_labels
