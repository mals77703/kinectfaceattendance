# -------------------------------------------------------------

from pylibfreenect2 import Freenect2, SyncMultiFrameListener, FrameType
import cv2
import numpy as np

# ---------- 1. Initialise Kinect ----------
fn = Freenect2()
num_devices = fn.enumerateDevices()
if num_devices == 0:
    raise RuntimeError("No Kinect v2 detected. Check USB & power.")
dev = fn.openDefaultDevice()

# We only need the color (RGB) stream for face encodings
listener = SyncMultiFrameListener(FrameType.Color)
dev.setColorFrameListener(listener)
dev.start()
print("Kinect RGB stream started. Press S to save a photo, ESC to quit.")

# ---------- 2. Main loop ----------
while True:
    frames = listener.waitForNewFrame()
    color = frames["color"]                        # BGRA 1920×1080
    img   = color.asarray()
    bgr   = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)  # Convert to OpenCV BGR

    cv2.imshow("Kinect RGB (press S to save)", bgr)

    key = cv2.waitKey(1) & 0xFF
    if key == 27:            # ESC key
        break
    elif key == ord('s'):    # S key
        cv2.imwrite("malu.jpg", bgr)
        print("Saved malu.jpg ✔")

    listener.release(frames)

# ---------- 3. Clean‑up ----------
dev.stop()
dev.close()
cv2.destroyAllWindows()
print("Kinect closed. Bye!")
