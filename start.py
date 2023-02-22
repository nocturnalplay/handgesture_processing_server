import cv2
import mediapipe as mp

# url of the video streaming server
url = "http://192.168.1.6:8000/video_feed"

try:
    mp_drawing = mp.solutions.drawing_utils
    mp_hands = mp.solutions.hands

    cap = cv2.VideoCapture(url)

    with mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5) as hands:

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                break

            # Flip the frame horizontally for a later selfie-view display
            frame = cv2.flip(frame, 1)

            # Convert the image to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Process the image with mediapipe
            results = hands.process(image)

            # Draw the hand landmarks on the image
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Display the resulting image
            cv2.imshow('Hand Gestures', cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
            if cv2.waitKey(1) == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()
except KeyboardInterrupt:
    print("exit...operation")
    cap.release()
    cv2.destroyAllWindows()
