import face_recognition, pickle

# load the head‑shot
img = face_recognition.load_image_file("malu.jpg")

# get the 128‑D encoding
enc = face_recognition.face_encodings(img)[0]

# store it for later use
pickle.dump({"name": "Malu", "encoding": enc}, open("enc.pkl", "wb"))

print("Encoding saved to enc.pkl ✔")
