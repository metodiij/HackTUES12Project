import cv2
from picamera2 import Picamera2

# 1. Initialize the camera
picam2 = Picamera2()

# 2. Configure for OpenCV (BGR format at 640x480 resolution)
config = picam2.create_preview_configuration(main={"format": "BGR888", "size": (640, 480)})
picam2.configure(config)

# 3. Start the camera
picam2.start()

print("Camera window opened. Press 'q' on your keyboard to exit.")

try:
    while True:
        # 4. Capture a frame as a numpy array (compatible with OpenCV)
        frame = picam2.capture_array()

        # 5. Show the window
        cv2.imshow('HackTUES12 Camera Feed', frame)

        # Stop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    # 6. Clean up properly
    picam2.stop()
    cv2.destroyAllWindows()