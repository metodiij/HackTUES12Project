import cv2
from picamera2 import Picamera2
from ultralytics import YOLO

# 1. Load your self-trained model
# Replace 'best.pt' with the actual path to your trained model file
model = YOLO('yolo11n_selftrained.pt')

# 2. Initialize and configure Picamera2
picam2 = Picamera2()
config = picam2.create_preview_configuration(main={"format": "BGR888", "size": (640, 480)})
picam2.configure(config)
picam2.start()

print("YOLO Model Loaded. Camera window opened. Press 'q' to exit.")

try:
    while True:
        # 3. Capture a frame
        frame = picam2.capture_array()

        # 4. Run YOLO inference on the frame
        # stream=True is more memory efficient for video
        results = model(frame, stream=True, conf=0.5) 

        # 5. Visualize the results on the frame
        for r in results:
            annotated_frame = r.plot() # This draws the boxes and labels

        # 6. Show the window
        cv2.imshow('YOLOv8 Detection', annotated_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    picam2.stop()
    cv2.destroyAllWindows()