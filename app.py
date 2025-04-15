from flask import Flask, request, jsonify
import face_recognition
import os

app = Flask(__name__)

# Absolute path to the known_faces directory
known_faces_dir = r"D:\VIT-C\Projects\facial recognition\known_faces"

# Load known faces
known_face_encodings = []
known_face_names = []

# Ensure the known_faces directory exists
if os.path.exists(known_faces_dir):
    for filename in os.listdir(known_faces_dir):
        if filename.lower().endswith((".jpg", ".png", ".jpeg")):
            path = os.path.join(known_faces_dir, filename)
            image = face_recognition.load_image_file(path)
            encodings = face_recognition.face_encodings(image)
            if encodings:
                known_face_encodings.append(encodings[0])
                known_face_names.append(os.path.splitext(filename)[0])

@app.route('/detect', methods=['POST'])
def detect_face():
    # Check if a frame is part of the request
    if 'frame' not in request.files:
        return jsonify({"error": "No file part"}), 400

    frame = request.files['frame']

    try:
        # Load the uploaded image
        image = face_recognition.load_image_file(frame)

        # Find all face locations and face encodings in the uploaded image
        face_locations = face_recognition.face_locations(image)
        face_encodings = face_recognition.face_encodings(image, face_locations)

        # List of recognized face names
        face_names = []

        # Compare each face encoding with known face encodings
        for encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, encoding)
            name = "Unknown"

            # Check if any face matches
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]

            face_names.append(name)

        return jsonify({"names": face_names, "locations": face_locations})

    except Exception as e:
        # Catch any exceptions and return a meaningful error message
        return jsonify({"error": f"Error processing the image: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
