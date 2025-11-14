import face_recognition
import cv2
import numpy as np
from PyQt5.QtWidgets import QFileDialog, QApplication
import os
import sys

# Where to save the face encoding and preview image
SAVE_PATH = "saved_face.npy"
PREVIEW_IMAGE_PATH = "saved_face_preview.jpg"

# Returns True if the face is saved successfully, False otherwise
def save_face_from_image():
    # Initialize QApplication if it doesn't already exist
    app = QApplication.instance() or QApplication(sys.argv)

    # Open file dialog to select image
    file_path, _ = QFileDialog.getOpenFileName(
        None, "Select an image", "", "Images (*.png *.jpg *.jpeg *.bmp)"
    )
    
    if not file_path:
        print("No image selected.")
        return False

    # Read the selected image
    image = cv2.imread(file_path)
    if image is None:
        print("Could not read the selected image.")
        return False

    # Resize for faster processing
    small_image = cv2.resize(image, (0, 0), fx=0.25, fy=0.25)
    
    # Detect face(s) in the image
    face_locations = face_recognition.face_locations(small_image)

    if not face_locations:
        print("No face found in the image.")
        # Removqe any existing preview image
        if os.path.exists(PREVIEW_IMAGE_PATH):
            os.remove(PREVIEW_IMAGE_PATH)
        return False

    # Use the first face found to avoid multiple faces being processed
    top, right, bottom, left = face_locations[0]
    scaled_location = (top * 4, right * 4, bottom * 4, left * 4)

    # Compute face encoding
    face_encoding = face_recognition.face_encodings(
        image, known_face_locations=[scaled_location]
    )[0]
    
    # Save encoding to the specified path
    np.save(SAVE_PATH, face_encoding)
    print(f"Face saved to: {SAVE_PATH}")

    # Draw rectangle around face and save preview image
    preview_image = image.copy()
    cv2.rectangle(
        preview_image,
        (scaled_location[3], scaled_location[0]),
        (scaled_location[1], scaled_location[2]),
        (0, 255, 0),
        2
    )
    cv2.imwrite(PREVIEW_IMAGE_PATH, preview_image)

    print(f"Preview image saved to: {PREVIEW_IMAGE_PATH}")
    return True
