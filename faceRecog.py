import os
import face_recognition

# Absolute path to the known_faces directory (using raw string to avoid backslash issues)
known_faces_dir = r"D:\VIT-C\Projects\facial recognition\known_faces.jpg"

# Check if the directory exists
if not os.path.exists(known_faces_dir):
    print("Directory does not exist:", known_faces_dir)
else:
    print("Directory exists:", known_faces_dir)

# Assuming known_face_encodings and known_face_names are already defined
known_face_encodings = []
known_face_names = []

# Loop through the files in the known_faces directory
for filename in os.listdir(known_faces_dir):
    if filename.lower().endswith((".jpg", ".png", ".jpeg")):
        path = os.path.join(known_faces_dir, filename)  # Get absolute path to the file
        print("Processing:", path)  # Check each file's absolute path
        image = face_recognition.load_image_file(path)
        encodings = face_recognition.face_encodings(image)
        if encodings:
            known_face_encodings.append(encodings[0])
            known_face_names.append(os.path.splitext(filename)[0])

# Check the results
print("Encodings:", known_face_encodings)
print("Names:", known_face_names)
