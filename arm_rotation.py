import cv2
import math
import numpy as np

# Open the video file
video_path = 'dataset/bandu/bandu-forehand.mp4'  # Replace with the path to your video file
cap = cv2.VideoCapture(video_path)

# Frame rate of the video
frame_rate = 30.0  # Replace with your video's frame rate

# Initialize variables for arm speed rotation calculation
previous_frame = None
frame_number = 0
arc_length = 0
rotation_angle_degrees = 0

# Distance from the axis of rotation (e.g., shoulder) to the reference point (e.g., wrist or racket handle) in meters
radius_meters = 0.5  # Replace with the actual radius

# Initialize the linear_speed_mph variable outside the loop
linear_speed_mph = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Calculate arm speed rotation
    if previous_frame is not None:
        # Calculate frame-to-frame motion using optical flow
        flow = cv2.calcOpticalFlowFarneback(
            cv2.cvtColor(previous_frame, cv2.COLOR_BGR2GRAY),
            cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY),
            None, 0.5, 3, 15, 3, 5, 1.2, 0
        )

        # Calculate the magnitude of motion vectors
        magnitude = np.sqrt(flow[:, :, 0] ** 2 + flow[:, :, 1] ** 2)

        # Calculate the arc length by summing the magnitudes
        arc_length += np.sum(magnitude)

        # Calculate the rotation angle in degrees
        rotation_angle_degrees = (arc_length / (2 * np.pi * radius_meters)) * 360

        # Convert angular speed (degrees per second) to linear speed (miles per hour)
        angular_speed_deg_per_sec = rotation_angle_degrees * frame_rate
        linear_speed_m_per_sec = angular_speed_deg_per_sec * (2 * np.pi * radius_meters / 360)
        linear_speed_mph = linear_speed_m_per_sec * 2.23694  # 1 m/s = 2.23694 mph

    # Write the frame with arm speed rotation information to the output video
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, f'Arm Speed Rotation: {linear_speed_mph:.2f} mph', (20, 30), font, 1, (255, 255, 255), 2)
    
    # Display the frame with arm speed rotation information
    cv2.imshow('Arm Speed Rotation (mph)', frame)

    # Store the current frame as the previous frame for the next iteration
    previous_frame = frame.copy()
    frame_number += 1

    # Exit the loop if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release video objects and close windows
cap.release()
cv2.destroyAllWindows()
