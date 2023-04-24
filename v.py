import cv2
import mediapipe as mp
import pyautogui

# Define the size of the screen
screen_width, screen_height = pyautogui.size()

# Initialize the camera and the MediaPipe hand detection model
cap = cv2.VideoCapture(0)
mp_hands = mp.solutions.hands.Hands(max_num_hands=1)

# Define the initial volume level
volume = 50

# Loop over frames from the camera
while True:
    # Read a frame from the camera
    ret, frame = cap.read()

    # Convert the frame to RGB and pass it to the MediaPipe hand detection model
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = mp_hands.process(frame_rgb)

    # Extract the hand landmarks from the detection results
    if results.multi_hand_landmarks:
        hand_landmarks = results.multi_hand_landmarks[0]

        # Calculate the distance between the thumb tip and the ring tip
        thumb_tip = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.THUMB_TIP]
        ring_tip = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.RING_FINGER_TIP]
        distance = ((thumb_tip.x - ring_tip.x)**2 +
                    (thumb_tip.y - ring_tip.y)**2)**0.5

        # Map the distance to a volume level between 0 and 100
        volume = int((1 - distance) * 100)

        # Set the system volume using PyAutoGUI
        pyautogui.press('volumedown')
        for i in range(volume):
            pyautogui.press('volumeup')

        # Display the current volume level
        print(f"Volume: {volume}")

    # Display the frame
    cv2.imshow('frame', frame)

    # Exit if the 'q' key is pressed
    if cv2.waitKey(1) == ord('q'):
        break

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()
