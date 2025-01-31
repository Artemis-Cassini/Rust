import cv2
import numpy as np

# Set up the camera
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    
    if not ret:
        print("Failed to grab frame.")
        break

    # Resize frame for faster processing
    frame = cv2.resize(frame, None, fx=0.7, fy=0.7)

    # Convert the frame to HSV (Hue, Saturation, Value) color space
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define the range of skin color in HSV
    lower_skin = np.array([0, 20, 70], dtype=np.uint8)
    upper_skin = np.array([20, 255, 255], dtype=np.uint8)

    # Create a mask to filter out the skin region
    skin_mask = cv2.inRange(hsv_frame, lower_skin, upper_skin)

    # Apply Gaussian blur to reduce noise
    skin_mask = cv2.GaussianBlur(skin_mask, (7, 7), 0)

    # Use morphological operations to clean up the mask
    kernel = np.ones((5, 5), np.uint8)
    skin_mask = cv2.dilate(skin_mask, kernel, iterations=2)
    skin_mask = cv2.erode(skin_mask, kernel, iterations=1)

    # Apply the mask to the original frame
    skin_segment = cv2.bitwise_and(frame, frame, mask=skin_mask)

    # Find contours in the masked image
    contours, _ = cv2.findContours(skin_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw contours around detected hands
    for contour in contours:
        if cv2.contourArea(contour) > 3000:  # Filter small contours
            # Approximate the contour to reduce points
            epsilon = 0.02 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)

            # Get bounding box around the contour
            x, y, w, h = cv2.boundingRect(approx)
            
            # Draw a rectangle for the hand
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Optionally, draw the contour itself
            cv2.drawContours(frame, [approx], -1, (0, 255, 255), 2)

    # Display the frame with hand detection
    cv2.imshow("Hand Detection", frame)
    cv2.imshow("Skin Mask", skin_mask)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close the window
cap.release()
cv2.destroyAllWindows()