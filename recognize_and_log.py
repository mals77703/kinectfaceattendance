"""
attendance_kinect_v2.py  –  Kinect v2 + Raspberry Pi 5
------------------------------------------------------
• Open Kinect RGB stream
• Recognise ANY face whose encoding is in encodings.pkl
• Mark 1‑hit‑per‑day attendance in attendance.db (SQLite)
• For an unknown face:
      – draws a red box + “Unknown”
      – press  N  → script asks for employee name,
        saves <name>.jpg, appends encoding to encodings.pkl,
        and immediately starts recognising that person
"""

from pylibfreenect2 import Freenect2, SyncMultiFrameListener, FrameType
import cv2, numpy as np, face_recognition, pickle, os, sqlite3, datetime, uuid, sys

# ---------- parameters ----------
TOLERANCE       = 0.45      # lower = stricter match
UNKNOWN_TIMEOUT = 60        # sec before re‑flagging same unknown
VIEW            = "--noview" not in sys.argv  # disable window if --noview

# ---------- load / init encodings ----------
ENC_FILE = "encodings.pkl"
if os.path.exists(ENC_FILE):
    enc_data = pickle.load(open(ENC_FILE, "rb"))
else:
    enc_data = []           # list of {"name": str, "encoding": np.array}
    pickle.dump(enc_data, open(ENC_FILE, "wb"))

known_enc  = [d["encoding"] for d in enc_data]
known_name = [d["name"]     for d in enc_data]
print(f"Loaded {len(known_enc)} known employee(s)")

# ---------- SQLite setup ----------
conn = sqlite3.connect("attendance.db")
cur  = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS log(
                  name TEXT,
                  date TEXT,
                  time TEXT)""")
conn.commit()

def mark_attendance(name):
    today = datetime.date.today().isoformat()
    cur.execute("SELECT 1 FROM log WHERE name=? AND date=?", (name, today))
    if cur.fetchone():             # already marked today
        return
    now = datetime.datetime.now().strftime("%H:%M:%S")
    cur.execute("INSERT INTO log VALUES (?,?,?)", (name, today, now))
    conn.commit()
    print(f"[ATTENDANCE] {name} marked present at {now}")

# ---------- Kinect ----------
fn  = Freenect2()
dev = fn.openDefaultDevice()
listener = SyncMultiFrameListener(FrameType.Color)
dev.setColorFrameListener(listener)
dev.start()
print("🎥  Kinect stream started.  Press  ESC  to quit,  N  to register unknown.")

# track recently‑seen unknowns to avoid spam
unknown_seen = {}

while True:
    frames   = listener.waitForNewFrame()
    color_fr = frames["color"].asarray()
    bgr      = cv2.cvtColor(color_fr, cv2.COLOR_BGRA2BGR)
    rgb_small = cv2.resize(bgr, (0,0), fx=0.25, fy=0.25)
    boxes     = face_recognition.face_locations(rgb_small, model="hog")
    encs      = face_recognition.face_encodings(rgb_small, boxes)

    for (top, right, bottom, left), enc in zip(boxes, encs):
        matches = face_recognition.compare_faces(known_enc, enc, TOLERANCE)
        face_dist = face_recognition.face_distance(known_enc, enc)
        name = "Unknown"

        if True in matches:
            idx  = np.argmin(face_dist)
            name = known_name[idx]
            mark_attendance(name)
            colour = (0,255,0)
        else:
            # avoid endless Unknown spam
            now = datetime.datetime.now()
            fid = uuid.uuid4().hex[:8]
            if fid not in unknown_seen or (now - unknown_seen.get(fid, now)).seconds > UNKNOWN_TIMEOUT:
                unknown_seen[fid] = now
            colour = (0,0,255)

        # scale coords back to full size
        top, right, bottom, left = [int(v*4) for v in (top, right, bottom, left)]
        if VIEW:
            cv2.rectangle(bgr, (left, top), (right, bottom), colour, 2)
            cv2.putText(bgr, name, (left, top-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, colour, 2)

    if VIEW:
        cv2.imshow("AttendanceCam (ESC quit, N add)", bgr)

    key = cv2.waitKey(1) & 0xFF
    if key == 27:                      # ESC
        break
    elif key in (ord('n'), ord('N')):  # register new face
        # grab the biggest Unknown face in current frame
        if not boxes:
            print("No face visible to register.")
        else:
            # find largest face by area
            areas = [(r-l)*(b-t) for (t,r,b,l) in boxes]
            best  = boxes[int(np.argmax(areas))]
            t,r,b,l = [int(v*4) for v in best]
            crop = bgr[t:b, l:r]
            new_name = input("Enter employee name: ").strip()
            if new_name:
                path = f"{new_name.replace(' ','_')}.jpg"
                cv2.imwrite(path, crop)
                print(f"Saved head‑shot to {path}")
                new_enc = face_recognition.face_encodings(cv2.cvtColor(crop, cv2.COLOR_BGR2RGB))[0]
                known_enc.append(new_enc)
                known_name.append(new_name)
                enc_data.append({"name": new_name, "encoding": new_enc})
                pickle.dump(enc_data, open(ENC_FILE, "wb"))
                print(f"{new_name} added and ready for recognition ✔")

    listener.release(frames)

dev.stop(); dev.close()
cv2.destroyAllWindows()
conn.close()
print("Goodbye 👋")
