import cv2
import mediapipe as mp

# Function to check if a given color is black
def is_black(color):
    # Define the threshold for considering a color as black
    threshold = 50
    return all(value < threshold for value in color)

# Function to check if the detected region represents a black t-shirt
def has_black_shirt(image, landmarks):
    # Get color of the center of the detected t-shirt
    height, width, _ = image.shape
    center_x = int(landmarks.landmark[mp.holistic.PoseLandmark.LEFT_SHOULDER].x * width)
    center_y = int(landmarks.landmark[mp.holistic.PoseLandmark.LEFT_SHOULDER].y * height)
    color = image[center_y, center_x]

    # Check if the color is black
    return is_black(color)

# Initialize MediaPipe pose detection
mp_holistic = mp.solutions.holistic
holistic = mp_holistic.Holistic()

# Initialize VideoCapture
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the image to RGB
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect poses
    results = holistic.process(image)

    # Draw pose landmarks
    if results.pose_landmarks:
        mp.solutions.drawing_utils.draw_landmarks(
            image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)

        # Check if the person is wearing a black t-shirt
        if has_black_shirt(image, results.pose_landmarks):
            cv2.putText(image, 'Black T-shirt Detected', (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    # Convert image back to BGR for displaying
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # Display output
    cv2.imshow('MediaPipe Holistic - Black T-shirt Detection', image)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the VideoCapture and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
