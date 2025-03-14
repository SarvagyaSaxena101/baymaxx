import cv2
import subprocess
import numpy as np

# Start libcamera-vid as a subprocess to capture video
command = [
    "libcamera-vid", "-t", "0", "--width", "640", "--height", "480", "--framerate", "30",
    "--codec", "mjpeg", "-o", "-", "--inline"
]

# Create the process with appropriate pipe configuration
process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=10**8)

# Give the camera a moment to initialize
import time
time.sleep(1)

# Create a VideoCapture object that reads from process.stdout
cap = cv2.VideoCapture()
cap.open("pipe:" + str(process.stdout.fileno()), cv2.CAP_FFMPEG)

# Check if camera opened successfully
if not cap.isOpened():
    print("Error: Could not open video stream")
    process.terminate()
    exit()

# Read the first frame
ret, frame = cap.read()
if not ret:
    print("Error: Couldn't read first frame from camera")
    cap.release()
    process.terminate()
    exit()

# Initialize tracking box (you can modify this manually)
bbox = (100, 100, 100, 100)

# Initialize KCF Tracker
tracker = cv2.legacy.TrackerKCF.create()
tracker.init(frame, bbox)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Couldn't read frame")
        break
        
    # Update tracker
    success, bbox = tracker.update(frame)
    
    if success:
        x, y, w, h = [int(v) for v in bbox]
        # Draw tracking box
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        # Check if object is out of bounds
        frame_h, frame_w = frame.shape[:2]
        status = []
        if x <= 0:
            status.append("Left")
        if x + w >= frame_w:
            status.append("Right")
        if y <= 0:
            status.append("Top")
        if y + h >= frame_h:
            status.append("Bottom")
        
        status_text = "Out from: " + ", ".join(status) if status else "Inside"
        cv2.putText(frame, status_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
    else:
        cv2.putText(frame, "Tracking failure", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
    
    # Show live feed
    cv2.imshow("Pi Camera Object Tracking", frame)
    
    # Exit on 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Clean up
cap.release()
cv2.destroyAllWindows()
process.terminate()
