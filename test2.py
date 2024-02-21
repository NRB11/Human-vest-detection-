import cv2
import numpy as np

def create_yellow_mask(image):
    # Convert the image from BGR to HSV color space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Define lower and upper bounds for the yellow color
    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([30, 255, 255])
    
    # Create a mask that selects only yellow pixels
    yellow_mask = cv2.inRange(hsv_image, lower_yellow, upper_yellow)
    
    # Apply morphological operations to remove noise
    kernel = np.ones((5, 5), np.uint8)
    yellow_mask = cv2.morphologyEx(yellow_mask, cv2.MORPH_OPEN, kernel)
    yellow_mask = cv2.morphologyEx(yellow_mask, cv2.MORPH_CLOSE, kernel)
    
    return yellow_mask

def apply_mask(image, mask):
    # Create a copy of the original image
    masked_image = np.copy(image)
    
    # Set pixels outside the mask to black
    masked_image[mask != 255] = [0, 0, 0]
    
    return masked_image

if __name__ == "__main__":
    # Open the default camera
    cap = cv2.VideoCapture(0)
    
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        
        if not ret:
            break
        
        # Create a mask for yellow objects
        yellow_mask = create_yellow_mask(frame)
        
        # Apply the mask to the original frame
        masked_frame = apply_mask(frame, yellow_mask)
        
        # Display the original frame and the masked frame
        cv2.imshow("Original Frame", frame)
        cv2.imshow("Yellow Masked Frame", masked_frame)
        
        # Check for key press
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
    
    # Release the camera and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()
