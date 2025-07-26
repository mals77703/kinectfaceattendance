# 🧠 Face Recognition-Based Attendance System (Raspberry Pi + Kinect v2)

## 📌 Project Overview

This project implements a real-time face recognition attendance system using a **Raspberry Pi** and **Kinect v2**, designed for small office, lab, or classroom settings. It detects and recognizes faces, logs attendance into a local SQLite database, and supports image encoding for new users.

## 🔧 Tech Stack

- **Hardware**: Raspberry Pi 4 (64-bit OS), Kinect v2 (via libfreenect2)
- **Languages**: Python
- **Libraries**: `face_recognition`, `OpenCV`, `pickle`, `sqlite3`
- **Database**: SQLite
- **OS**: Raspberry Pi OS (booting from USB)

## ✨ Features

- Real-time face detection and recognition using Kinect v2
- Attendance logged in `attendance.db` with unique daily entries
- Face encoding for new users via `encode_face.py` or built-in feature
- Live camera feed with feedback in terminal
- Runs without GUI if needed (`--noview` mode)
- USB-bootable Raspberry Pi setup (no SD card needed)

## 📂 File Structure

```
├── encode_face.py             # For encoding faces from images
├── recognize_and_log.py       # Main script (was: attendance_kinect_v2.py)
├── attendance.db              # SQLite database file for logs
├── enc.pkl                    # Stored face encodings
├── capture_debug.py          # Saves a test image from Kinect
├── hello_kinect.py           # Preview Kinect stream and capture with 'S'
└── attendance_kinect.py       # Simpler version logging to text file
```

## 🧪 How It Works

### 1. Register Face
Run the following to capture and encode a new face manually:
```bash
python hello_kinect.py  # Press 'S' to save an image as malu.jpg
python encode_face.py   # Saves face encoding to enc.pkl
```
Or, run the main script and press **`N`** during detection to register a new face interactively.

### 2. Run Attendance Logger
```bash
python recognize_and_log.py
```
- Automatically detects and logs attendance in `attendance.db`
- One entry per user per day

### 3. View Attendance
```bash
sqlite3 attendance.db
.headers on
.mode column
SELECT * FROM log;
.quit
```

## 🔓 Known Limitations

- Requires decent lighting for best results
- Kinect needs USB 3.0 and root permissions
- Manual face capture still required initially

## 🎯 Future Add-ons (WIP)
- [x] USB-boot OS support
- [x] Kinect v2 integration
- [x] Multi-user detection
- [ ] Cloud sync (Option B)
- [ ] Web dashboard (Option C)
- [ ] Admin panel with CRUD (Option D)
- [ ] Masked face support (TBD)

## 💡 Use Case Fit

This project is a great fit for:
- Real-time **computer vision** and **ML on edge devices**
- **IoT-based attendance tracking systems**
- Applied AI/ML engineering roles (esp. CV/Edge/Tooling)

## 🎓 Authored By
**Malu** – Built from scratch using open-source tools and real-world hardware.
> For more, visit: [github.com/yourusername](https://github.com/yourusername)
