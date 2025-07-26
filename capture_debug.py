# capture_debug.py
from pylibfreenect2 import Freenect2, SyncMultiFrameListener, FrameType
import cv2, os, numpy as np, datetime

fn = Freenect2()
dev = fn.openDefaultDevice()
listener = SyncMultiFrameListener(FrameType.Color)
dev.setColorFrameListener(listener)
dev.start()

save_path = os.path.expanduser("~/employee.jpg")
print("LIVE -- click the window, press S to save, ESC to quit")

while True:
    frames = listener.waitForNewFrame()
    color  = frames["color"]
    img    = color.asarray()
    bgr    = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

    cv2.imshow("Kinect RGB (diagnostic)", bgr)
    key = cv2.waitKey(1) & 0xFF         # catch every key

    if key != 255:                      # 255 == no key pressed
        print(f"Key pressed: {key}")

    if key == 27:                       # ESC
        break
    elif key in [ord('s'), ord('S')]:   # lower‑ or uppercase S
        ok = cv2.imwrite(save_path, bgr)
        print("Attempting save to:", save_path, "Success:", ok)

    listener.release(frames)

dev.stop(); dev.close()
cv2.destroyAllWindows()
