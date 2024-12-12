import torch 
import cv2 
from ultralytics import YOLO
import time


# load the best model
best_model = YOLO("/home/mohsin/detection/best.pt") # change this to point to your best saved model weights

# dynamically retrieve class names from the model
if hasattr(best_model, 'names'):
    class_names = best_model.names
else:
    raise ValueError("Model does not have attribute 'names'.")

# initialize webcam
cap = cv2.VideoCapture(0)  # Default webcam
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

# function to draw bounding boxes, labels, and FPS on the frame
def draw_predictions(frame, results, fps):
    for result in results:  # Process each detected object
        boxes = result.boxes
        for box in boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])  # Get bounding box coordinates
            conf = box.conf[0].item()  # Confidence score
            cls = int(box.cls[0].item())  # Class index

            # Skip if class index is invalid
            if cls >= len(class_names):
                print(f"Warning: Class index {cls} is out of range.")
                continue

            class_name = class_names[cls]
            label = f"{class_name} ({conf:.2f})"

            # draw the bounding box
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

            # draw the label
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    # draw FPS on the frame
    fps_text = f"FPS: {fps:.2f}"
    cv2.putText(frame, fps_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
    return frame

# configure OpenCV window for full-screen display
cv2.namedWindow("YOLO Inference", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("YOLO Inference", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

# inference loop
prev_time = time.time()  # Initialize timer
while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        break

    # calculate the time taken for processing
    current_time = time.time()
    fps = 1 / (current_time - prev_time)
    prev_time = current_time

    # perform inference
    results = best_model.predict(frame, imgsz=416, conf=0.25) # default train img size 416, try 320, 224 .....

    # draw predictions on the frame along with FPS
    frame_with_predictions = draw_predictions(frame, results, fps)

    # display the frame in full screen
    cv2.imshow("YOLO Inference", frame_with_predictions)

    # break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# release resources
cap.release()
cv2.destroyAllWindows()
