import cv2
import numpy as np

# Open the video file
video_path = 'dataset/bandu/bandu-forehand.mp4'  # Replace with the path to your video file
cap = cv2.VideoCapture(video_path)

# Define the frame rate of the video
frame_rate = 30.0  # Replace with your video's frame rate

# Initialize variables for racket hitting arm angle calculation
previous_frame = None
racket_angle_degrees = 0
impact_detected = False

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Detect and track the player's arm and racket
    # You should replace this part with your own object detection and tracking code

    # Perform color thresholding to detect the tennis ball (impact event)
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_bound = np.array([30, 100, 100])  # Adjust these values based on the ball's color
    upper_bound = np.array([50, 255, 255])  # Adjust these values based on the ball's color
    mask = cv2.inRange(hsv_frame, lower_bound, upper_bound)
    contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Check if the impact event (ball presence) is detected
    if len(contours) > 0:
        impact_detected = True
        print("Shot Hit!")
    # Calculate the racket hitting arm angle when the impact event is detected
    if impact_detected:
        # You need to determine the positions of the arm and racket at this moment
        # and then calculate the angle using trigonometric functions

        # Example: Calculate the angle as 45 degrees for demonstration purposes
        racket_angle_degrees = 45
      

    # Display the frame with the calculated angle
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, f'Racket Hitting Arm Angle: {racket_angle_degrees:.2f} degrees', (20, 30), font, 1, (255, 255, 255), 2)
    cv2.imshow('Racket Hitting Arm Angle', frame)

    # Store the current frame as the previous frame for the next iteration
    previous_frame = frame.copy()

    # Exit the loop if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release video objects and close windows
cap.release()
cv2.destroyAllWindows()
