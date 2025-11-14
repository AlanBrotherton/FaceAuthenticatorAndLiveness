import face_recognition
import cv2
import numpy as np
import os
import time

SAVE_PATH = "saved_face.npy"
FACE_MATCH_THRESHOLD = 0.6  # A threshold to determine how close the match should be

def draw_text(img, text, position, color=(255, 255, 255), size=0.6, thickness=2):
    cv2.putText(img, text, position, cv2.FONT_HERSHEY_SIMPLEX, size, color, thickness, lineType=cv2.LINE_AA)

# Check if the save_face has been run and a saved face file exists
# Returns True if the face is verified successfully, False otherwise
def verify_face(): 
    if not os.path.exists(SAVE_PATH):
        print("Saved face encoding not found. Please save a face first.")
        return False

    # Load the saved face encoding
    saved_encoding = np.load(SAVE_PATH)
    
    # Initialize webcam capture
    cap = cv2.VideoCapture(0)

    # Check if the webcam opened successfully
    match_result = False
    message = ""
    message_color = (0, 255, 0)
    show_until = 0

    # Capture frames from the webcam
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture image.")
            break

        # Get current time
        current_time = time.time()

        # Resize frame for faster processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        face_locations = face_recognition.face_locations(small_frame)
        scaled_locations = [(top*4, right*4, bottom*4, left*4) for (top, right, bottom, left) in face_locations]

        # Draw rectangles around detected faces
        if scaled_locations:
            top, right, bottom, left = scaled_locations[0]
            cv2.rectangle(frame, (left, top), (right, bottom), (255, 0, 0), 2)

        # Draw instructions in top left corner
        draw_text(frame, "Press 'v' to verify, 'q' to quit", (20, 50), (0, 255, 255), size=0.9, thickness=3)

        # Draw result message 
        if current_time < show_until:
            draw_text(frame, message, (20, 100), message_color, size=0.9, thickness=3)

        # Show the frame with rectangles and instructions
        cv2.imshow("Verify Face", frame)

        # Wait for user input
        key = cv2.waitKey(1) & 0xFF

        # If 'v' is pressed, verify the face
        if key == ord('v') and scaled_locations:
            print("Verifying face...")
            test_encoding = face_recognition.face_encodings(
                frame, known_face_locations=[scaled_locations[0]]
            )[0]

            distance = np.linalg.norm(saved_encoding - test_encoding)
            print(f"Distance: {distance:.3f}")

            # Compare the distance with the threshold
            if distance < FACE_MATCH_THRESHOLD:
                message = "Match: Same person"
                message_color = (0, 255, 0)
                match_result = True
                print(message)
            else:
                message = "No match: Different person"
                message_color = (0, 0, 255)
                match_result = False
                print(message)

            # Show the above message for 2 seconds
            show_until = time.time() + 2
            time.sleep(1.5)
            break


        # If 'q' is pressed, exit the loop
        elif key == ord('q'):
            print("Verification aborted by user.")
            break

    cap.release()
    cv2.destroyAllWindows()
    return match_result

if __name__ == "__main__":
    success = verify_face()
    print("\nVerification result: Access Granted" if success else "\nVerification result: Access Denied")
