import cv2
import dlib
import time
from scipy.spatial import distance as dist
from imutils import face_utils
import mediapipe as mp

EYE_AR_THRESH = 0.25  # Eye Aspect Ratio threshold for eye closure
CLOSED_DURATION_REQUIRED = 2.0  # Duration required for eyes to be closed
PEACE_HOLD_REQUIRED = 2.0  # Duration required to hold peace sign gesture

# Eye Aspect Ratio (EAR) calculation
def eye_aspect_ratio(eye):
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])
    return (A + B) / (2.0 * C)

# Checks eye closure and peace sign gesture for liveness
# Returns True if both checks pass, False otherwise
def liveness_check():
    # Initialize dlib's face detector and shape predictor
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
    (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
    (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

    # Initialize MediaPipe for hand gesture recognition
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1)
    mp_draw = mp.solutions.drawing_utils

    # Initialize webcam capture
    cap = cv2.VideoCapture(0)

    # Initialize variables for liveness checks
    closed_start_time = None  # Time when eyes were first closed
    peace_start_time = None  # Time when peace sign gesture was first detected
    eye_liveness_passed = False  # Whether eye closure check passed
    gesture_verified = False  # Whether peace sign gesture was verified
    short_msg = ""
    show_short_blink_msg_until = 0  # Time until which short blink message is shown
    show_eye_passed_msg_until = 0  # Time until which eye check passed message is shown

    # Initialize step timing
    EYE_STEP_TIME = 15
    HAND_STEP_TIME = 15

    eye_step_start = time.time()
    hand_step_start = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Convert frame to grayscale and flip for better visualization
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        flipped = cv2.flip(frame, 1)

        # Convert flipped frame to RGB for MediaPipe processing
        rgb_flipped = cv2.cvtColor(flipped, cv2.COLOR_BGR2RGB)
        current_time = time.time()

        # Step 1: Eye closure
        if not eye_liveness_passed:
            time_left = max(0, EYE_STEP_TIME - (current_time - eye_step_start))
            timer_text = f"Time left: {time_left:.1f}s"
            cv2.putText(
                frame, timer_text, (frame.shape[1] - 250, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255) if time_left < 5 else (0, 255, 255), 3
            )

            # Show the instructions for eye closure in the top left corner
            cv2.putText(frame, "STEP 1: Close eyes for 2 seconds", (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 255), 3)

            rects = detector(gray, 0)
            if rects:
                for rect in rects:
                    shape = predictor(gray, rect)
                    shape = face_utils.shape_to_np(shape)

                    left_eye = shape[lStart:lEnd]
                    right_eye = shape[rStart:rEnd]
                    ear = (eye_aspect_ratio(left_eye) + eye_aspect_ratio(right_eye)) / 2.0

                    cv2.putText(frame, f"EAR: {ear:.2f}", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 255), 3)

                    if ear < EYE_AR_THRESH:
                        if closed_start_time is None:
                            closed_start_time = current_time
                        elapsed = current_time - closed_start_time

                        cv2.putText(frame, f"Closed: {elapsed:.1f}s", (20, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 3)

                        if elapsed >= CLOSED_DURATION_REQUIRED:
                            eye_liveness_passed = True
                            show_eye_passed_msg_until = current_time + 2
                            closed_start_time = None
                            hand_step_start = time.time()
                    else:
                        if closed_start_time:
                            elapsed = current_time - closed_start_time
                            if elapsed > 0.3:
                                short_msg = f"Eyes closed for only {elapsed:.1f}s — close for 2s"
                                show_short_blink_msg_until = current_time + 2
                            closed_start_time = None

                    cv2.drawContours(frame, [cv2.convexHull(left_eye)], -1, (0, 255, 0), 1)
                    cv2.drawContours(frame, [cv2.convexHull(right_eye)], -1, (0, 255, 0), 1)

            if current_time < show_short_blink_msg_until:
                cv2.putText(frame, short_msg, (20, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 3)

            if time_left <= 0:
                break

        # Step 2: Peace sign gesture
        elif not gesture_verified:
            time_left = max(0, HAND_STEP_TIME - (current_time - hand_step_start))
            timer_text = f"Time left: {time_left:.1f}s"
            cv2.putText(
                flipped, timer_text, (flipped.shape[1] - 250, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255) if time_left < 5 else (0, 255, 255), 3
            )

            cv2.putText(flipped, "STEP 2: Hold up your INDEX and MIDDLE fingers", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 255), 3)
            cv2.putText(flipped, "Keep your PALM facing the camera", (60, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 3)
            cv2.putText(flipped, "Hold for 2 seconds to verify!", (60, 130), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 3)

            if current_time < show_eye_passed_msg_until:
                text = "Eye check passed"
                (tw, th), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1.0, 3)
                x = flipped.shape[1] - tw - 40
                y = flipped.shape[0] - 40
                cv2.putText(flipped, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 3)

            result = hands.process(rgb_flipped)
            if result.multi_hand_landmarks:
                hand_landmarks = result.multi_hand_landmarks[0]
                mp_draw.draw_landmarks(flipped, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                lm = hand_landmarks.landmark

                def is_up(tip_id): return lm[tip_id].y < lm[tip_id - 2].y

                if is_up(8) and is_up(12) and not is_up(16) and not is_up(20) and not (lm[4].x < lm[3].x):
                    if peace_start_time is None:
                        peace_start_time = current_time
                    held_time = current_time - peace_start_time

                    cv2.putText(flipped, f"Held: {held_time:.1f}s", (60, 170), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 3)

                    if held_time >= PEACE_HOLD_REQUIRED:
                        gesture_verified = True
                        break
                else:
                    peace_start_time = None

            if time_left <= 0:
                break

        # Final "Hand check passed" message
        elif gesture_verified:
            end_time = current_time + 2
            while time.time() < end_time:
                text = "Hand check passed"
                (tw, th), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1.2, 4)
                x = flipped.shape[1] - tw - 40
                y = flipped.shape[0] - 40
                cv2.putText(flipped, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 4)
                cv2.imshow("Liveness Check", flipped)
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
            break

        cv2.imshow("Liveness Check", flipped if eye_liveness_passed else frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return eye_liveness_passed and gesture_verified

if __name__ == "__main__":
    result = liveness_check()
    print("\nLiveness check passed." if result else "\nLiveness check failed.")
