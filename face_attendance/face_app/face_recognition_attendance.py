import face_recognition
import cv2
import numpy as np

def load_user_profile_encoding(profile_picture_path):
    if not profile_picture_path:
        return None

    try:
        # Load image using OpenCV
        image = cv2.imread(profile_picture_path)
        if image is None:
            print(f"Error: Unable to load image from {profile_picture_path}")
            return None

        # Convert BGR to RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Ensure the image is 8-bit
        if image_rgb.dtype != np.uint8:
            image_rgb = image_rgb.astype(np.uint8)

        encodings = face_recognition.face_encodings(image_rgb)
        if encodings:
            return encodings[0]
        return None
    except Exception as e:
        print(f"Error processing profile picture: {e}")
        return None

def compare_faces(frame, user_encoding, tolerance=0.4):
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for encoding in face_encodings:
        distance = face_recognition.face_distance([user_encoding], encoding)  # ✅ Get similarity score
        match = distance[0] < tolerance  # ✅ Match only if distance is below threshold

        if match:
            return True, face_locations  # ✅ Return match status and face locations

    return False, face_locations  # ✅ Return false if no match
